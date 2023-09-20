#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Tkinter
from tkinter import *
from tkinter import messagebox, filedialog, messagebox, ttk
from PIL import ImageTk, Image

#Metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

#Misc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

#Classifiers
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import GridSearchCV

#Global Variables that need to be placed
root = Tk()
file_path = 'change this in function below' #will be reassigned in csv_opener()
choose_csv_frame = LabelFrame(root, pady= 6, padx=15)
df = pd.DataFrame() #will ve reassigned in csv_opener()

def create_root(project_name):
    
    #create root
    root.title(project_name)
    
    #title at top
    title_label = Label(root, bg="gray", padx = 185, text = project_name)
    title_label.place(anchor=CENTER, relx= 0.5, y=10)
    
    #size
    # width= root.winfo_screenwidth()               
    # height= root.winfo_screenheight()
    # root.geometry("%dx%d" % (width, height))
    root.geometry("1400x700")
    # root.resizable(False,False)

def root_loop() -> int:
    #start root loop
    root.mainloop()
    
    return 0

 #get file path

def csv_opener():
    #choose CSV File
    csv_file_name = Label(choose_csv_frame ,text="No File Selected")
    choose_csv_frame.filename = filedialog.askopenfilename(initialdir="/C", title="Select CSV File", filetypes=(("CSV Files", "*.csv"),))
    csv_file_name["text"] = choose_csv_frame.filename
    global file_path
    file_path = csv_file_name["text"]
    print(file_path)

    #make df
    global df
    df = pd.read_csv(file_path)

    #delete choose_csv_frame
    csv_submission_successful = messagebox.showinfo("Submission Successful", "The data has been submitted successfully")
    if csv_submission_successful == "ok":
        choose_csv_frame.place_forget()
        treeview_of_df()

def choose_csv():
    #label frame to put things in
    choose_csv_frame.place(anchor=CENTER, relx= 0.5, y=50)
    
    choose_csv_button = Button(choose_csv_frame, text="Choose Select CSV File", command= csv_opener)
    choose_csv_button.grid(row= 0, column=0)

def treeview_of_df():
    #~~ treeview ~~#
    # create tree view frame & treeview
    treevew_data_frame = LabelFrame(root, padx=40, text="Data Display")
    tv = ttk.Treeview(treevew_data_frame,height=15)
    y_scrollbar = ttk.Scrollbar(treevew_data_frame, orient="vertical")
    x_scrollbar = ttk.Scrollbar(treevew_data_frame, orient="horizontal", command=tv.xview)

    #put frame on grid
    treevew_data_frame.pack(fill=None, expand=False)
    #put scroll bars
    tv.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=RIGHT, fill="y")
    x_scrollbar.pack(side=BOTTOM, fill="x")
    y_scrollbar.config(command= tv.yview)
    x_scrollbar.config(command= tv.xview)

    #show columns and list
    tv["column"] = list(df.columns)
    tv["show"] = "headings"
    for column in tv["column"]:
        tv.heading(column, text = column)
        tv.column(column, width=100, minwidth=100)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv.insert("", "end", values= row)

    tv.pack()

    #~~ Simple EDA ~~#
    #check is_na of all columns
    
    for column in df.columns:
        column_is_na = f"{column}: {df[column].isna().any()}"

        column_is_na_label = Label(root, padx = 185, text = column_is_na)
        # column_is_na_label.place(anchor=CENTER, relx= 0.5, y=10)
        column_is_na_label.pack()


    #~~ What actions ~~#
    # transform_data_button = Button(treevew_data_frame, text="Transform")
    # transform_data_button.grid(row= 0, column=0)

def main() -> int:
    """
    Main Function for processing the data
    arg:
        None
    returns:
        0: int
            exit code
    """

    create_root("Supervised ML Classifier")
    choose_csv()

    #runs the looping root
    root_loop()
    
    return 0
    
if (__name__ == "__main__"):
    
    main()
