# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import time 
from sklearn.linear_model import LinearRegression

# Global variables
height = 100
width = 500

# Define window close
def quit():

	# Print goodbye message
	root.destroy()
	gbye = tk.Tk()

	# Create canvas
	canvas = tk.Canvas(gbye, height = 100, width = 500, bg='#6dda00')
	canvas.pack()
	
	# Create frame
	frame = tk.Frame(gbye, bg='#6dda00')
	frame.place(relx=0.1, relwidth=0.8, relheight=1)

	# Create prompt
	label = tk.Label(frame, text="Conversion complete. 'output.xlsx' created", bg="white", fg="black")
	label.pack(side="top", fill="x")

	# Close all
	#time.sleep(3)
	#gbye.destroy()

def error_warn():
    # Print warning if wrong file
	err = tk.Tk()

	# Create canvas
	canvas2 = tk.Canvas(err, height = 100, width = 500, bg='#eb2a00')
	canvas2.pack()
	
	# Create frame
	frame2 = tk.Frame(err, bg='#eb2a00')
	frame2.place(relx=0.1, relwidth=0.8, relheight=1)

	# Create prompt
	label = tk.Label(frame2, text="Incorrect file type selected. Try again", bg="white", fg="black")
	label.pack(side="top", fill="x")

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
        #predicted = round(predicted, 2)
    
        # Format for outputing
        a = np.array([predicted[:]])
        a = a.reshape(8,12)
        df= pd.DataFrame(a)
    
    	## Write output file
    	# Cols and rows names
        col_names = [1,2,3,4,5,6,7,8,9,10,11,12]
        row_names = pd.DataFrame(["","A", "B", "C", "D", "E", "F", "G", "H"])
    	
    	# Open file
        writer = pd.ExcelWriter("output.xlsx", engine='xlsxwriter')
    
        # Write row names
        row_names.to_excel(writer, header = False, index = False)
        
        # Write data
        df.to_excel(writer, startcol = 1, header = col_names, index = False)
    
        # Close file
        writer.save()
        print("output generated")
        quit()
    except:
        error_warn()
        
# Create main window
root = tk.Tk()

# Create canvas
canvas = tk.Canvas(root, height = height, width = width, bg='#80c1ff')
canvas.pack()

# Create frame
frame = tk.Frame(root, bg='#80c1ff')
frame.place(relx=0.1, relwidth=0.8, relheight=1)

# Create prompt
label = tk.Label(frame, text="Carga en esta ventana tu archivo de resultados", bg="white")
label.pack(side="top", fill="x")

# Create button
button = tk.Button(frame, text="Click para buscar...", bg="#ca8943", command=lambda: load_file())
button.pack(side="top")
#root.withdraw()

# Close the window
root.mainloop()


