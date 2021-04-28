import pandas as pd
import os

import subprocess
from sqlalchemy import create_engine
import shutil



def generate_from_file(data_file):
    df_rate = pd.DataFrame()
    df_raw = pd.DataFrame()
    df_cal = pd.DataFrame()

    filename = os.path.basename(data_file)
    assay_config = pd.read_excel(data_file, 'Assay Configuration')

    if "MR" in filename.upper():
        test_type = "Media Run"
    elif "LB" in filename.upper():
        test_type = "Long Baseline"
    elif "ST" in filename.upper():
        test_type = "Stress Test"
    elif "SB" in filename.upper():
        test_type = "Sort Baseline"
    elif "GAIN" in filename.upper():
        test_type = "GAIN"
    elif "KSV" in filename.upper():
        test_type = "KSV"
    elif "WETQC" in filename.upper():
        test_type = "WETQC"
    else:
        test_type = "Unknown"

    instrument = assay_config.iloc[25,1]
    instrument_number = assay_config.iloc[36, 1]

    if instrument[0] == "W":
        inst_type = 'XFe96'
    elif instrument[0] == "B":
        inst_type = 'XFe24'
    elif instrument[0] == "C" and instrument_number[:2] == '43':
        inst_type = 'XFp'
    elif instrument[0] == "C" and instrument_number[:4] == '0044':
        inst_type = 'HSmini'
    else:
        inst_type = 'Unknown'

    data_rate = pd.read_excel(data_file, 'Rate')
    data_rate['ECAR'] = data_rate['ECAR (mpH/min)'].round(decimals=2)
    data_rate['OCR'] = data_rate['OCR (pmol/min)'].round(decimals=2)
    data_rate['PER'] = data_rate['PER (pmol/min)'].round(decimals=2)
    data_rate['Test'] = test_type
    data_rate['Filename'] = filename
    data_rate["Instrument No"] = instrument_number
    data_rate["Cartridge Lot"] = assay_config.iloc[27, 1]
    data_rate["Cartridge Serial"] = assay_config.iloc[26, 1]
    data_rate["Software version"] = assay_config.columns[1]
    data_rate["Instrument Type"] = inst_type
    data_rate["datetime"] = assay_config.iloc[22, 1]
    data_rate["Date"] = pd.to_datetime(data_rate['datetime']).dt.date
    data_rate["Time"] = pd.to_datetime(data_rate['datetime']).dt.time

    data_raw = pd.read_excel(data_file, 'Raw')
    data_raw['Env. Temperature'] = data_raw['Manif. Temperature'].round(decimals=2)
    data_raw['Well Temperature'] = data_raw['Well Temperature'].round(decimals=2)
    data_raw['O2 (mmHg)'] = data_raw['O2 (mmHg)'].round(decimals=2)
    data_raw['O2 Corrected Em.'] = data_raw['O2 Corrected Em.'].round(decimals=2)
    data_raw['pH'] = data_raw['pH'].round(decimals=2)
    data_raw['pH Corrected Em.'] = data_raw['pH Corrected Em.'].round(decimals=2)
    data_raw['Filename'] = filename
    data_raw['Test'] = test_type
    data_raw["Instrument No"] = assay_config.iloc[36, 1]
    data_raw["Cartridge Lot"] = assay_config.iloc[27, 1]
    data_raw["Cartridge Serial"] = assay_config.iloc[26, 1]
    data_raw["Software version"] = assay_config.columns[1]
    data_raw["Instrument Type"] = inst_type
    data_raw["datetime"] = assay_config.iloc[22, 1]
    data_raw["Date"] = pd.to_datetime(data_raw['datetime']).dt.date
    data_raw["Time"] = pd.to_datetime(data_raw['datetime']).dt.time

    data_cal = pd.read_excel(data_file, 'Calibration')

    if inst_type == "XFe96":
        well = data_rate.iloc[0:96, 1]
        well = well.reset_index(drop=True)

        O2_LEDs = data_cal.iloc[6:14, 2:14].stack()
        O2_LEDs = O2_LEDs.reset_index(drop=True)
        O2_Emm = data_cal.iloc[15:23, 2:14].stack()
        O2_Emm = O2_Emm.reset_index(drop=True)
        O2_Ref = data_cal.iloc[33:41, 2:14].stack()
        O2_Ref = O2_Ref.reset_index(drop=True)

        pH_LEDs = data_cal.iloc[6:14, 16:28].stack()
        pH_LEDs = pH_LEDs.reset_index(drop=True)
        pH_Emm = data_cal.iloc[15:23, 16:28].stack()
        pH_Emm = pH_Emm.reset_index(drop=True)
        pH_Ref = data_cal.iloc[33:41, 16:28].stack()
        pH_Ref = pH_Ref.reset_index(drop=True)

    elif inst_type == "XFe24":
        well = data_rate.iloc[0:24, 1]
        well = well.reset_index(drop=True)

        O2_LEDs = data_cal.iloc[6:10, 2:8].stack()
        O2_LEDs = O2_LEDs.reset_index(drop=True)
        O2_Emm = data_cal.iloc[15:19, 2:8].stack()
        O2_Emm = O2_Emm.reset_index(drop=True)
        O2_Ref = data_cal.iloc[33:37, 2:8].stack()
        O2_Ref = O2_Ref.reset_index(drop=True)

        pH_LEDs = data_cal.iloc[6:10, 16:22].stack()
        pH_LEDs = pH_LEDs.reset_index(drop=True)
        pH_Emm = data_cal.iloc[15:19, 16:22].stack()
        pH_Emm = pH_Emm.reset_index(drop=True)
        pH_Ref = data_cal.iloc[33:37, 16:22].stack()
        pH_Ref = pH_Ref.reset_index(drop=True)

    elif inst_type == "XFp" or "HSmini":
        well = data_rate.iloc[0:8, 1]
        well = well.reset_index(drop=True)

        O2_LEDs = data_cal.iloc[6:14, 2]
        O2_LEDs = O2_LEDs.reset_index(drop=True)
        O2_Emm = data_cal.iloc[15:23, 2]
        O2_Emm = O2_Emm.reset_index(drop=True)
        O2_Ref = data_cal.iloc[33:41, 2]
        O2_Ref = O2_Ref.reset_index(drop=True)

        pH_LEDs = data_cal.iloc[6:14, 16]
        pH_LEDs = pH_LEDs.reset_index(drop=True)
        pH_Emm = data_cal.iloc[15:23, 16]
        pH_Emm = pH_Emm.reset_index(drop=True)
        pH_Ref = data_cal.iloc[33:41, 16]
        pH_Ref = pH_Ref.reset_index(drop=True)
    else:
        print("Instrument type is not defined")
    data_cal1 = pd.concat([well, O2_LEDs, O2_Emm, O2_Ref, pH_LEDs, pH_Emm, pH_Ref], axis=1)
    data_cal1.columns = ['Well', 'O2_LEDs', 'O2_Emm', 'O2_Ref', 'PH_LEDs', 'PH_Emm', 'PH_Ref']
    data_cal1['Filename'] = filename
    data_cal1['Test'] = test_type
    data_cal1["Instrument No"] = assay_config.iloc[36, 1]
    data_cal1["Cartridge Lot"] = assay_config.iloc[27, 1]
    data_cal1["Cartridge Serial"] = assay_config.iloc[26, 1]
    data_cal1["Software version"] = assay_config.columns[1]
    data_cal1["Instrument Type"] = inst_type
    data_cal1["datetime"] = assay_config.iloc[22, 1]
    data_cal1["Date"] = pd.to_datetime(data_cal1['datetime']).dt.date
    data_cal1["Time"] = pd.to_datetime(data_cal1['datetime']).dt.time

    df_rate = df_rate.append(data_rate, sort=True)
    df_raw = df_raw.append(data_raw, sort=True)
    df_cal = df_cal.append(data_cal1, sort=True)

    # droping extra columns
    df_rate = df_rate.drop(["datetime", "PER"], axis=1)
    df_raw = df_raw.drop(["datetime", "O2 is Valid", "pH Is Valid"], axis=1)
    df_cal = df_cal.drop(["datetime"], axis=1)

    return df_rate, df_raw, df_cal


def absfilepath(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def convert_asyr_file(asyr_files):
    print("Converting asyr to xlsx.")
    xlsx_files = os.path.join(asyr_files, 'xlsx_output')
    Asyr_to_xlsx = subprocess.check_output(
        ['C:\Program Files (x86)\Agilent Technologies\Wave Pro\MassAssayExporter.exe',
         asyr_files, xlsx_files, '-o'])

    # select xlsx files
    files = absfilepath(xlsx_files)
    rate = pd.DataFrame()
    raw = pd.DataFrame()
    cal = pd.DataFrame()

    for data_file in files:
        print(f'Processing {data_file} ...', )
        df_rate, df_raw, df_cal = generate_from_file(data_file)
        rate = rate.append(df_rate)
        raw = raw.append(df_raw)
        cal = cal.append(df_cal)

    return rate, raw, cal


def process_asyr_file(asyr_files):
    print("Converting asyr to xlsx.")
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

def delete_folder_contents (folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif the_file == "xlsx_output": shutil.rmtree(file_path)
        except Exception as e:
            print(e)