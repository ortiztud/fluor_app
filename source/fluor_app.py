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
import time 
import datetime
from sklearn.linear_model import LinearRegression

# Global variables
height = 300
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
    std = np.array([0, 10]).reshape((-1, 1))
      
    # Fluorescense values
    y = np.array([a1, b1])
       
    # Run regression
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(std, y)  # perform linear regression
      
    # Get values from regression
    slope = linear_regressor.coef_
    interc = linear_regressor.intercept_
      
    # Get fluor values
    fluor_vals = dataframe.loc[:, 'Fluor']
      	
    # Predicted DNA
    predicted = (fluor_vals - interc)/slope
    predicted = predicted * factor
    predicted = round(predicted, 1)
    predicted[predicted <=0] = 0
    print(predicted)
      
    # Format for outputing
    a = np.array([predicted[:]])
    a = a.reshape(8,12)
    df= pd.DataFrame(a)
      
    ## Write output file
    # Cols and rows names
    col_names = [1,2,3,4,5,6,7,8,9,10,11,12]
    row_names = pd.DataFrame(["","A", "B", "C", "D", "E", "F", "G", "H"])
    
    # Open output file
    out_dir="resultados_concentracion_ADN/"
    os.makedirs(out_dir, exist_ok=True)
    ts = get_time()
    out_filename = "resultados_concentracion_ADN/" + method_lab + "_" + ts + ".xlsx"
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
bck_im = tk.PhotoImage(file= "logo.png", master=root)
bck_label = tk.Label(root, image=bck_im)
bck_label.place(relx=0, relwidth=1, relheight=.4)

# Create prompt
label = tk.Label(canvas, text="Cargue en esta ventana su archivo de resultados", bg="white", font=30)
label.place(relwidth=1, relheight=1)

# Create frame
frame = tk.Frame(root, bg='#005fcd')
frame.place(rely=.8, relwidth=1, relheight=.2)

# Create button
button = tk.Button(frame, text="Click para buscar...", bg="#ca8943", command=lambda: load_file())
button.place(relx=0.5,relwidth=.3, anchor="n")

# Close the window
root.mainloop()


