#imports packages and libraries
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import subprocess
from sqlalchemy import create_engine
from XF_tools.dataframe_generator import generate_from_file
import shutil

def absfilepath(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


# Get data folder from user
root = tk.Tk()
root.withdraw()
asyr_files = filedialog.askdirectory(title='select the folder with asyr files')
#xlsx_files = filedialog.askdirectory(title='select the folder to export in xlsx')
xlsx_files = os.path.join(asyr_files, 'xlsx_output')

# Export into Excel using MassAssayExporter
def process_asyr_file(asyr_files):
    xlsx_files = os.path.join(asyr_files, 'xlsx_output')
    Asyr_to_xlsx = subprocess.check_output(['C:\Program Files (x86)\Agilent Technologies\Wave Pro\MassAssayExporter.exe',
                                  asyr_files, xlsx_files, '-o'])

    #select xlsx files
    files = absfilepath(xlsx_files)
    engine = create_engine('mysql+pymysql://root:Quality123@localhost/instrumentqc')

    for data_file in files:
        print(f'Processing {data_file} ...',)
        df_rate, df_raw, df_cal = generate_from_file(data_file)
        df_rate.to_sql('iqc_rates', con=engine, if_exists='append', index=False)
        df_raw.to_sql('iqc_raw', con=engine, if_exists='append', index=False)
        df_cal.to_sql('iqc_cal', con=engine, if_exists='append', index=False)
        print('completed')

    #delete xlsx files
    shutil.rmtree(xlsx_files)

