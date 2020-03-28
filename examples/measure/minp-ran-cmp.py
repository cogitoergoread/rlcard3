"""
Compare min agent and random agent.
Agent sets? MMMR, MMRR, MRRR
Cards: 15 .. 55 step 4
"""
from typing import List
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# PATH Const
PNG_SAVE_PRFX = 'F:/muszi/AnaPy/rlcard3/examples/measure/result'
LOG_SAVE_PRFX = 'f:/tmp/rlcard2log'

# File names
# log_dirname = 'Ran_Mi_Mp_Mw_20200304-163948'
# Nagyobb futás
# log_filename = '300_20200304-164711.csv'
# log_dirname = 'Ran_Mi_Mp_Mw_110_20200308-210102'
# log_filename = '300_20200308-212904.csv'
# plot_list2 = [
#     ('PPRR', "Payoff distribution for 2 MinPlus and 2 Random agents", True, "Ag2vs2V"),
#     ('MMPP', "Payoff distribution for 2 MinPlus and 2 Min agents", True, "Ag2vs2V"),
#     ('PRRR', "Payoff distribution for 1 MinPlus and 3 Random agents", True, "Ag1vs3V"),
#     ('QQRR', "Payoff distribution for 2 MinPlusWin and 2 Random agents", True, "Ag2vs2V"),
#     ('PPQQ', "Payoff distribution for 2 MinPlusWin(Q) and 2 MinPlus(P) agents", True, "Ag2vs2V"),
#     ('PPRR', "Mean payoff for 2 MinPlus and 2 Random agents", False, "Ag2vs2L"),
#     ('QQRR', "Mean payoff for 2 MinPlusWin and 2 Random agents", False, "Ag2vs2L"),
#     ('MMPP', "Mean payoff for 2 MinPlus and 2 Min agents", False, "Ag2vs2L"),
#     ('PPQQ', "Mean payoff for 2 MinPlus and 2 MinPlusWin agents", False, "Ag2vs2L"),
#     ('QQRR', "Mean payoff for 2 Random (R) 2 MinPlusWin (Q) agents", False, "Ag2vs2L"),
# ]

# DQN
#log_dirname = 'Ran_Mi_Mp_Mw_110_20200318-200223'
#log_filename = '300_20200318-200847.csv'
# plot_list3 = [
#     ('RRdd', "Payoff distribution for 2 DQN and 2 Random agents", True, "Ag2vs2V"),
#     ('RRdd', "Mean payoff for 2 DQN and 2 Random agents", False, "Ag2vs2L"),
# ]

# RAS, van pass
#log_dirname = 'RAS_Mi_110_20200322-075346'
#log_filename = '300_20200322-075802.csv'
# plot_list4 = [
#     ('MMRR', "RAS, pass action enabled, Payoff distribution for 2 Min and 2 Random agents", True, "Ag2vs2V"),
#     ('MMRR', "RAS, pass action enabled, Mean payoff for 2 MIN and 2 Random agents", False, "Ag2vs2L"),
# ]

# RAS + NoPass, passzolás elnyomva, TRandom agent passzol 10%
#log_dirname = 'RAS_NP_Mi_110_20200322-084228'
#log_filename = '300_20200322-084643.csv'
# plot_list4 = [
#     ('MMRR', "RAS, pass action disabled, Payoff distribution for 2 Min and 2 Random agents", True, "Ag2vs2V"),
#     ('MMRR', "RAS, pass action disabled, Mean payoff for 2 Min and 2 Random agents", False, "Ag2vs2L"),
# ]

# RAS DQN 100k
#log_dirname = 'RAS_NP_Mi_110_20200324-172136'
#log_filename = '300_20200324-172350.csv'
# plot_list = [
#     ('RRdd', "RAS, Payoff distribution for 2 DQN 100k and 2 Random agents", True, "Ag2vs2V"),
#     ('RRdd', "RAS, Mean payoff for 2 DQN 100k and 2 Random agents", False, "Ag2vs2L"),
# ]

# RAS DQN 100k több
# log_dirname = 'RAS_DQN100_20200324-173729'
# log_filename = '500_20200324-180556.csv'
# plot_list = [
#     ('RRdd', "RAS, Payoff distribution for 2 DQN 100k and 2 Random agents", True, "Ag2vs2V"),
#     ('RRdd', "RAS, Mean payoff for 2 DQN 100k and 2 Random agents", False, "Ag2vs2L"),
#     ('RRRd', "Payoff distribution for 1 DQN 100k and 3 Random agents", True, "Ag1vs3V"),
#     ('RRRd', "RAS, Mean payoff for 1 DQN 100k and 3 Random agents", False, "Ag2vs2L"),
#     ('MMdd', "RAS, Payoff distribution for 2 DQN 100k and 2 Min agents", True, "Ag2vs2V"),
#     ('MMdd', "RAS, Mean payoff for 2 DQN 100k and 2 Min agents", False, "Ag2vs2L"),
#     ('MMMd', "Payoff distribution for 1 DQN 100k and 3 Min agents", True, "Ag1vs3V"),
# ]

# rlcard3, Min - Random
log_dirname = '3RAS_RAMI_20200328-164129'
log_filename = '500_20200328-164650.csv'
plot_list = [
    ('MMRR', "Payoff distribution for 2 Min and 2 Random agents", True, "Ag2vs2V"),
    ('MRRR', "Payoff distribution for 1 Min and 3 RANDOM agents", True, "Ag2vs2V"),
    ('MMRR', "RAS, Mean payoff for 2 Min and 2 Random agents", False, "Ag2vs2L"),
]

def read_data() -> pd.DataFrame:
    dfr = pd.read_csv(f"{LOG_SAVE_PRFX}/{log_dirname}/{log_filename}", sep=";")
    return dfr


def create_plots(df: pd.DataFrame, agentstr: str, title: str, is_violin: bool, filename: str):
    """
    Create nice figures from the played data
    :param title: Tilte of the figure
    :param df: DataFrame containing the logs of the games
    :param agentstr: Which type of data to display
    :param is_violin: Violin / line graph
    :param filename: filename to store the fihure
    """
    if is_violin:
        _ = sns.violinplot(x="cardnr", y="payoff", data=df[(df['agentstr'] == agentstr)], hue="agentid",
                           split=True).set_title(title)
    else:
        _ = sns.relplot(x="cardnr", y="payoff", kind="line", data=df[(df['agentstr'] == agentstr)], hue="agentid")
        plt.title(title)
    dir_path = f"{PNG_SAVE_PRFX}/{log_dirname}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    plt.savefig(f"{PNG_SAVE_PRFX}/{log_dirname}/{filename}_{agentstr}.png")
    plt.show()


def plot_list_items(pl_list: List):
    df = read_data()
    for agentstr, title, is_violin, filename in pl_list:
        create_plots(df, agentstr, title, is_violin, filename)

plot_list_items(plot_list)
