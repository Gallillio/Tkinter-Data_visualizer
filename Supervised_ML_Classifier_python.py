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

#Feature Transformations
from sklearn.preprocessing import StandardScaler

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
x, y = None,None
x_train, x_test, y_train, y_test = None,None,None,None

# I keep all frames here incase I want to delete them later
choose_csv_frame = LabelFrame(root, pady= 6, padx=15)
treevew_data_frame = LabelFrame(root, padx=40, text="Data Display")
treevew_has_NA_data_frame = LabelFrame(root, padx=40, text="Does Column have NA")
transoform_data_frame = LabelFrame(root, padx=20, text="Transform Data")
split_data_frame = LabelFrame(root, padx=20, text="Split Data")
EDA_frame = LabelFrame(root, padx=20, text="EDA")


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
    root.geometry("1100x600+300+100")
    # root.resizable(False,False)

def root_loop() -> int:
    #start root loop
    root.mainloop()
    
    return 0

 #get file path

def run_code():
    choose_csv_frame.place_forget()
    treeview_of_df()
    EDA()
    transform_data()
    split_data()

def csv_opener():
    #choose CSV File
    csv_file_name = Label(choose_csv_frame ,text="No File Selected")
    choose_csv_frame.filename = filedialog.askopenfilename(initialdir="/C", title="Select CSV File", filetypes=(("CSV Files", "*.csv"),))
    csv_file_name["text"] = choose_csv_frame.filename
    global file_path
    file_path = csv_file_name["text"]

    #make df
    global df, df_original
    df = pd.read_csv(file_path)
    df_original = df

    #delete choose_csv_frame / Starts Actual Apps
    submission_successful = messagebox.showinfo("Submission Successful", "The data has been submitted successfully")
    if submission_successful == "ok":
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
        column_has_na_list = [column, df[column].isna().any(), df[column].isna().sum(), f"{round(df[column].isna().sum() * 100 / len(df[column]), 4)} %"]
        data.append(column_has_na_list)
        
    df_has_NA = pd.DataFrame(data, columns=["Column Name", "Column Has NA", "Count of NA Cells", "% of NA Cells"])

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

