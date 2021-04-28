import os
import pandas as pd
import numpy as np
# import tkinter as tk
# from tkinter import filedialog
import subprocess
# import shutil
# import xlrd
# from dataframe_generator import *
from XF_tools import dataframe_generator

def convert_asyr_file(asyr_files):
    #convert .xflr to .asyr
    with os.scandir(asyr_files) as it:
        for entry in it:
            if entry.name.endswith(".xflr") and entry.is_file():
                print("Converting xflr to asyr")
                pre, ext = os.path.splitext(entry)
                os.rename(entry, pre + ".asyr")
    #convert .asyr to .xlsx
    print("Converting asyr to xlsx.")
    xlsx_files = os.path.join(asyr_files, 'xlsx_output')
    Asyr_to_xlsx = subprocess.check_output(
        ['C:\Program Files (x86)\Agilent Technologies\Wave Pro\MassAssayExporter.exe',
         asyr_files, xlsx_files, '-o'])

    # select xlsx files
    files = dataframe_generator.absfilepath(xlsx_files)
    rate = pd.DataFrame()
    raw = pd.DataFrame()
    cal = pd.DataFrame()

    for data_file in files:
        print(f'Processing {data_file} ...', )
        df_rate, df_raw, df_cal = dataframe_generator.generate_from_file(data_file)
        rate = rate.append(df_rate)
        raw = raw.append(df_raw)
        cal = cal.append(df_cal)

    return rate, raw, cal

