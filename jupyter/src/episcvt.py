"""
    Convert timstep to episode
    File name: jpyter/src/episcvt.py
    Author: József Varga
    Date created: 4/08/2020

    CSV header, source : timestep,reward,episode,timestamp
    CSV header, dest : timestep,reward,episode
"""

import pandas as pd

def episcvt(file_from_csv:str, file_to_csv:str, episode:int):
    df = pd.read_csv(file_from_csv, sep=",")
    max_timestep = df['timestep'].max()
    df["episode"] = df['timestep'] / max_timestep * episode
    df = df.astype({'episode': 'int64'})
    df.to_csv(file_to_csv, sep=",")

episcvt(file_from_csv= "f:/muszi/gwork/mocsar_unpack/mocs_75_bigjav/performance-nfsp.csv",
        file_to_csv="f:/muszi/AnaPy/rlcard3/jupyter/data/2020_03_05_bigjav_50k-nfsp.csv",
        episode= 22000)
episcvt(file_from_csv= "f:/muszi/gwork/mocsar_unpack/mocs_75_bigjav/performance-nfsp-ra.csv",
        file_to_csv="f:/muszi/AnaPy/rlcard3/jupyter/data/2020_03_05_bigjav_50k-nfsp-ra.csv",
        episode= 22000)