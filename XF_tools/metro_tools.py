# imports packages and libraries
import os
import pandas as pd
from tkinter import Tk,filedialog
import xlrd
from sqlalchemy import create_engine

def absfilepath(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

# # Get data folder from user
# root = Tk()
# root.withdraw()
# cmm_files = filedialog.askdirectory(title='select the folder with cmm files')


def generate_cmm_result(data_file):
    df_cmm = pd.DataFrame()
    filename = os.path.basename(data_file)
    data_report = pd.read_excel(data_file, 'Report')

    meas_plan = data_report.iloc[3, 1]
    meas_date = data_report.iloc[3, 3]
    meas_time = data_report.iloc[6, 3]
    part_no = data_report.iloc[6, 5]

    headers = data_report.iloc[11].values
    df_report = pd.DataFrame(data_report.values[12:], columns=headers)
    df_report['Lot No'] = filename.split('_')[0]
    df_report['Cavity'] = filename.split('_')[1][7]
    df_report['Sample'] = filename.split('_')[2][7]
    df_report['Measurement Plan'] = meas_plan
    df_report['Part No'] = part_no
    df_report['Date'] = meas_date
    df_report['Time'] = meas_time
    df_report['File name'] = filename

    df_cmm = df_cmm.append(df_report, sort=True)

    return df_cmm
def process_cmm_file(data_files):
    print("Converting cmm result files")
    engine = create_engine('mysql+pymysql://agilent:agilent@supercomputer/metrology')

    df_sql_cmm = pd.read_sql('SELECT * FROM metrology.`mm strips`', con=engine)
    old_files = set(df_sql_cmm['File name'].unique())

    # select xlsx files
    files = absfilepath(data_files)
    files_xlsx = [f for f in files if f[-4:] == 'xlsx' or f[-3:] == 'xls' and os.path.basename(f) not in old_files]
    for data_file in files_xlsx:
        print(f'Processing {data_file} ...', )
        data_cmm = generate_cmm_result(data_file)
        data_cmm.to_sql('mm strips', con=engine, if_exists='append', index=False)

        print('completed')
    #delete xlsx files
    # shutil.rmtree(xlsx_files)

def delete_folder_contents (folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif the_file == "xlsx_output": shutil.rmtree(file_path)
        except Exception as e:
            print(e)



