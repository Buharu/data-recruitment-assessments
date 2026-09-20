import pandas as pd
from pathlib import Path

# read_file is a function that helps to read the csv files
# the function has only 1 parameter: file_path
# the output of the funcion is a DataFrame
def read_file(file_path):
    df = pd.read_csv(file_path)
    return df

# real_all_files is the function that helps me to read all the csv files from a folder
# the parameter of the function is the folder path
# the output of the function is a dictonari collection of DataFrames
def read_all_files(folder_path):
    folder = Path(folder_path)
    files = folder.rglob("*.csv")
    dfs = {}

    for file in files:
        name = f"df_{file.stem}"
        dfs[name] = read_file(file)

    return dfs
