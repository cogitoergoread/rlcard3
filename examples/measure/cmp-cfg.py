"""
    File name: examples/measure/cmp-cfg.py
    Author: József Varga
    Date created: 4/06/2020
    Compare various agents
"""
import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from rlcard3.games.mocsar.agentdb import str_to_agent_dict, get_by_id
from rlcard3.utils.config_read import Config

conf = Config('environ.properties')
# PATH Const
LOG_SAVE_PRFX = conf.get_str(section='cfg.compare', key="stat_dir_path")
PNG_SAVE_PRFX = conf.get_str(section='cfg.visual', key="png_dir_path")
log_dirname = conf.get_str(section='cfg.visual', key="dir_name")
log_filename = conf.get_str(section='cfg.visual', key="file_name")


def read_data() -> pd.DataFrame:
    csv_file_name = os.path.join(LOG_SAVE_PRFX, log_dirname, log_filename)
    dfr = pd.read_csv(csv_file_name, sep=";")
    return dfr


def create_plots(df: pd.DataFrame, agentstr: str, plot_type: str):
    """
    Create nice figures from the played data
    :param df: DataFrame containing the logs of the games
    :param agentstr: Which type of data to display
    :param plot_type: VIO: Violin plot, LIN: Line plot
    """
    if plot_type == 'VIO':
        # Violin plot comparing agent performace
        ag_di = str_to_agent_dict(agentstr, False)
        ag_1, ag_2 = get_by_id(list(ag_di.keys())[0]), get_by_id(list(ag_di.keys())[1])
        title = f"Payoff distribution for {ag_di[ag_1.aid]} {ag_1.aname} and {ag_di[ag_2.aid]} {ag_2.aname}"
        plt_filename = f"Ag2vs2V_{agentstr}.png"
        _ = sns.violinplot(x="cardnr", y="payoff", data=df[(df['agentstr'] == agentstr)], hue="agentid",
                           split=True).set_title(title)
    elif plot_type == 'LIN':
        # Line plot comparing agent vs agent results
        ag_di = str_to_agent_dict(agentstr, False)
        ag_1, ag_2 = get_by_id(list(ag_di.keys())[0]), get_by_id(list(ag_di.keys())[1])
        title = f"Mean payoff for {ag_di[ag_1.aid]} {ag_1.aname} and {ag_di[ag_2.aid]} {ag_2.aname}"
        plt_filename = f"Ag2vs2L_{agentstr}.png"
        _ = sns.relplot(x="cardnr", y="payoff", kind="line", data=df[(df['agentstr'] == agentstr)], hue="agentid")
        plt.title(title)
        plt.tight_layout()
        plt.subplots_adjust(top=0.88)
    elif plot_type =="CMP":
        # Compare performance against Random agents
        agentstrli = agentstr.split('-')
        ag_li_str = ','.join([  get_by_id(agstr.replace("R", "")[0]).aname  for agstr in agentstrli])

        # Plays from the list
        df2 = df[df.agentstr.isin(agentstrli)]
        # Filter out the result of a RandomAgent
        df2 = df2[df2['agentid'] != 'R']
        title = f"Mean payoff against Random agent for {ag_li_str}"
        plt_filename = f"Randvs2Ags2L_{ag_li_str}.png"
        _ = sns.relplot(x="cardnr", y="payoff", kind="line", data=df2, hue="agentstr")
        plt.title(title)
        plt.tight_layout()
        plt.subplots_adjust(top=0.88)
    dir_path = os.path.join(PNG_SAVE_PRFX, log_dirname)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    plt.savefig(os.path.join(dir_path, plt_filename))
    plt.show()


def plot_list_items(pl_list: List):
    df = read_data()
    for plot_element in pl_list:
        plot_type, agentstr = plot_element.split(':')
        create_plots(df, agentstr, plot_type)


plot_list_items(conf.get_str(section='cfg.visual', key="plot_list").split(','))