def IQC_auto_analyze(df_rate, df_raw, df_cal):

    # subset df based on type of run
    MR_rate = df_rate.loc[df_rate["Test"] == "Media Run"]
    LB_rate = df_rate.loc[df_rate["Test"] == "Long Baseline"]
    ST_rate = df_rate.loc[df_rate["Test"] == "Stress Test"]
    MR_raw = df_raw.loc[df_raw["Test"] == "Media Run"]
    LB_raw = df_raw.loc[df_raw["Test"] == "Long Baseline"]
    ST_raw = df_raw.loc[df_raw["Test"] == "Stress Test"]
    MR_cal = df_cal.loc[df_cal["Test"] == "Media Run"]
    LB_cal = df_cal.loc[df_cal["Test"] == "Long Baseline"]
    ST_cal = df_cal.loc[df_cal["Test"] == "Stress Test"]

    # media run calibration
    mr_avg_o2_led = round(MR_cal["O2_LEDs"].mean(), 2)
    mr_avg_ph_led = round(MR_cal["PH_LEDs"].mean(), 2)
    mr_avg_o2_ref = round(MR_cal["O2_Ref"].mean(), 2)
    mr_avg_ph_ref = round(MR_cal["PH_Ref"].mean(), 2)
    mr_min_o2_led = MR_cal["O2_LEDs"].min()
    mr_min_ph_led = MR_cal["PH_LEDs"].min()
    mr_min_o2_ref = MR_cal["O2_Ref"].min()
    mr_min_ph_ref = MR_cal["PH_Ref"].min()
    mr_max_o2_led = MR_cal["O2_LEDs"].max()
    mr_max_ph_led = MR_cal["PH_LEDs"].max()
    mr_max_o2_ref = MR_cal["O2_Ref"].max()
    mr_max_ph_ref = MR_cal["PH_Ref"].max()
    mr_o2_led_outliers = MR_cal.loc[(MR_cal["O2_LEDs"] < 1000) | (MR_cal["O2_LEDs"] > 30000) | (
                MR_cal["O2_LEDs"] > (2 * mr_avg_o2_led)), "Well"].unique()
    mr_o2_ref_outliers = MR_cal.loc[MR_cal["O2_Ref"] > (2 * mr_avg_o2_ref), "Well"].unique()
    mr_ph_led_outliers = MR_cal.loc[(MR_cal["PH_LEDs"] < 1000) | (MR_cal["PH_LEDs"] > 30000) | (
                MR_cal["PH_LEDs"] > (2 * mr_avg_ph_led)), "Well"].unique()
    mr_ph_ref_outliers = MR_cal.loc[MR_cal["PH_Ref"] > (2 * mr_avg_ph_ref), "Well"].unique()

    # Long Baseline calibration
    lb_avg_o2_led = round(LB_cal["O2_LEDs"].mean(), 2)
    lb_avg_ph_led = round(LB_cal["PH_LEDs"].mean(), 2)
    lb_avg_o2_ref = round(LB_cal["O2_Ref"].mean(), 2)
    lb_avg_ph_ref = round(LB_cal["PH_Ref"].mean(), 2)
    lb_min_o2_led = LB_cal["O2_LEDs"].min()
    lb_min_ph_led = LB_cal["PH_LEDs"].min()
    lb_min_o2_ref = LB_cal["O2_Ref"].min()
    lb_min_ph_ref = LB_cal["PH_Ref"].min()
    lb_max_o2_led = LB_cal["O2_LEDs"].max()
    lb_max_ph_led = LB_cal["PH_LEDs"].max()
    lb_max_o2_ref = LB_cal["O2_Ref"].max()
    lb_max_ph_ref = LB_cal["PH_Ref"].max()
    lb_o2_led_outliers = LB_cal.loc[(LB_cal["O2_LEDs"] < 1000) | (LB_cal["O2_LEDs"] > 30000) | (
                LB_cal["O2_LEDs"] > (2 * lb_avg_o2_led)), "Well"].unique()
    lb_o2_ref_outliers = LB_cal.loc[LB_cal["O2_Ref"] > (2 * lb_avg_o2_ref), "Well"].unique()
    lb_ph_led_outliers = LB_cal.loc[(LB_cal["PH_LEDs"] < 1000) | (LB_cal["PH_LEDs"] > 30000) | (
                LB_cal["PH_LEDs"] > (2 * lb_avg_ph_led)), "Well"].unique()
    lb_ph_ref_outliers = LB_cal.loc[LB_cal["PH_Ref"] > (2 * lb_avg_ph_ref), "Well"].unique()

    # Stress Test calibration
    st_avg_o2_led = round(ST_cal["O2_LEDs"].mean(), 2)
    st_avg_ph_led = round(ST_cal["PH_LEDs"].mean(), 2)
    st_avg_o2_ref = round(ST_cal["O2_Ref"].mean(), 2)
    st_avg_ph_ref = round(ST_cal["PH_Ref"].mean(), 2)
    st_min_o2_led = ST_cal["O2_LEDs"].min()
    st_min_ph_led = ST_cal["PH_LEDs"].min()
    st_min_o2_ref = ST_cal["O2_Ref"].min()
    st_min_ph_ref = ST_cal["PH_Ref"].min()
    st_max_o2_led = ST_cal["O2_LEDs"].max()
    st_max_ph_led = ST_cal["PH_LEDs"].max()
    st_max_o2_ref = ST_cal["O2_Ref"].max()
    st_max_ph_ref = ST_cal["PH_Ref"].max()
    st_o2_led_outliers = ST_cal.loc[(ST_cal["O2_LEDs"] < 1000) | (ST_cal["O2_LEDs"] > 30000) | (
                ST_cal["O2_LEDs"] > (2 * st_avg_o2_led)), "Well"].unique()
    st_o2_ref_outliers = ST_cal.loc[ST_cal["O2_Ref"] > (2 * st_avg_o2_ref), "Well"].unique()
    st_ph_led_outliers = ST_cal.loc[(ST_cal["PH_LEDs"] < 1000) | (ST_cal["PH_LEDs"] > 30000) | (
                ST_cal["PH_LEDs"] > (2 * st_avg_ph_led)), "Well"].unique()
    st_ph_ref_outliers = ST_cal.loc[ST_cal["PH_Ref"] > (2 * st_avg_ph_ref), "Well"].unique()

    # Media run- rate analysis
    mr_ocr_outliers = MR_rate.loc[(MR_rate["OCR"] < -20) | (MR_rate["OCR"] > 20), "Well"].unique()
    mr_min_ocr = MR_rate.loc[
        MR_rate["Measurement"] == 3 & (MR_rate["OCR"] >= -20) & (MR_rate["OCR"] <= 20), "OCR"].min()
    mr_max_ocr = MR_rate.loc[
        MR_rate["Measurement"] == 3 & (MR_rate["OCR"] >= -20) & (MR_rate["OCR"] <= 20), "OCR"].max()
    mr_ocr_range = (mr_min_ocr, mr_max_ocr)
    mr_ecar_outliers = MR_rate.loc[(MR_rate["ECAR"] < -5) | (MR_rate["ECAR"] > 5), "Well"].unique()
    mr_ecar_min = MR_rate.loc[
        MR_rate["Measurement"] == 3 & (MR_rate["ECAR"] >= -5) & (MR_rate["ECAR"] <= 5), "ECAR"].min()
    mr_ecar_max = MR_rate.loc[
        MR_rate["Measurement"] == 3 & (MR_rate["ECAR"] >= -5) & (MR_rate["ECAR"] <= 5), "ECAR"].max()
    mr_ecar_range = (mr_ecar_min, mr_ecar_max)

    # Long Baseline- rate analysis

    lb_rate = LB_rate.loc[LB_rate["Group"] != "Background"]
    lb_ocr_outliers = lb_rate.loc[(lb_rate["OCR"] < 50) | (lb_rate["OCR"] > 300), "Well"].unique()
    lb_mean_ocr = round(lb_rate.loc[lb_rate["Measurement"] == 3, "OCR"].mean(), 2)
    lb_std_ocr = round(lb_rate.loc[lb_rate["Measurement"] == 3, "OCR"].std(), 2)
    lb_cv_ocr = round(lb_std_ocr / lb_mean_ocr * 100, 2)
    lb_ecar_outliers = lb_rate.loc[(lb_rate["ECAR"] < 10) | (lb_rate["ECAR"] > 70), "Well"].unique()
    lb_mean_ecar = round(lb_rate.loc[lb_rate["Measurement"] == 3, "ECAR"].mean(), 2)
    lb_std_ecar = round(lb_rate.loc[lb_rate["Measurement"] == 3, "ECAR"].std(), 2)
    lb_cv_ecar = round(lb_std_ecar / lb_mean_ecar * 100, 2)

    # Stress test- rate analysis
    st_rate = ST_rate.loc[ST_rate["Group"] != "Background"]
    st_ocr_outliers = st_rate.loc[
        st_rate["Measurement"] <= 3 & (st_rate["OCR"] < 50) | (st_rate["OCR"] > 300), "Well"].unique()
    st_mean_ocr = round(st_rate.loc[st_rate["Measurement"] == 3, "OCR"].mean(), 2)
    st_std_ocr = round(st_rate.loc[st_rate["Measurement"] == 3, "OCR"].std(), 2)
    st_cv_ocr = round(st_std_ocr / st_mean_ocr * 100, 2)
    st_ecar_outliers = st_rate.loc[
        st_rate["Measurement"] <= 3 & (st_rate["ECAR"] < 10) | (st_rate["ECAR"] > 70), "Well"].unique()
    st_mean_ecar = round(st_rate.loc[st_rate["Measurement"] == 3, "ECAR"].mean(), 2)
    st_std_ecar = round(st_rate.loc[st_rate["Measurement"] == 3, "ECAR"].std(), 2)
    st_cv_ecar = round(st_std_ecar / st_mean_ecar * 100, 2)

    # Media run- level data analysis

    # subsetting df for starting level (tick 0)
    MR_raw_tick0 = MR_raw.loc[MR_raw["Tick"] == 0]

    # o2 analysis
    mr_o2_outliers = MR_raw_tick0.loc[
        (MR_raw_tick0["O2 (mmHg)"] < 142) | (MR_raw_tick0["O2 (mmHg)"] > 162), "Well"].unique()
    mr_min_o2 = MR_raw_tick0.loc[
        (MR_raw_tick0["O2 (mmHg)"] >= 142) & (MR_raw_tick0["O2 (mmHg)"] <= 162), "O2 (mmHg)"].min()
    mr_max_o2 = MR_raw_tick0.loc[
        (MR_raw_tick0["O2 (mmHg)"] >= 142) & (MR_raw_tick0["O2 (mmHg)"] <= 162), "O2 (mmHg)"].max()
    mr_o2_range = (mr_min_o2, mr_max_o2)

    # pH analysis
    mr_ph_outliers = MR_raw_tick0.loc[(MR_raw_tick0["pH"] < 7.2) | (MR_raw_tick0["pH"] > 7.6), "Well"].unique()
    mr_min_ph = MR_raw_tick0.loc[(MR_raw_tick0["pH"] >= 7.2) & (MR_raw_tick0["pH"] <= 7.6), "pH"].min()
    mr_max_ph = MR_raw_tick0.loc[(MR_raw_tick0["pH"] >= 7.2) & (MR_raw_tick0["pH"] <= 7.6), "pH"].max()
    mr_ph_range = (mr_min_ph, mr_max_ph)

    # Long Baseline- level data analysis
    # subsetting df for starting level (tick 0)
    LB_raw_tick0 = LB_raw.loc[(LB_raw["Tick"] == 0) & (LB_raw["Group"] != "Background")]

    # o2 analysis
    lb_o2_low_limit = LB_raw_tick0["O2 (mmHg)"].median() - 10
    lb_o2_high_limit = LB_raw_tick0["O2 (mmHg)"].median() + 10
    lb_min_o2 = LB_raw_tick0.loc[(LB_raw_tick0["O2 (mmHg)"] >= lb_o2_low_limit) & (
                LB_raw_tick0["O2 (mmHg)"] <= lb_o2_high_limit), "O2 (mmHg)"].min()
    lb_max_o2 = LB_raw_tick0.loc[(LB_raw_tick0["O2 (mmHg)"] >= lb_o2_low_limit) & (
                LB_raw_tick0["O2 (mmHg)"] <= lb_o2_high_limit), "O2 (mmHg)"].max()
    lb_o2_range = (lb_min_o2, lb_max_o2)
    lb_o2_outliers = LB_raw_tick0.loc[
        (LB_raw_tick0["O2 (mmHg)"] < lb_min_o2) | (LB_raw_tick0["O2 (mmHg)"] > lb_max_o2), "Well"].unique()

    # pH analysis
    lb_ph_low_limit = LB_raw_tick0["pH"].median() - 0.1
    lb_ph_high_limit = LB_raw_tick0["pH"].median() + 0.1
    lb_min_ph = LB_raw_tick0.loc[
        (LB_raw_tick0["pH"] >= lb_ph_low_limit) & (LB_raw_tick0["pH"] <= lb_ph_high_limit), "pH"].min()
    lb_max_ph = LB_raw_tick0.loc[
        (LB_raw_tick0["pH"] >= lb_ph_low_limit) & (LB_raw_tick0["pH"] <= lb_ph_high_limit), "pH"].max()
    lb_ph_range = (lb_min_ph, lb_max_ph)
    lb_ph_outliers = LB_raw_tick0.loc[
        (LB_raw_tick0["pH"] < lb_min_ph) | (LB_raw_tick0["pH"] > lb_max_ph), "Well"].unique()

    # Stress Test- level data analysis
    # subsetting df for starting level (tick 0)
    ST_raw_tick0 = ST_raw.loc[(ST_raw["Tick"] == 0) & (ST_raw["Group"] != "Background")]

    # o2 analysis
    st_o2_low_limit = ST_raw_tick0["O2 (mmHg)"].median() - 10
    st_o2_high_limit = ST_raw_tick0["O2 (mmHg)"].median() + 10
    st_min_o2 = ST_raw_tick0.loc[(ST_raw_tick0["O2 (mmHg)"] >= st_o2_low_limit) & (
                ST_raw_tick0["O2 (mmHg)"] <= st_o2_high_limit), "O2 (mmHg)"].min()
    st_max_o2 = ST_raw_tick0.loc[(ST_raw_tick0["O2 (mmHg)"] >= st_o2_low_limit) & (
                ST_raw_tick0["O2 (mmHg)"] <= st_o2_high_limit), "O2 (mmHg)"].max()
    st_o2_range = (st_min_o2, st_max_o2)
    st_o2_outliers = ST_raw_tick0.loc[
        (ST_raw_tick0["O2 (mmHg)"] < st_min_o2) | (ST_raw_tick0["O2 (mmHg)"] > st_max_o2), "Well"].unique()

    # pH analysis
    st_ph_low_limit = ST_raw_tick0["pH"].median() - 0.1
    st_ph_high_limit = ST_raw_tick0["pH"].median() + 0.1
    st_min_ph = ST_raw_tick0.loc[
        (ST_raw_tick0["pH"] >= st_ph_low_limit) & (ST_raw_tick0["pH"] <= st_ph_high_limit), "pH"].min()
    st_max_ph = ST_raw_tick0.loc[
        (ST_raw_tick0["pH"] >= st_ph_low_limit) & (ST_raw_tick0["pH"] <= st_ph_high_limit), "pH"].max()
    st_ph_range = (st_min_ph, st_max_ph)
    st_ph_outliers = ST_raw_tick0.loc[
        (ST_raw_tick0["pH"] < st_min_ph) | (ST_raw_tick0["pH"] > st_max_ph), "Well"].unique()

    mr_filename = MR_cal['Filename'].unique()
    lb_filename = LB_cal['Filename'].unique()
    st_filename = ST_cal['Filename'].unique()
    inst_number = df_cal['Instrument No'].unique()
    inst_type = df_cal['Instrument Type'].unique()
    mr_cart_lot_number = MR_cal['Cartridge Lot'].unique()
    mr_cart_serial_number = MR_cal['Cartridge Serial'].unique()
    lb_cart_lot_number = LB_cal['Cartridge Lot'].unique()
    lb_cart_serial_number = LB_cal['Cartridge Serial'].unique()
    st_cart_lot_number = ST_cal['Cartridge Lot'].unique()
    st_cart_serial_number = ST_cal['Cartridge Serial'].unique()
    software_version = df_cal['Software version'].unique()


    return_dict = {
        'mr_cart_lot_number': mr_cart_lot_number,
        'mr_cart_serial_number': mr_cart_serial_number,
        'lb_cart_lot_number': lb_cart_lot_number,
        'lb_cart_serial_number': lb_cart_serial_number,
        'st_cart_lot_number': st_cart_lot_number,
        'st_cart_serial_number': st_cart_serial_number,
        'software_version': software_version,
        'mr_filename': mr_filename,
        'lb_filename': lb_filename,
        'st_filename': st_filename,
        'inst_number': inst_number,
        'inst_type': inst_type,
        'mr_avg_o2_led': mr_avg_o2_led,
        'mr_avg_ph_led': mr_avg_ph_led,
        'mr_avg_o2_ref': mr_avg_o2_ref,
        'mr_avg_ph_ref': mr_avg_ph_ref,
        'mr_min_o2_led': mr_min_o2_led,
        'mr_min_ph_led': mr_min_ph_led,
        'mr_min_o2_ref': mr_min_o2_ref,
        'mr_min_ph_ref': mr_min_ph_ref,
        'mr_max_o2_led': mr_max_o2_led,
        'mr_max_ph_led': mr_max_ph_led,
        'mr_max_o2_ref': mr_max_o2_ref,
        'mr_max_ph_ref': mr_max_ph_ref,
        'mr_o2_led_outliers': mr_o2_led_outliers,
        'mr_o2_ref_outliers': mr_o2_ref_outliers,
        'mr_ph_led_outliers': mr_ph_led_outliers,
        'mr_ph_ref_outliers': mr_ph_ref_outliers,
        'lb_avg_o2_led': lb_avg_o2_led,
        'lb_avg_ph_led': lb_avg_ph_led,
        'lb_avg_o2_ref': lb_avg_o2_ref,
        'lb_avg_ph_ref': lb_avg_ph_ref,
        'lb_min_o2_led': lb_min_o2_led,
        'lb_min_ph_led': lb_min_ph_led,
        'lb_min_o2_ref': lb_min_o2_ref,
        'lb_min_ph_ref': lb_min_ph_ref,
        'lb_max_o2_led': lb_max_o2_led,
        'lb_max_ph_led': lb_max_ph_led,
        'lb_max_o2_ref': lb_max_o2_ref,
        'lb_max_ph_ref': lb_max_ph_ref,
        'lb_o2_led_outliers': lb_o2_led_outliers,
        'lb_o2_ref_outliers': lb_o2_ref_outliers,
        'lb_ph_led_outliers': lb_ph_led_outliers,
        'lb_ph_ref_outliers': lb_ph_ref_outliers,
        'st_avg_o2_led': st_avg_o2_led,
        'st_avg_ph_led': st_avg_ph_led,
        'st_avg_o2_ref': st_avg_o2_ref,
        'st_avg_ph_ref': st_avg_ph_ref,
        'st_min_o2_led': st_min_o2_led,
        'st_min_ph_led': st_min_ph_led,
        'st_min_o2_ref': st_min_o2_ref,
        'st_min_ph_ref': st_min_ph_ref,
        'st_max_o2_led': st_max_o2_led,
        'st_max_ph_led': st_max_ph_led,
        'st_max_o2_ref': st_max_o2_ref,
        'st_max_ph_ref': st_max_ph_ref,
        'st_o2_led_outliers': st_o2_led_outliers,
        'st_o2_ref_outliers': st_o2_ref_outliers,
        'st_ph_led_outliers': st_ph_led_outliers,
        'st_ph_ref_outliers': st_ph_ref_outliers,
        'mr_ocr_outliers': mr_ocr_outliers,
        'mr_ocr_range': mr_ocr_range,
        'mr_ecar_outliers': mr_ecar_outliers,
        'mr_ecar_range': mr_ecar_range,
        'lb_ocr_outliers': lb_ocr_outliers,
        'lb_mean_ocr': lb_mean_ocr,
        'lb_std_ocr': lb_std_ocr,
        'lb_cv_ocr': lb_cv_ocr,
        'lb_ecar_outliers': lb_ecar_outliers,
        'lb_mean_ecar': lb_mean_ecar,
        'lb_std_ecar': lb_std_ecar,
        'lb_cv_ecar': lb_cv_ecar,
        'st_ocr_outliers': st_ocr_outliers,
        'st_mean_ocr': st_mean_ocr,
        'st_std_ocr': st_std_ocr,
        'st_cv_ocr': st_cv_ocr,
        'st_ecar_outliers': st_ecar_outliers,
        'st_mean_ecar': st_mean_ecar,
        'st_std_ecar': st_std_ecar,
        'st_cv_ecar': st_cv_ecar,
        'mr_o2_range': mr_o2_range,
        'mr_o2_outliers': mr_o2_outliers,
        'mr_ph_range': mr_ph_range,
        'mr_ph_outliers': mr_ph_outliers,
        'lb_o2_range': lb_o2_range,
        'lb_o2_outliers': lb_o2_outliers,
        'lb_ph_range': lb_ph_range,
        'lb_ph_outliers': lb_ph_outliers,
        'st_o2_range': st_o2_range,
        'st_o2_outliers': st_o2_outliers,
        'st_ph_range': st_ph_range,
        'st_ph_outliers': st_ph_outliers
    }
    return return_dict


