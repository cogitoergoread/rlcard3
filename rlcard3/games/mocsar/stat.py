"""
Class to store information about series of games into files.
The aim is to collect statistics about it.
"""
from typing import List, Dict
from rlcard3.games.mocsar.game import MocsarGame as Game
import pandas as pd
import csv
import datetime
from rlcard3.games.mocsar.utils import card_list_to_str
import json
import os


class MocsarStat:
    game_payeoffs: List[Dict]  # List of dictionary items, See "tennivalo.md",  #### Eredmény
    game_hist: List[Dict]  # List of dictionary items, See "tennivalo.md",  #### Játékmenet
    game: Game
    game_nr: int  # Actual number of the current game int the series
    log_dir: str  # Path, to store the log directories
    log_batch_dir: str  # Path, to store the log files
    filename: str  # name of the files to store info in
    nr_of_cards: int  # The number of cards the game was played
    agent_ids: List[str]
    agent_names: List[str]
    agentstr: str  # Agent names joined
    nr_of_games: int  # Number of games

    def __init__(self, game: Game, agents: List, nr_of_games: int, log_dir: str, batch_name: str = ""):
        self.game = game
        self.nr_of_games = nr_of_games
        self.game_payeoffs = list()
        self.game_hist = list()
        self.agent_ids = list()
        self.agent_names = list()
        self.log_dir = log_dir

        self.reset_game_nr(agents)
        self._create_batch_dir(batch_name, datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))

    def next_game(self):
        """Invrement game nr"""
        self.game_nr += 1

    def reset_game_nr(self, agents: List):
        self.game_nr = 1
        self.nr_of_cards = self.game.dealer.nr_cards
        self.agent_ids.clear()
        self.agent_names.clear()
        # Build up filename
        agentids = [agent.id for agent in agents]
        agentids.sort()
        self.agentstr = ",".join(agentids).replace(",", "")
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

        self.filename = f"{self.nr_of_games}_{timestamp}"
        # Store agents
        for agent in agents:
            self.agent_ids.append(agent.id)
            self.agent_names.append(agent.name)

    def add_startgame(self):
        """Store information about the starting of the game"""
        self.game_hist.append({
            "gamenr": self.game_nr,
            "cardnr": self.nr_of_cards,
            "agentstr": self.agentstr,  # Milyen Agentek játszottak
            'players': [{
                "playerid": playerid,
                "name": self.game.players.players[playerid].name,
                "agentid": self.agent_ids[playerid],
                "cards": card_list_to_str(self.game.players.players[playerid].hand),
                "order": self.game.players.order.index(playerid)
            } for playerid in range(self.game.num_players)]
        })

    def add_result(self, payoffs: List):
        """
        Add result to the statistics
        :param payoffs: See MocsarEnv.get_payoffs(), List of results in the game by PlayerID
        """
        # Store the results
        for playerid in range(self.game.num_players):
            self.game_payeoffs.append({
                "cardnr": self.nr_of_cards,  # Ennyi kártyás játék volt
                "gamenr": self.game_nr,  # játék sorszáma 1..100
                "playerid": playerid,  # 0...n
                "agentid": self.agent_ids[playerid],
                "agentstr": self.agentstr,  # Milyen Agentek játszottak
                "payoff": payoffs[playerid]  # Pontszám a kör végén
            })
        # Store hostory
        self.game_hist[-1]["history"] = self.game.played_rounds

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.game_payeoffs)

    def write_to_file(self):
        """
        Write the list to a CSV file
        :return:
        """
        # Write results to csv
        df = self.get_dataframe()
        df.to_csv(os.path.join(self.log_batch_dir, f"{self.filename}.csv"),
                  quoting=csv.QUOTE_NONNUMERIC, sep=";")

        # Write history to json
        with open(os.path.join(self.log_batch_dir, f"{self.filename}.json"), 'w', encoding='utf-8') as f:
            json.dump(self.game_hist, f, ensure_ascii=False, indent=4)

    def _create_batch_dir(self, batch_name: str, timestamp: str):
        """
        Létrehoz egy alkönyvtárat, ha a batch név neg van adva
        :param timestamp: Az az időpont, amikor fut a játék összehasonlítás
        :param batch_name: a batch futtatás neve
        :return:
        """
        if len(batch_name) == 0:
            self.log_batch_dir = self.log_dir
        else:
            dirname = os.path.join(self.log_dir, f"{batch_name}_{timestamp}")
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            self.log_batch_dir = dirname
