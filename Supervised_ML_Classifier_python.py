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
from sklearn.impute import SimpleImputer

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
df_original = pd.DataFrame() # this df will not be transformed at all, it will keep original data
df = pd.DataFrame() #will ve reassigned in csv_opener() / this df will be transformed
x, y = 0,0

# I keep all frames here incase I want to delete them later
choose_csv_frame = LabelFrame(root, pady= 6, padx=15)
treevew_data_frame = LabelFrame(root, padx=40, text="Data Display")
treevew_has_NA_data_frame = LabelFrame(root, padx=40, text="Does Column have NA")
transoform_data_frame = LabelFrame(root, padx=20, text="Transform Data")
split_data_frame = LabelFrame(root, padx=20, text="Split Data")


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
    split_data()


def csv_opener():
    #choose CSV File
    csv_file_name = Label(choose_csv_frame ,text="No File Selected")
    choose_csv_frame.filename = filedialog.askopenfilename(initialdir="/C", title="Select CSV File", filetypes=(("CSV Files", "*.csv"),))
    csv_file_name["text"] = choose_csv_frame.filename
    global file_path
    file_path = csv_file_name["text"]
    print(file_path)

    #make df
    global df, df_original
    df = pd.read_csv(file_path)
    df_original = df

    #delete choose_csv_frame / Starts Actual Apps
    csv_submission_successful = messagebox.showinfo("Submission Successful", "The data has been submitted successfully")
    if csv_submission_successful == "ok":
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
    treevew_has_NA_data_frame.pack(side=LEFT, anchor=NW)
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

def close_whatever_transform_window(transform_window):
    transform_window.destroy()

    #delete old treeview and repack it
    for widgets in treevew_data_frame.winfo_children():
        widgets.destroy()
    #deletes old 
    for widgets in treevew_has_NA_data_frame.winfo_children():
        widgets.destroy()
    treeview_of_df()

def encode_columns():
    column_entry_get = StringVar()

    def actually_encode_column():
        column_to_encode = column_entry_get.get()
        label_encoder = LabelEncoder()
        global df
        df[column_to_encode] = label_encoder.fit_transform(df[column_to_encode])

        messagebox.showinfo("Encoding Successful", "The data has been encodded successfully")

    #making window
    encode_columns_window = Toplevel(root, padx=30)
    encode_columns_window.title("Encoding Columns")
    encode_columns_window.geometry("440x500")
    #make window behind this one unclickable
    encode_columns_window.grab_set()
    encode_columns_window.transient(root)

    Label(encode_columns_window, text= "Enter Column Name to Encode: ").grid(row=0, column=0)
    Entry(encode_columns_window, textvariable= column_entry_get).grid(row=0, column=1)
    Button(encode_columns_window, text= "encode", command= lambda: actually_encode_column()).grid(row=0, column=2)
    encode_columns_window

    #each column
    Label(encode_columns_window,bg="lightgray", text ="Columns").grid(row=1, column=0)
    Label(encode_columns_window,bg="lightgray", text ="Column has NA").grid(row=1, column=2)

    for i, column in enumerate(df.columns):
        column_has_NA = df[column].isna().any()
        Label(encode_columns_window, text = column).grid(row=i+2, column=0)
        Label(encode_columns_window, text = column_has_NA).grid(row=i+2, column=2)
    
    #Closing & Saving button
    Button(encode_columns_window, text= "Close & Save", command=lambda: close_whatever_transform_window(encode_columns_window)).grid(row=1010, column=1, columnspan=1)