def IQC_evaluate_result(values):
    if len(np.intersect1d(values["mr_o2_led_outliers"], values["lb_o2_led_outliers"])) > 0 or len(
            np.intersect1d(values["mr_o2_led_outliers"], values["st_o2_led_outliers"])) > 0 or len(
            np.intersect1d(values["mr_o2_ref_outliers"], values["lb_o2_ref_outliers"])) > 0 or len(
            np.intersect1d(values["mr_o2_ref_outliers"], values["st_o2_ref_outliers"])) > 0:
        values['mr_o2_cal_result'] = 'Fail'
    else:
        values['mr_o2_cal_result'] = 'Pass'
    if len(np.intersect1d(values["lb_o2_led_outliers"], values["mr_o2_led_outliers"])) > 0 or len(
            np.intersect1d(values["lb_o2_led_outliers"], values["st_o2_led_outliers"])) > 0 or len(
        np.intersect1d(values["lb_o2_ref_outliers"], values["mr_o2_ref_outliers"])) > 0 or len(
        np.intersect1d(values["lb_o2_ref_outliers"], values["st_o2_ref_outliers"])) > 0:
        values['lb_o2_cal_result'] = 'Fail'
    else:
        values['lb_o2_cal_result'] = 'Pass'
    if len(np.intersect1d(values["st_o2_led_outliers"], values["mr_o2_led_outliers"])) > 0 or len(
            np.intersect1d(values["st_o2_led_outliers"], values["lb_o2_led_outliers"])) > 0 or len(
        np.intersect1d(values["st_o2_ref_outliers"], values["mr_o2_ref_outliers"])) > 0 or len(
        np.intersect1d(values["st_o2_ref_outliers"], values["lb_o2_ref_outliers"])) > 0:
        values['st_o2_cal_result'] = 'Fail'
    else:
        values['st_o2_cal_result'] = 'Pass'

    if len(np.intersect1d(values["mr_ph_led_outliers"], values["lb_ph_led_outliers"])) > 0 or len(
            np.intersect1d(values["mr_ph_led_outliers"], values["st_ph_led_outliers"])) > 0 or len(
        np.intersect1d(values["mr_ph_ref_outliers"], values["lb_ph_ref_outliers"])) > 0 or len(
        np.intersect1d(values["mr_ph_ref_outliers"], values["st_ph_ref_outliers"])) > 0:
        values['mr_ph_cal_result'] = 'Fail'
    else:
        values['mr_ph_cal_result'] = 'Pass'
    if len(np.intersect1d(values["lb_ph_led_outliers"], values["mr_ph_led_outliers"])) > 0 or len(
            np.intersect1d(values["lb_ph_led_outliers"], values["st_ph_led_outliers"])) > 0 or len(
        np.intersect1d(values["lb_ph_ref_outliers"], values["mr_ph_ref_outliers"])) > 0 or len(
        np.intersect1d(values["lb_ph_ref_outliers"], values["st_ph_ref_outliers"])) > 0:
        values['lb_ph_cal_result'] = 'Fail'
    else:
        values['lb_ph_cal_result'] = 'Pass'
    if len(np.intersect1d(values["st_ph_led_outliers"], values["mr_ph_led_outliers"])) > 0 or len(
            np.intersect1d(values["st_ph_led_outliers"], values["lb_ph_led_outliers"])) > 0 or len(
        np.intersect1d(values["st_ph_ref_outliers"], values["mr_ph_ref_outliers"])) > 0 or len(
        np.intersect1d(values["st_ph_ref_outliers"], values["lb_ph_ref_outliers"])) > 0:
        values['st_ph_cal_result'] = 'Fail'
    else:
        values['st_ph_cal_result'] = 'Pass'
    if 1000< values['mr_min_o2_led'] and values['mr_max_o2_led'] < 30000 and values['mr_max_o2_led'] < 2* values['mr_avg_o2_led']:
        values['mr_o2_led_result'] = 'Pass'
    else:
        values['mr_o2_led_result'] = 'Fail'
    if 1000< values['mr_min_ph_led'] and values['mr_max_ph_led'] < 30000 and values['mr_max_ph_led'] < 2* values['mr_avg_ph_led']:
        values['mr_ph_led_result'] = 'Pass'
    else:
        values['mr_ph_led_result'] = 'Fail'
    if 1000< values['lb_min_o2_led'] and values['lb_max_o2_led'] < 30000 and values['lb_max_o2_led'] < 2* values['lb_avg_o2_led']:
        values['lb_o2_led_result'] = 'Pass'
    else:
        values['lb_o2_led_result'] = 'Fail'
    if 1000< values['lb_min_ph_led'] and values['lb_max_ph_led'] < 30000 and values['lb_max_ph_led'] < 2* values['lb_avg_ph_led']:
        values['lb_ph_led_result'] = 'Pass'
    else:
        values['lb_ph_led_result'] = 'Fail'
    if 1000< values['st_min_o2_led'] and values['st_max_o2_led'] < 30000 and values['st_max_o2_led'] < 2* values['st_avg_o2_led']:
        values['st_o2_led_result'] = 'Pass'
    else:
        values['st_o2_led_result'] = 'Fail'
    if 1000< values['st_min_ph_led'] and values['st_max_ph_led'] < 30000 and values['st_max_ph_led'] < 2* values['st_avg_ph_led']:
        values['st_ph_led_result'] = 'Pass'
    else:
        values['st_ph_led_result'] = 'Fail'

    if len(np.intersect1d(values["mr_ocr_outliers"], values["lb_ocr_outliers"]))>0 or len(np.intersect1d(values["mr_ocr_outliers"], values["st_ocr_outliers"]))>0:
        values['mr_ocr_result'] = 'Fail'
    else:
        values['mr_ocr_result'] = 'Pass'
    if len(np.intersect1d(values["lb_ocr_outliers"], values["mr_ocr_outliers"]))>0 or len(np.intersect1d(values["lb_ocr_outliers"], values["st_ocr_outliers"]))>0:
        values['lb_ocr_result'] = 'Fail'
    else:
        values['lb_ocr_result'] = 'Pass'
    if len(np.intersect1d(values["mr_ocr_outliers"], values["lb_ocr_outliers"]))>0 or len(np.intersect1d(values["mr_ocr_outliers"], values["st_ocr_outliers"]))>0:
        values['mr_ocr_result'] = 'Fail'
    else:
        values['mr_ocr_result'] = 'Pass'
    if len(np.intersect1d(values["st_ocr_outliers"], values["mr_ocr_outliers"]))>0 or len(np.intersect1d(values["st_ocr_outliers"], values["lb_ocr_outliers"]))>0:
        values['st_ocr_result'] = 'Fail'
    else:
        values['st_ocr_result'] = 'Pass'
    if len(np.intersect1d(values["mr_ecar_outliers"], values["lb_ecar_outliers"]))>0 or len(np.intersect1d(values["mr_ecar_outliers"], values["st_ecar_outliers"]))>0:
        values['mr_ecar_result'] = 'Fail'
    else:
        values['mr_ecar_result'] = 'Pass'
    if len(np.intersect1d(values["lb_ecar_outliers"], values["mr_ecar_outliers"]))>0 or len(np.intersect1d(values["lb_ecar_outliers"], values["st_ecar_outliers"]))>0:
        values['lb_ecar_result'] = 'Fail'
    else:
        values['lb_ecar_result'] = 'Pass'
    if len(np.intersect1d(values["mr_ecar_outliers"], values["lb_ecar_outliers"]))>0 or len(np.intersect1d(values["mr_ecar_outliers"], values["st_ecar_outliers"]))>0:
        values['mr_ecar_result'] = 'Fail'
    else:
        values['mr_ecar_result'] = 'Pass'
    if len(np.intersect1d(values["st_ecar_outliers"], values["mr_ecar_outliers"]))>0 or len(np.intersect1d(values["st_ecar_outliers"], values["lb_ecar_outliers"]))>0:
        values['st_ecar_result'] = 'Fail'
    else:
        values['st_ecar_result'] = 'Pass'

    if len(np.intersect1d(values["mr_o2_outliers"], values["lb_o2_outliers"]))>0 or len(np.intersect1d(values["mr_o2_outliers"], values["st_o2_outliers"]))>0:
        values['mr_o2_result'] = 'Fail'
    else:
        values['mr_o2_result'] = 'Pass'
    if len(np.intersect1d(values["lb_o2_outliers"], values["mr_o2_outliers"]))>0 or len(np.intersect1d(values["lb_o2_outliers"], values["st_o2_outliers"]))>0:
        values['lb_o2_result'] = 'Fail'
    else:
        values['lb_o2_result'] = 'Pass'
    if len(np.intersect1d(values["mr_o2_outliers"], values["lb_o2_outliers"]))>0 or len(np.intersect1d(values["mr_o2_outliers"], values["st_o2_outliers"]))>0:
        values['mr_o2_result'] = 'Fail'
    else:
        values['mr_o2_result'] = 'Pass'
    if len(np.intersect1d(values["st_o2_outliers"], values["mr_o2_outliers"]))>0 or len(np.intersect1d(values["st_o2_outliers"], values["lb_o2_outliers"]))>0:
        values['st_o2_result'] = 'Fail'
    else:
        values['st_o2_result'] = 'Pass'
    if len(np.intersect1d(values["mr_ph_outliers"], values["lb_ph_outliers"]))>0 or len(np.intersect1d(values["mr_ph_outliers"], values["st_ph_outliers"]))>0:
        values['mr_ph_result'] = 'Fail'
    else:
        values['mr_ph_result'] = 'Pass'
    if len(np.intersect1d(values["lb_ph_outliers"], values["mr_ph_outliers"]))>0 or len(np.intersect1d(values["lb_ph_outliers"], values["st_ph_outliers"]))>0:
        values['lb_ph_result'] = 'Fail'
    else:
        values['lb_ph_result'] = 'Pass'
    if len(np.intersect1d(values["mr_ph_outliers"], values["lb_ph_outliers"]))>0 or len(np.intersect1d(values["mr_ph_outliers"], values["st_ph_outliers"]))>0:
        values['mr_ph_result'] = 'Fail'
    else:
        values['mr_ph_result'] = 'Pass'
    if len(np.intersect1d(values["st_ph_outliers"], values["mr_ph_outliers"]))>0 or len(np.intersect1d(values["st_ph_outliers"], values["lb_ph_outliers"]))>0:
        values['st_ph_result'] = 'Fail'
    else:
        values['st_ph_result'] = 'Pass'
    return values