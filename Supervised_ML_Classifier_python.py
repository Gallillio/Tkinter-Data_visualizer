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

#Global Variables & Frames that need to be placed
root = Tk()
file_path = 'change this in function below' #will be reassigned in csv_opener()
df = pd.DataFrame() #will ve reassigned in csv_opener()

# I keep all frames here incase I want to delete them later
choose_csv_frame = LabelFrame(root, pady= 6, padx=15)
treevew_data_frame = LabelFrame(root, padx=40, text="Data Display")
treevew_has_NA_data_frame = LabelFrame(root, padx=40, text="Does Column have NA")
transoform_data_frame = LabelFrame(root, text="Transform Data")


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

def run_code():
    choose_csv_frame.place_forget()
    treeview_of_df()
    transform_data()

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

    #delete choose_csv_frame / Starts Actual Apps
    csv_submission_successful = messagebox.showinfo("Submission Successful", "The data has been submitted successfully")
    if csv_submission_successful == "ok":
        # choose_csv_frame.place_forget()
        # treeview_of_df()
        # transform_data()
        run_code()

def choose_csv():
    #label frame to put things in
    choose_csv_frame.place(anchor=CENTER, relx= 0.5, y=50)
    
    choose_csv_button = Button(choose_csv_frame, text="Choose Select CSV File", command= csv_opener)
    choose_csv_button.grid(row= 0, column=0)

def treeview_of_df():
    #~~ treeview ~~#
    # create tree view frame & treeview
    tv = ttk.Treeview(treevew_data_frame,height=15)
    y_scrollbar = ttk.Scrollbar(treevew_data_frame, orient="vertical", command= tv.yview)
    x_scrollbar = ttk.Scrollbar(treevew_data_frame, orient="horizontal", command=tv.xview)

    #put frame on grid
    treevew_data_frame.pack(fill=None, expand=False)
    #put scroll bars
    tv.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=RIGHT, fill="y")
    x_scrollbar.pack(side=BOTTOM, fill="x")

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
    #create dataframe with data
    data = []
    for column in df.columns:
        column_has_na_list = [column, df[column].isna().any()]
        data.append(column_has_na_list)
        
    df_has_NA = pd.DataFrame(data, columns=["column_name", "column_has_NA"])

    # create tree view to show each column and if it has NA values
    tv_has_NA = ttk.Treeview(treevew_has_NA_data_frame)
    y_scrollbar_has_NA = ttk.Scrollbar(treevew_has_NA_data_frame, orient="vertical", command=tv_has_NA.yview)
    x_scrollbar_has_NA = ttk.Scrollbar(treevew_has_NA_data_frame, orient="horizontal", command=tv_has_NA.xview)

    #put frame on grid
    treevew_has_NA_data_frame.pack(side=LEFT)
    #put scroll bars
    tv_has_NA.configure(yscrollcommand=y_scrollbar_has_NA.set, xscrollcommand=x_scrollbar_has_NA.set)

    y_scrollbar_has_NA.pack(side=RIGHT, fill="y")
    x_scrollbar_has_NA.pack(side=BOTTOM, fill="x")

    # #show columns and list
    tv_has_NA["column"] = list(df_has_NA.columns)
    tv_has_NA["show"] = "headings"
    for column in tv_has_NA["column"]:
        tv_has_NA.heading(column, text = column)
        tv_has_NA.column(column, width=100, minwidth=100)

    df_has_NA_rows = df_has_NA.to_numpy().tolist()
    for row in df_has_NA_rows:
        tv_has_NA.insert("", "end", values= row)

    tv_has_NA.pack()

def encode_columns():
    def actually_encode_column(column):
        label_encoder = LabelEncoder()
        global df
        df[column] = label_encoder.fit_transform(df[column])

        messagebox.showinfo("Encoding Successful", "The data has been encodded successfully")

    #making window
    encode_columns_window = Toplevel(root, padx=30)
    encode_columns_window.title("Encoding Columns")
    encode_columns_window.geometry("400x500")

    #each column and a button to encode it
    Label(encode_columns_window, text ="Columns").grid(row=0, column=0)
    Label(encode_columns_window, text ="Encode it?").grid(row=0, column=1)
    Label(encode_columns_window, text ="Column has NA").grid(row=0, column=2)
    for i, column in enumerate(df.columns):
        column_has_NA = df[column].isna().any()
        Label(encode_columns_window, text = column).grid(row=i+1, column=0)
        Button(encode_columns_window, text= "encode",command= lambda: actually_encode_column(column)).grid(row=i+1, column=1)
        Label(encode_columns_window, text = column_has_NA).grid(row=i+1, column=2)
    
    #Update treeviews function
    def close_encoding_window():
        encode_columns_window.destroy()

        #delete old treeview and repack it
        for widgets in treevew_data_frame.winfo_children():
            widgets.destroy()
        #deletes old 
        for widgets in treevew_has_NA_data_frame.winfo_children():
            widgets.destroy()
        treeview_of_df()

    #Closing & Saving button
    Button(encode_columns_window, text= "Close & Save", command=close_encoding_window).grid(row=1010, column=1)

def transform_data():
    transoform_data_frame.pack(side=LEFT)

    #~~ What actions ~~#
    encode_column_button = Button(transoform_data_frame, text="Encode Column", command=encode_columns)
    encode_column_button.pack()


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
