"""
    Data visualization, Compare learning rates
    File name: jpyter/src/lrnratediff.py
    Author: József Varga
    Date created: 4/07/2020

    See dtavis.py

    CSV header : timestep,reward,episode,timestamp
"""

import io
from urllib.request import urlopen
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

r1 = urlopen(
    'https://github.com/cogitoergoread/rlcard3/raw/master/jupyter/data/2020_04_07_DQN_Pytorch_Random_200k.csv.gz')
df1 = pd.read_csv(io.BytesIO(r1.read()), compression='gzip', sep=",")
df1['agent'] = 'R'

r2 = urlopen('https://github.com/cogitoergoread/rlcard3/raw/master/jupyter/data/2020_04_02_DQN_Pytorch_Min_200k.csv.gz')
df2 = pd.read_csv(io.BytesIO(r2.read()), compression='gzip', sep=",")
df2['agent'] = 'M'

df = pd.concat([df1, df2])

df = df[['reward', 'episode', 'agent']]

title = "Mean payoff for DQN agent vs Random agents, learnt against R:Random / M:Min agents"
_ = sns.relplot(x="episode", y="reward", kind="line", data=df , hue="agent")
plt.title(title)
plt.show()
