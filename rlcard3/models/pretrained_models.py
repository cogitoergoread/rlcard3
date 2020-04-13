''' Wrrapers of pretrained models.
'''

import os

import rlcard3
from rlcard3.agents.cfr_agent import CFRAgent
from rlcard3.models.model import Model

# Root path of pretrianed models
ROOT_PATH = os.path.join(rlcard3.__path__[0], 'models/pretrained')


class LeducHoldemNFSPModel(Model):
    ''' A pretrained model on Leduc Holdem with NFSP
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        import tensorflow as tf
        from rlcard3.agents.nfsp_agent import NFSPAgent
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)

        env = rlcard3.make('leduc-holdem')
        with self.graph.as_default():
            self.nfsp_agents = []
            for i in range(env.player_num):
                agent = NFSPAgent(self.sess,
                                  scope='nfsp' + str(i),
                                  action_num=env.action_num,
                                  state_shape=env.state_shape,
                                  hidden_layers_sizes=[128, 128],
                                  q_mlp_layers=[128, 128])
                self.nfsp_agents.append(agent)

        check_point_path = os.path.join(ROOT_PATH, 'leduc_holdem_nfsp')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.train.Saver()
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.nfsp_agents


class LeducHoldemNFSPPytorchModel(Model):
    ''' A pretrained PyTorch model on Leduc Holdem with NFSP
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        import torch
        from rlcard3.agents.nfsp_agent_pytorch import NFSPAgent as NFSPAgentPytorch
        env = rlcard3.make('leduc-holdem')
        self.nfsp_agents = []
        for i in range(env.player_num):
            agent = NFSPAgentPytorch(scope='nfsp' + str(i),
                                     action_num=env.action_num,
                                     state_shape=env.state_shape,
                                     hidden_layers_sizes=[128, 128],
                                     q_mlp_layers=[128, 128],
                                     device=torch.device('cpu'))
            self.nfsp_agents.append(agent)

        check_point_path = os.path.join(ROOT_PATH, 'leduc_holdem_nfsp_pytorch/model.pth')
        checkpoint = torch.load(check_point_path)
        for agent in self.nfsp_agents:
            agent.load(checkpoint)

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.nfsp_agents


class LeducHoldemCFRModel(Model):
    ''' A pretrained model on Leduc Holdem with CFR
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard3.make('leduc-holdem')
        self.agent = CFRAgent(env, model_path=os.path.join(ROOT_PATH, 'leduc_holdem_cfr'))
        self.agent.load()

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return [self.agent, self.agent]


class MocsarPreNFSPPytorchModel(Model):
    ''' A pretrained PyTorch model on Mocsar with NFSP, learnt against itself
    '''

    def __init__(self, **kwargs):
        ''' Load pretrained model
        '''
        import torch
        from rlcard3.agents.nfsp_agent_pytorch import NFSPAgent as NFSPAgentPytorch
        num_players, action_num, state_shape = kwargs['num_players'], kwargs['action_num'], kwargs['state_shape']
        self.nfsp_agents = []
        for i in range(num_players):
            agent = NFSPAgentPytorch(scope='nfsp' + str(i),
                                     action_num=action_num,
                                     state_shape=state_shape,
                                     hidden_layers_sizes=[512, 512],
                                     q_mlp_layers=[512, 512],
                                     device=torch.device('cuda'))
            self.nfsp_agents.append(agent)

        check_point_path = os.path.join(ROOT_PATH, 'mocsar_nfsp_pytorch/model.pth')
        checkpoint = torch.load(check_point_path)
        for agent in self.nfsp_agents:
            agent.id = "j"
            agent.name = "PreNFSPPytorch"
            agent.load(checkpoint)

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.nfsp_agents


class MocsarPreNFSPPytorchModelMin(MocsarPreNFSPPytorchModel):
    ''' A pretrained PyTorch model on Mocsar with NFSP, learnt against 3 MIn agents
    '''

    def __init__(self, **kwargs):
        ''' Load pretrained model
        '''
        import torch
        from rlcard3.agents.nfsp_agent_pytorch import NFSPAgent as NFSPAgentPytorch
        num_players, action_num, state_shape = kwargs['num_players'], kwargs['action_num'], kwargs['state_shape']
        self.num_players = num_players
        self.agent = NFSPAgentPytorch(scope='nfsp',
                                      action_num=action_num,
                                      state_shape=state_shape,
                                      hidden_layers_sizes=[512, 512],
                                      q_mlp_layers=[512, 512],
                                      device=torch.device('cuda'))

        check_point_path = os.path.join(ROOT_PATH, 'mocsar_nfsp_pytorch/model_min.pth')
        checkpoint = torch.load(check_point_path)
        self.agent.id = "i"
        self.agent.name = "PreNFSPPytorchMin"
        self.agent.load(checkpoint)

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return [self.agent for _ in range(self.num_players)]


class MocsarPreDQNPytorchModel(Model):
    ''' A pretrained PyTorch model on Mocsar with DQN, against Min agents
    '''

    def __init__(self, **kwargs):
        ''' Load pretrained model
        '''
        import torch
        from rlcard3.agents.dqn_agent_pytorch import DQNAgent as DQNAgentPytorch
        num_players, action_num, state_shape = kwargs['num_players'], kwargs['action_num'], kwargs['state_shape']
        self.num_players = num_players
        self.agent = DQNAgentPytorch(scope='dqn',
                                     action_num=action_num,
                                     replay_memory_init_size=1000,  # Not important while not training
                                     train_every=1,  # Not important while not training
                                     state_shape=state_shape,
                                     mlp_layers=[512, 512],
                                     device=torch.device('cuda'))
        self._local_init()

    def _local_init(self):
        self._init_end(chkp='mocsar_dqn_ra_pytorch/model.pth', aid="k", aname="PreDQNPytorch")

    def _init_end(self, chkp: str, aid: str, aname: str):
        import torch
        check_point_path = os.path.join(ROOT_PATH, chkp)
        checkpoint = torch.load(check_point_path)
        self.agent.load(checkpoint)
        self.agent.id = aid
        self.agent.name = aname

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return [self.agent for _ in range(self.num_players)]


class MocsarPreDQNPytorchModelRan(MocsarPreDQNPytorchModel):
    ''' A pretrained PyTorch model on Mocsar with DQN, Against Random agents
    '''

    def _local_init(self):
        self._init_end(chkp='mocsar_dqn_ra_pytorch/model_random.pth', aid="l", aname="PreDQNPytorchRan")