def handle_NA():
    column_to_handle_na = StringVar()

    #check if any columns have NA
    if df.isnull().any().any() == False:
        messagebox.showinfo("No NA values found", "All columns don't contain any NA")
    #open window to handle NA values
    elif df.isnull().any().any() == True:
        handle_NA_window = Toplevel(root, padx=30)
        handle_NA_window.title("Handle NA")
        handle_NA_window.geometry("420x500")

        #make window behind this one unclickable
        handle_NA_window.grab_set()
        handle_NA_window.transient(root)

        #title at top
        title_label = Label(handle_NA_window, bg="gray", padx = 105, text = "Columns Containing NA")
        title_label.grid(row=0, column=0, columnspan=3)
        # Label(handle_NA_window, bg="lightgray", text ="How to Handle it?").grid(row=1, column=1, columnspan=2)
        Label(handle_NA_window, bg="lightgray", text ="Enter Column Name to Handle").grid(row=1, column=0)
        Entry(handle_NA_window, textvariable= column_to_handle_na).grid(row=1, column=1)

        Label(handle_NA_window, bg="lightgray", text ="Columns").grid(row=2, column=0)
        Label(handle_NA_window, bg="lightgray", text ="Choose How to Handle Column").grid(row=2, column=1)

        def replace_NA_with_mean():
            column_to_handle = column_to_handle_na.get()

            global df
            mean = df[column_to_handle].mean()
            df[column_to_handle].fillna(value=mean, inplace=True)
            messagebox.showinfo("Filling Successful", "NA cells have been filled with mean successfully in the column")
        def remove_NA_row():
            column_to_handle = column_to_handle_na.get()

            global df
            df.dropna(subset = [column_to_handle], inplace=True)
            messagebox.showinfo("Removal Successful", "The rows has been removed successfully")

        def replace_all_NA_with_imputer(strategy):
            global df
            removal_successful = messagebox.showinfo("Filling Successful", "NA cells have been filled successfully in all DataFrame")
            if removal_successful == "ok":
                    close_whatever_transform_window(handle_NA_window)
        def remove_all_NA_row():
            global df
            for column in df.columns:
                df.dropna(subset = [column], inplace=True)

            removal_successful =  messagebox.showinfo("Removal Successful", "The rows has been removed successfully in all DataFrame")
            if removal_successful == "ok":
                close_whatever_transform_window(handle_NA_window)

        count_skipped_list = [] #this list will be used to count how many times the loop was skipped (continue) so that the unskipped Labels print in the correct grid
        for i, column in enumerate(df.columns, start= 3):
            if df[column].isna().any() == False:
                count_skipped_list.append(1)
                continue
            else:
                Label(handle_NA_window, text = column).grid(row=i - len(count_skipped_list), column=0)

        Button(handle_NA_window, text= "Replace with Mean",command= lambda: replace_NA_with_mean()).grid(row=3, column=1)
        # Button(handle_NA_window, text= "Replace with Median",command= lambda: replace_NA_with_mean()).grid(row=3, column=1)
        Button(handle_NA_window, text= "Remove Entire Row",command= lambda: remove_NA_row()).grid(row=4, column=1)
        Label(handle_NA_window, text= "or").grid(row=5, column=1)
        Button(handle_NA_window, text= "Replace all NA with Mean",command= lambda: replace_all_NA_with_imputer("mean")).grid(row=6, column=1)
        Button(handle_NA_window, text= "Replace all NA with Median",command= lambda: replace_all_NA_with_imputer("median")).grid(row=7, column=1)
        Button(handle_NA_window, text= "Remove all NA rows Entirely",command= lambda: remove_all_NA_row()).grid(row=8, column=1)

        #Closing & Saving button
        Button(handle_NA_window, text= "Close & Save", command=lambda: close_whatever_transform_window(handle_NA_window)).grid(row=1010, column=1)    

def remove_column():
        column_entry_get = StringVar()
        def actually_remove_column():
            column_to_remove = column_entry_get.get()
            global df
            df = df.drop(column_to_remove, axis=1)

            messagebox.showinfo("Removal Successful", "The column has been removed successfully")
        def actually_remove_all_non_int_columns():
            global df
            for column in df.columns:
                if df[column].dtype == 'int64' or df[column].dtype == 'float64':
                    continue
                else:
                    df = df.drop(column, axis=1)
            removal_successful = messagebox.showinfo("Removal Successful", "All non float/int columns have been removed successfully")
            if removal_successful == "ok":
                    close_whatever_transform_window(remove_column_window)
        
        remove_column_window = Toplevel(root, padx=30)
        remove_column_window.title("Remove Column")
        remove_column_window.geometry("460x500")

        #make window behind this one unclickable
        remove_column_window.grab_set()
        remove_column_window.transient(root)

        Label(remove_column_window, text= "Enter Column Name to Remove: ").grid(row=0, column=0)
        Entry(remove_column_window, textvariable= column_entry_get).grid(row=0, column=1)
        Button(remove_column_window, text= "Remove Column", command= actually_remove_column).grid(row=0, column=2)

        #each column
        Label(remove_column_window,bg="lightgray", text ="Columns").grid(row=1, column=0)
        Label(remove_column_window,bg="lightgray", text ="Column dtype").grid(row=1, column=1)

        for i, column in enumerate(df.columns):
            column_dtype = df[column].dtype
            Label(remove_column_window, text = column).grid(row=i+2, column=0)
            Label(remove_column_window, text = column_dtype).grid(row=i+2, column=1)

        Label(remove_column_window,bg="lightgray", text ="or").grid(row=1, column=2)
        Button(remove_column_window, text= "Remove all non \n float/int columns", command= actually_remove_all_non_int_columns).grid(row=2, column=2)

        #Closing & Saving button
        Button(remove_column_window, text= "Close & Save", command=lambda: close_whatever_transform_window(remove_column_window)).grid(row=1010, column=1)   

def transform_data():
    transoform_data_frame.pack(side=LEFT, anchor=NW)

    #~~ What actions ~~#
    Button(transoform_data_frame, text="Handle NA", command=handle_NA).pack()
    Button(transoform_data_frame, text="Encode Column", command=encode_columns).pack()
    Button(transoform_data_frame, text="Remove Column", command=remove_column).pack()
    # Button(transoform_data_frame, text="Feature Scaling", command=feature_scaling).pack()
    # Button(transoform_data_frame, text="Encode Column", command=encode_columns).pack()

def split_data():
    split_data_frame.pack(side=RIGHT, anchor=NE)
    target_column_get = StringVar()
    
    def select_target():
        target_column = target_column_get.get()

        # y: target_column, x: all dependant columns
        global x, y
        x = df.drop([target_column], axis=1)
        y = df[target_column]
        csv_submission_successful = messagebox.showinfo("Data Selection Successful", "Target and Independant Variables have been selected successfully")
        if csv_submission_successful == "ok":
            ...

    Label(split_data_frame, text= "Input Target Column: ").grid(row=0, column=0)
    Entry(split_data_frame, textvariable= target_column_get).grid(row=0, column=1)
    Button(split_data_frame, text= "Confirm Target Selection",command= lambda: select_target()).grid(row=1, column=0, columnspan=1)

    # input target_column
    #label : "nope: all the other columns will be selected as the independent variables"




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