def detailed_EDA():    
    detailed_EDA_window = Toplevel(root, padx=30)
    detailed_EDA_window.title("Handle NA")
    detailed_EDA_window.geometry("470x500")

    detailed_EDA_frame = LabelFrame(detailed_EDA_window) #will be used in display_detailed_EDA()

    Label(detailed_EDA_window, bg="gray", padx = 105, text = "Detailed Column EDA").grid(row=0, column=0, columnspan=3)

    choices = []
    for i, column in enumerate(df.columns):
        choices.append(column)

    Label(detailed_EDA_window, text = "Choose Column to view more about").grid(row=1, column=0)
    column_combobox_get = ttk.Combobox(detailed_EDA_window, values= choices)
    column_combobox_get.grid(row=1, column=1)
    Button(detailed_EDA_window, text= "Display More", command= lambda: display_detailed_EDA(column_combobox_get.get())).grid(row=1, column=2)
    
    Label(detailed_EDA_window, text=" ").grid(row=2, column=0)
    def display_detailed_EDA(column):
        #delete frame and rebuild it (incase user changes column)
        for widgets in detailed_EDA_frame.winfo_children():
            widgets.destroy()
        detailed_EDA_frame.grid(row=3, column=0, columnspan=3)

        def statistics_detailed_EDA(column):
            Label(detailed_EDA_frame, text = "     ").grid(row=2, column=0)
            #min value
            Label(detailed_EDA_frame, text="Minimum: ").grid(row=3, column=0, columnspan=2)
            Label(detailed_EDA_frame, text= min(df[column])).grid(row=3, column=1, columnspan=2)
            #max value
            Label(detailed_EDA_frame, text="Maximum: ").grid(row=4, column=0, columnspan=2)
            Label(detailed_EDA_frame, text= max(df[column])).grid(row=4, column=1, columnspan=2)
            #distance value
            Label(detailed_EDA_frame, text="Distinct: ").grid(row=3, column=2, columnspan=2)
            Label(detailed_EDA_frame, text= len(pd.unique(df[column]))).grid(row=3, column=3, columnspan=2)
            #distance percentage
            Label(detailed_EDA_frame, text="Distinct (%): ").grid(row=4, column=2, columnspan=2)
            distinct_percentage = round((len(pd.unique(df[column])) / len(df[column])) * 100, 1)
            Label(detailed_EDA_frame, text= f"{distinct_percentage}%").grid(row=4, column=3, columnspan=2)
            #mean value
            Label(detailed_EDA_frame, text="Mean: ").grid(row=5, column=0, columnspan=2)
            Label(detailed_EDA_frame, text= round(df[column].mean(), 3)).grid(row=5, column=1, columnspan=2)
            #median value
            Label(detailed_EDA_frame, text="Median: ").grid(row=6, column=0, columnspan=2)
            Label(detailed_EDA_frame, text= round(df[column].median(), 3)).grid(row=6, column=1, columnspan=2)
            #missing value
            Label(detailed_EDA_frame, text="Missing: ").grid(row=5, column=2, columnspan=2)
            Label(detailed_EDA_frame, text= df[column].isna().sum()).grid(row=5, column=3, columnspan=2)
            #missing percentage
            Label(detailed_EDA_frame, text="Missing(%): ").grid(row=6, column=2, columnspan=2)
            missing_percentage = round((df[column].isna().sum() / len(df[column])) * 100, 1)
            Label(detailed_EDA_frame, text= f"{missing_percentage}%").grid(row=6, column=3, columnspan=2)
            #sum value
            Label(detailed_EDA_frame, text="Sum: ").grid(row=7, column=0, columnspan=2)
            Label(detailed_EDA_frame, text= round(df[column].sum(), 3)).grid(row=7, column=1, columnspan=2)
            #standard diviation value
            Label(detailed_EDA_frame, text="STD: ").grid(row=7, column=2, columnspan=2)
            Label(detailed_EDA_frame, text= round(df[column].std(), 3)).grid(row=7, column=3, columnspan=2)



        #build statistics_detailed_EDA() automatically
        statistics_detailed_EDA(column)

        Label(detailed_EDA_frame, bg="lightgray", text= column, padx=105).grid(row=0, column=0, columnspan=4)
        Button(detailed_EDA_frame, text="Statistics", command=lambda: statistics_detailed_EDA(column)).grid(row=1, column=0)
        Button(detailed_EDA_frame, text="Histogram").grid(row=1, column=1)
        Button(detailed_EDA_frame, text="Common Values").grid(row=1, column=2)
        Button(detailed_EDA_frame, text="Extreme Values").grid(row=1, column=3)


def EDA():
    EDA_frame.pack(side=TOP, anchor=NW)
    empty_space_label = Label(EDA_frame, text = "     ")

    #check if column is categorical or numaric or bool
    column_is_categorical = []
    column_is_numaric = []
    column_is_bool = []
    for column in df.columns:
        #check if bool                                                     this checks if the unique() outcome is actually 0 & 1 or if it this column just happens to contain only 2 unique rows that could be not a bool
        if df[column].dtype == np.dtype('bool') or (len(df[column].unique()) == 2 and (1 in df[column].unique() and 0 in df[column].unique()) ):
            column_is_bool.append(column)
        #check if object
        elif df[column].dtype == np.dtype('O'):
            column_is_categorical.append(column)
        #check if float or int
        elif df[column].dtype == np.dtype('float64') or df[column].dtype == np.dtype('int64') or df[column].dtype == np.dtype('float32') or df[column].dtype == np.dtype('int32'):
            column_is_numaric.append(column)

    Label(EDA_frame, text = f"Number of Features: {len(df.columns)}").grid(row=0, column=0)
    Label(EDA_frame, text = f"Number of Rows: {len(df)}").grid(row=1, column=0)
    Label(EDA_frame, text = f"Number of Missing Cells: {df.isnull().sum().sum()}").grid(row=2, column=0)
    Button(EDA_frame, text="More Detailed EDA", command=detailed_EDA).grid(row=3, column=0, columnspan=3)
    empty_space_label.grid(row=0, column=1)
    Label(EDA_frame, text = f"Number of Numaric Columns: {len(column_is_numaric)}").grid(row=0, column=2)
    Label(EDA_frame, text = f"Number of Boolean Columns: {len(column_is_bool)}").grid(row=1, column=2)
    Label(EDA_frame, text = f"Number of Categorical Columns: {len(column_is_categorical)}").grid(row=2, column=2)

