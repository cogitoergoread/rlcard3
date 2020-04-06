"""
    Data visualization, Compare agent csv
    File name: jpyter/src/dtavis.py
    Author: József Varga
    Date created: 4/06/2020

    Using pandas read_csv with zip compression
    https://stackoverflow.com/questions/40744027/using-pandas-read-csv-with-zip-compression
    https://stackoverflow.com/questions/2792650/import-error-no-module-name-urllib2
"""

import io
from urllib.request import urlopen
import pandas as pd

r = urlopen('https://github.com/cogitoergoread/rlcard3/raw/master/jupyter/data/CAS2_110_MMRR_500_20200405-113309.csv.gz')
df = pd.read_csv(io.BytesIO(r.read()), compression='gzip', sep=";")
print(df)