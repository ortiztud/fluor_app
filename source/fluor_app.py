# -*- coding: utf-8 -*-
"""
victor_ADN

Author: Javier Ortiz-Tudela (github.com/ortizTud)

"""
import os
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import datetime
import scipy
from scipy import stats

# Global variables
height = 400
width = 500
method = 999
method_lab = "default"
   
# Define get time
def get_time():
    ts = datetime.datetime.now()
    return ts.strftime("%y%m%d_%H%M")
    
# Define window close
def quit():

 	# Print goodbye message
 	root.destroy()
 	gbye = tk.Tk()

 	# Create canvas
 	canvas = tk.Canvas(gbye, height = 100, width = 500, bg='#005fcd')
 	canvas.pack()
 	
 	# Create frame
 	frame = tk.Frame(gbye, bg='#005fcd')
 	frame.place(relwidth=1, relheight=1)

 	# Create prompt
 	label = tk.Label(frame, text="Archivo de resultados creado. \n Puede cerrar esta ventana.", font=30,bg="white", fg="black")
 	label.place(relx=.1, rely=.3,relwidth=.8, relheight=.4)
 	
 	frame2 = tk.Frame(gbye, bg='#005fcd')
 	frame2.pack()
 	label2 = tk.Label(frame2, text="github.com/ortizTud", bg='#005fcd',fg="white", font=("Arial", 10, "italic"))
 	label2.pack()

	# Close all
	#time.sleep(3)
	#gbye.destroy()

def error_warn(message, color):
     # Print warning if wrong file
 	err = tk.Tk()

     # Create canvas
 	canvas = tk.Canvas(err, height = 100, width = 500, bg=color)
 	canvas.pack()
 	
 	# Create frame
 	frame = tk.Frame(err, bg=color)
 	frame.place(relwidth=1, relheight=1)

 	# Create prompt
 	label = tk.Label(frame, text=message, font=30, bg="white", fg="black")
 	label.place(relx=.1, rely=.3,relwidth=.8, relheight=.4)

# Def function
def load_file():
    filename = filedialog.askopenfilename()
    print(filename)
    
    try:
        
        # Read in the file
        dataframe = pd.read_csv(filename, nrows=96, sep="\t", usecols=(2,5))
        dataframe.head() # prints out first rows of your data
        
        dataframe.rename(columns={'Qubit_Fluorescein (Counts)':'Fluor'}, inplace = True)
        a1 = dataframe[dataframe.Well == "A01"]
        b1 = dataframe[dataframe.Well == "B01"]
        a1 = a1.at[0, 'Fluor']
        b1 = b1.at[12, 'Fluor']

        # Ask user for cuantification method
        method = simpledialog.askstring("Input", parent=root,
                                        prompt="Elige el tipo de cuantificación: \n 1. muestras de ADN \n 2. librerías individuales",)
    except:
        print("error")
        error_warn("Archivo incorrecto; seleccione otro", "#eb2a00")
        
    # Chose feats upon request
    if (method == '1'):
        method_lab = "ADN_original"
        factor = 1
    elif (method == '2'):
        method_lab = "librerias"
        factor = 4
    print(method_lab + " chosen as method")
    
    ## Compute ADN
    # Standards
    std = (0, 10)
      
    # Fluorescense values
    y = (a1, b1)
       
    # Run regression
    linear_regressor  = scipy.stats.linregress(std,y)
      
    # Get values from regression
    slope = linear_regressor.slope
    interc = linear_regressor.intercept
      
    # Get fluor values
    fluor_vals = dataframe.loc[:, 'Fluor']
      	
    # Predicted DNA
    predicted = (fluor_vals - interc)/slope
    predicted = predicted * factor
    predicted = round(predicted, 1)
    predicted[predicted <=0] = 0
      
    # Format for outputing
    data = np.array([predicted[:]])
    data = data.reshape(8,12)
    
    # Re-code standards
    data[0,0] = 0
    data[1,0] = 10
    df= pd.DataFrame(data)
      
    ## Write output file ##
    # Cols and rows names
    col_names = [1,2,3,4,5,6,7,8,9,10,11,12]
    row_names = pd.DataFrame(["","A", "B", "C", "D", "E", "F", "G", "H"])
    
    # Open output file
    out_dir="../resultados_concentracion_ADN/"
    os.makedirs(out_dir, exist_ok=True)
    ts = get_time()
    out_filename = out_dir + method_lab + "_" + ts + ".xlsx"
    writer = pd.ExcelWriter(out_filename, engine='xlsxwriter')
      
    # Write row names
    row_names.to_excel(writer, header = False, index = False)
      
    # Write data
    df.to_excel(writer, startcol = 1, header = col_names, index = False)
    
    # Close file
    writer.save()
    print("output generated")
    quit()
        
# Create main window
root = tk.Tk()

# Create canvas
canvas = tk.Canvas(root, height = height, width = width, bg='white')
canvas.pack()

# Define image
bck_im = tk.PhotoImage(file= ".img\logo.png", master=root)
bck_label = tk.Label(root, image=bck_im)
bck_label.place(relx=0, relwidth=1, relheight=.4)

# Create prompt
label = tk.Label(canvas, text="Cargue en esta ventana su archivo de resultados", bg="white", font=30)
label.place(rely=0.1,relwidth=1, relheight=1)

# Create frame
frame = tk.Frame(root, bg='#005fcd')
frame.place(rely=.8, relwidth=1, relheight=.2)
label2 = tk.Label(frame, text="github.com/ortizTud", bg='#005fcd',fg="white", font=("Arial", 10, "italic"))
label2.pack(side="right")

# Create button
button = tk.Button(frame, text="Click para buscar...", bg="#ca8943", command=lambda: load_file())
button.place(relx=0.5,relwidth=.3, anchor="n")

# Close the window
root.mainloop()