def close_whatever_transform_window(transform_window):
    transform_window.destroy()

    #delete old treeview and repack it
    for widgets in treevew_data_frame.winfo_children():
        widgets.destroy()
    #deletes old 
    for widgets in treevew_has_NA_data_frame.winfo_children():
        widgets.destroy()
    treeview_of_df()

def handle_NA():
    #check if any columns have NA
    if df.isnull().any().any() == False:
        messagebox.showinfo("No NA values found", "All columns don't contain any NA")
    #open window to handle NA values
    elif df.isnull().any().any() == True:
        handle_NA_window = Toplevel(root, padx=30)
        handle_NA_window.title("Handle NA")
        handle_NA_window.geometry("420x500")

        # #make window behind this one unclickable
        # handle_NA_window.grab_set()
        # handle_NA_window.transient(root)

        #title at top
        title_label = Label(handle_NA_window, bg="gray", padx = 105, text = "Columns Containing NA")
        title_label.grid(row=0, column=0, columnspan=3)
        
        choices = []
        for column in df.columns:
            if df[column].isna().any() == False:
                continue
            else:
                choices.append(column)

        Label(handle_NA_window, bg="lightgray", text ="Choose Column Name to Handle").grid(row=1, column=0)
        column_to_handle_na = ttk.Combobox(handle_NA_window, values= choices)
        column_to_handle_na.grid(row=1, column=1)

        Label(handle_NA_window, bg="lightgray", text ="Choose How to Handle Column").grid(row=2, column=0, columnspan=2)

        def replace_NA_with_mean():
            column_to_handle = column_to_handle_na.get()

            global df
            mean = df[column_to_handle].mean()
            df[column_to_handle].fillna(value=mean, inplace=True)
            messagebox.showinfo("Filling Successful", "NA cells have been filled with mean successfully in the column")
        def replace_NA_with_median():
            column_to_handle = column_to_handle_na.get()

            global df
            median = df[column_to_handle].median()
            df[column_to_handle].fillna(value=median, inplace=True)
            messagebox.showinfo("Filling Successful", "NA cells have been filled with median successfully in the column")
        def remove_NA_row():
            column_to_handle = column_to_handle_na.get()

            global df
            df.dropna(subset = [column_to_handle], inplace=True)
            messagebox.showinfo("Removal Successful", "The rows has been removed successfully")

        def replace_all_NA_with_imputer(strategy):
            global df
            removal_successful = messagebox.showinfo("Filling Successful", f"NA cells have been filled with {strategy} successfully in all DataFrame")
            if removal_successful == "ok":
                    close_whatever_transform_window(handle_NA_window)
        def remove_all_NA_row():
            global df
            for column in df.columns:
                df.dropna(subset = [column], inplace=True)

            removal_successful =  messagebox.showinfo("Removal Successful", "The rows has been removed successfully in all DataFrame")
            if removal_successful == "ok":
                close_whatever_transform_window(handle_NA_window)

        Button(handle_NA_window, text= "Replace with Mean",command= lambda: replace_NA_with_mean()).grid(row=3, column=0, columnspan=2)
        # Button(handle_NA_window, text= "Replace with Median",command= lambda: replace_NA_with_mean()).grid(row=3, column=1)
        Button(handle_NA_window, text= "Remove Entire Row",command= lambda: remove_NA_row()).grid(row=4, column=0, columnspan=2)
        Label(handle_NA_window, text= "or").grid(row=5, column=0, columnspan=2)
        Button(handle_NA_window, text= "Replace all NA with Mean",command= lambda: replace_all_NA_with_imputer("mean")).grid(row=6, column=0, columnspan=2)
        Button(handle_NA_window, text= "Replace all NA with Median",command= lambda: replace_all_NA_with_imputer("median")).grid(row=7, column=0, columnspan=2)
        Button(handle_NA_window, text= "Remove all NA rows Entirely",command= lambda: remove_all_NA_row()).grid(row=8, column=0, columnspan=2)

        #Closing & Saving button
        Label(handle_NA_window, text= " ").grid(row=1009, column=0)
        Button(handle_NA_window, text= "Close & Save", command=lambda: close_whatever_transform_window(handle_NA_window)).grid(row=1010, column=0, columnspan=2)    

