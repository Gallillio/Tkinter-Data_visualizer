# Tkinter-Data_visualizer
Simple Data Visualizer Using Tkinter Python.

<h3> What it will be: </h3>
  1) Will include Machine Learning featuers such as choosing a model to train the data or using Auto ML to auitomatically choose the best option
  2) Have more transform data options which include normalization, standardization, etc...
  3) Have Feature Engineering and Data Reduction using PCA
  4) Implement Data manipulation feature such as Filtering / Sorting / Joins & Merging
  5) (Maybe) Use a web framework such as Django or Flask or even Pyscript to make the app instead of Tkinter and make the frontend actually good instead of just usable like in its current state

<h3> ✨Milestones: </h3>
  1) Implement basic features that includes: EDA / Transforming Data / Seeing Interaction and Correlation between columns ✅
  2) Implement 1. Data Manipulation feature: Filtering / Sorting / Joins & Merging ❌
               2. Feature Engineering & Data Reduction
  3) Implement 1. Machine Learning featuers: splitting data & train - test model ❌
               2. Normalization / Standardization
  4) (Maybe) Use a web Framework instead of Tkinter ❌

<h3> What it currently is: </h3>
Use Tkinter GUI to import CSV file and do certain operations on it such as:
  1) Check of NaN values and handle them
  2) Encode Columns
  3) Remove Duplicates
  4) See Interaction between 2 columns
  5) See Correlation Heatmap
  6) Rename columns
  7) Remove Columns
  
![image](https://github.com/Gallillio/Tkinter-Data_visualizer/assets/117813417/ee180592-855f-42f4-bec1-e8c8616d335a)


You can also check detailed EDA on columns, this includes:
  1) Statistical Information such as: Minimum / Maximum / IQR / Mean / Median / Distinct Data & its percentage / Missing Data & its percentage / STD / Sum
     ![image](https://github.com/Gallillio/Tkinter-Data_visualizer/assets/117813417/535a4d5b-8684-4f3b-b02b-a5f6163d77a4)
  
  2) Histogram for numaric data with custom bin number or using freeman diaconis
    ![image](https://github.com/Gallillio/Tkinter-Data_visualizer/assets/117813417/0d6dc9a4-a636-46c9-8a2e-89f5c7bf691e)

  3) Stacked Bar for boolean data with percentage of each bool from total values
     ![image](https://github.com/Gallillio/Tkinter-Data_visualizer/assets/117813417/239ab2d6-ab9c-4e90-8b24-9415d061812b)
  
  4) Most Common Values
     ![image](https://github.com/Gallillio/Tkinter-Data_visualizer/assets/117813417/725871f6-af42-4bb1-8def-32e1822661fc)

  5) Extreme Values (Outliers)
     ![image](https://github.com/Gallillio/Tkinter-Data_visualizer/assets/117813417/828f6bfb-7253-44e4-876e-1d23dabe4573)