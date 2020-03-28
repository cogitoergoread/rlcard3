"""
Process results of various cuda tests
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

PNG_SAVE_PRFX = 'F:/muszi/AnaPy/rlcard2/rlcard3/mocsar_measure/result_cuda'
LOG_SAVE_PRFX = 'f:/muszi/gwork/mocsar_unpack'

case = 'mocsar_4fele_55_10_bigosb'

dir_dic = {
    "NFSP" : "mocsar_nfsp_result",
    "DQN": "mocsar_dqn_result",
    "NFSP RA": "mocsar_nfsp_ra_result",
    "DQN RA": "mocsar_dqn_ra_result",
}
df = pd.DataFrame()
for name, directory in dir_dic.items():
#name, directory = "NFSP" , "mocsar_nfsp_result"
    dfr = pd.read_csv(f"{LOG_SAVE_PRFX}/{case}/{directory}/performance.csv", sep=",")
    dfr['agent']=name
    df = pd.concat([df, dfr])

_ = sns.relplot(x="timestep", y="reward", kind="line", data=df, hue="agent")
plt.title('55 cards, 10k episode, OSB mapping is 9 pcs 3 layers')
plt.show()