def encode_columns():
    def actually_encode_column():
        column_to_encode = column_combobox_get.get()
        label_encoder = LabelEncoder()
        global df
        df[column_to_encode] = label_encoder.fit_transform(df[column_to_encode])

        messagebox.showinfo("Encoding Successful", "The data has been encodded successfully")

    #making window
    encode_columns_window = Toplevel(root, padx=30)
    encode_columns_window.title("Encoding Columns")
    encode_columns_window.geometry("440x500")
    # #make window behind this one unclickable
    # encode_columns_window.grab_set()
    # encode_columns_window.transient(root)

    choices = []
    for i, column in enumerate(df.columns):
        choices.append(column)
        column_has_NA = df[column].isna().any()
        Label(encode_columns_window, text = column).grid(row=i+2, column=0)
        Label(encode_columns_window, text = column_has_NA).grid(row=i+2, column=2)

    Label(encode_columns_window, text= "Enter Column Name to Encode: ").grid(row=0, column=0)
    column_combobox_get = ttk.Combobox(encode_columns_window, values= choices)
    column_combobox_get.grid(row=0, column=1)
    Button(encode_columns_window, text= "encode", command= lambda: actually_encode_column()).grid(row=0, column=2)

    #each column
    Label(encode_columns_window,bg="lightgray", text ="Columns").grid(row=1, column=0)
    Label(encode_columns_window,bg="lightgray", text ="Column has NA").grid(row=1, column=2)
    
    #Closing & Saving button
    Button(encode_columns_window, text= "Close & Save", command=lambda: close_whatever_transform_window(encode_columns_window)).grid(row=1010, column=1, columnspan=1)

def remove_column():
        def actually_remove_column():
            column_to_remove = column_combobox_get.get()
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

        # #make window behind this one unclickable
        # remove_column_window.grab_set()
        # remove_column_window.transient(root)

        choices = []
        for i, column in enumerate(df.columns):
            choices.append(column)
            column_dtype = df[column].dtype
            Label(remove_column_window, text = column).grid(row=i+2, column=0)
            Label(remove_column_window, text = column_dtype).grid(row=i+2, column=1)

        Label(remove_column_window, text= "Enter Column Name to Remove: ").grid(row=0, column=0)
        column_combobox_get = ttk.Combobox(remove_column_window, values= choices)
        column_combobox_get.grid(row=0, column=1)
        Button(remove_column_window, text= "Remove Column", command= actually_remove_column).grid(row=0, column=2)

        #each column
        Label(remove_column_window,bg="lightgray", text ="Columns").grid(row=1, column=0)
        Label(remove_column_window,bg="lightgray", text ="Column dtype").grid(row=1, column=1)

        Label(remove_column_window,bg="lightgray", text ="or").grid(row=1, column=2)
        Button(remove_column_window, text= "Remove all non \n float/int columns", command= actually_remove_all_non_int_columns).grid(row=2, column=2)

        #Closing & Saving button
        Button(remove_column_window, text= "Close & Save", command=lambda: close_whatever_transform_window(remove_column_window)).grid(row=1010, column=1)   

def rename_column():
    new_column_name_get = StringVar()
    
    #making window
    rename_column_window = Toplevel(root, padx=30)
    rename_column_window.title("Rename Column")
    rename_column_window.geometry("430x500")

    def actually_rename_column():
        new_column_name = new_column_name_get.get()
        column_to_rename = column_combobox_get.get()
        global df
        df.rename(columns = {f'{column_to_rename}':f'{new_column_name}'}, inplace = True)

        removal_successful = messagebox.showinfo("Removed Duplicates Successful", "The duplicated data has been removed successfully")
        if removal_successful == "ok":
            # close_whatever_transform_window(remove_duplicates_window)
            rename_column_window.destroy()
            rename_column()
    def save_and_close():
        close_whatever_transform_window(rename_column_window)

    choices = []
    for i, column in enumerate(df.columns):
        choices.append(column)
    Label(rename_column_window, text= "Choose Column to Rename: ").grid(row=0, column=0)
    Label(rename_column_window, text= "Rename Column to: ").grid(row=1, column=0)
    column_combobox_get = ttk.Combobox(rename_column_window, values= choices)
    column_combobox_get.grid(row=0, column=1)
    Entry(rename_column_window, textvariable= new_column_name_get).grid(row=1, column=1)

    Button(rename_column_window, text= "Rename Column", command= actually_rename_column).grid(row=2, column=0, columnspan=2)
    Button(rename_column_window, text= "Save & Close", command= save_and_close).grid(row=3, column=0, columnspan=2)

def rename_column():
    new_column_name_get = StringVar()
    
    #making window
    rename_column_window = Toplevel(root, padx=30)
    rename_column_window.title("Rename Column")
    rename_column_window.geometry("430x500")

    def actually_rename_column():
        new_column_name = new_column_name_get.get()
        column_to_rename = column_combobox_get.get()
        global df
        df.rename(columns = {f'{column_to_rename}':f'{new_column_name}'}, inplace = True)

        removal_successful = messagebox.showinfo("Removed Duplicates Successful", "The duplicated data has been removed successfully")
        if removal_successful == "ok":
            # close_whatever_transform_window(remove_duplicates_window)
            rename_column_window.destroy()
            rename_column()
    def save_and_close():
        close_whatever_transform_window(rename_column_window)

    choices = []
    for i, column in enumerate(df.columns):
        choices.append(column)
    Label(rename_column_window, text= "Choose Column to Rename: ").grid(row=0, column=0)
    Label(rename_column_window, text= "Rename Column to: ").grid(row=1, column=0)
    column_combobox_get = ttk.Combobox(rename_column_window, values= choices)
    column_combobox_get.grid(row=0, column=1)
    Entry(rename_column_window, textvariable= new_column_name_get).grid(row=1, column=1)

    Button(rename_column_window, text= "Rename Column", command= actually_rename_column).grid(row=2, column=0, columnspan=2)
    Button(rename_column_window, text= "Save & Close", command= save_and_close).grid(row=3, column=0, columnspan=2)

def remove_duplicates():
    #making window
    remove_duplicates_window = Toplevel(root, padx=30)
    remove_duplicates_window.title("Remove Duplicates")
    remove_duplicates_window.geometry("450x500")
    def actually_remove_duplicates():
        column_entry = column_combobox_get.get()
        global df
        df = df.drop_duplicates(subset=[column_entry])

        removal_successful = messagebox.showinfo("Removed Duplicates Successful", "The duplicated data has been removed successfully")
        if removal_successful == "ok":
            close_whatever_transform_window(remove_duplicates_window)
    choices = []
    for i, column in enumerate(df.columns):
        choices.append(column)
        Label(remove_duplicates_window, text = column).grid(row=i+2, column=0, columnspan=2)

    Label(remove_duplicates_window, text= "Enter Column to Remove Duplicates From: ").grid(row=0, column=0)
    column_combobox_get = ttk.Combobox(remove_duplicates_window, values= choices)
    column_combobox_get.grid(row=0, column=1)
    Label(remove_duplicates_window, bg="lightgray", text= "Columns: ").grid(row=1, column=0, columnspan=2)
    Button(remove_duplicates_window, text= "Remove", command= lambda: actually_remove_duplicates()).grid(row=1, column=1)
    Label(remove_duplicates_window, text= "").grid(row=2, column=1)
    Button(remove_duplicates_window, text= "Create Index Column", command= lambda: create_index_column(remove_duplicates_window)).grid(row=3, column=1)
    Button(remove_duplicates_window, text= "Rename Column", command= lambda: actually_remove_duplicates()).grid(row=1, column=1)
    Button(remove_duplicates_window, text= "Rename Column", command= lambda: actually_remove_duplicates()).grid(row=1, column=1)

def create_index_column(remove_duplicates_window):
    #create index column
    global df
    if "index" in df.columns:
        messagebox.showerror("Index already exists", "A column with the name 'index' already exists, please rename that column and try again")
    else:
        df["index"] = df.index
        #rearrange columns and put index column first
        new_order = ['index']
        for column in df.columns[:-1]:
            new_order.append(column)
        df = df[new_order]

        removal_successful = messagebox.showinfo("Column Created Successfully", "Index Column has been created successfully")
        if removal_successful == "ok":
                #delete old treeview and repack it
                for widgets in treevew_data_frame.winfo_children():
                    widgets.destroy()
                #deletes old 
                for widgets in treevew_has_NA_data_frame.winfo_children():
                    widgets.destroy()
                treeview_of_df()
        
    # incase this function is run inside remove_duplicates(), have to delete remove_duplicates_window and create it again
    remove_duplicates_window.destroy()
    remove_duplicates()

def transform_data():
    transoform_data_frame.pack(side=LEFT, anchor=NW)

    #~~ What actions ~~#
    Button(transoform_data_frame, text="Handle NA", command=handle_NA).pack()
    Button(transoform_data_frame, text="Encode Column", command=encode_columns).pack()
    Button(transoform_data_frame, text="Remove Column", command=remove_column).pack()
    Button(transoform_data_frame, text="Rename Column", command=rename_column).pack()
    Button(transoform_data_frame, text="Rename Column", command=rename_column).pack()
    Button(transoform_data_frame, text="Remove Duplicates", command=remove_duplicates).pack()
    Button(transoform_data_frame, text="Create Index Column", command=lambda: create_index_column(None)).pack()

def standard_scaler():
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test) #using same mean used in scaling x_train

def split_data():
    split_data_frame.pack(side=TOP, anchor=NW)
    target_column_get = StringVar()
    train_size_get = StringVar()
    
    def select_target():
        target_column = target_column_get.get()

        # y: target_column, x: all dependant columns
        global x, y
        x = df.drop([target_column], axis=1)
        y = df[target_column]
        submission_successful = messagebox.showinfo("Data Selection Successful", "Target and Independant Variables have been selected successfully")
        if submission_successful == "ok":
            #reset split_data_frame
            # for widgets in split_data_frame.winfo_children():
            #     widgets.destroy()
            # split_data()
            #show current Target Value
            Label(split_data_frame, text= "Selected Target Column: ").grid(row=3, column=0)
            Label(split_data_frame, text= target_column).grid(row=3, column=1)
            
            #add x_train, x_test, y_train, y_test Labels
            def actually_split_data():
                train_size = float(train_size_get.get())
                #checks if train_size is between 0 -1, if not send an error
                if 0 <= train_size <= 1:
                    global x_train, x_test, y_train, y_test
                    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=train_size)
                    submission_successful = messagebox.showinfo("Data Split Sucecessfully", "(x_train, x_test, y_train, y_test) have been created created successfully")
                    if submission_successful == "ok":
                        Label(transoform_data_frame).pack()
                        Label(transoform_data_frame, bg="gray", text="Feature Transformation Methods").pack()
                        Button(transoform_data_frame, text="Standard Scaler", command=standard_scaler).pack()
                else:
                    pass
            
            Label(split_data_frame, text= "\n").grid(row=4, column=0)
            Label(split_data_frame, bg="gray", text= "Splitting Data").grid(row=5, column=0, columnspan=2)
            Label(split_data_frame, text= "train size(0-1): ").grid(row=6, column=0)
            Entry(split_data_frame, textvariable= train_size_get).grid(row=6, column=1)
            Button(split_data_frame, text= "Confirm train size & Split Data",command= lambda: actually_split_data()).grid(row=7, column=0, columnspan=2)           

    Label(split_data_frame, bg="gray", text= "Target & Independant Selection").grid(row=0, column=0, columnspan=2)
    Label(split_data_frame, text= "Input Target Column: ").grid(row=1, column=0)
    Entry(split_data_frame, textvariable= target_column_get).grid(row=1, column=1)
    Button(split_data_frame, text= "Confirm Target Selection",command= lambda: select_target()).grid(row=2, column=0, columnspan=2)





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
