''' Register new environments
'''

from rlcard3.envs.registration import register, make

register(
    env_id='blackjack',
    entry_point='rlcard3.envs.blackjack:BlackjackEnv',
)

register(
    env_id='doudizhu',
    entry_point='rlcard3.envs.doudizhu:DoudizhuEnv',
)
register(
    env_id='simple-doudizhu',
    entry_point='rlcard3.envs.simpledoudizhu:SimpleDoudizhuEnv',
)
register(
    env_id='limit-holdem',
    entry_point='rlcard3.envs.limitholdem:LimitholdemEnv',
)

register(
    env_id='no-limit-holdem',
    entry_point='rlcard3.envs.nolimitholdem:NolimitholdemEnv',
)

register(
    env_id='leduc-holdem',
    entry_point='rlcard3.envs.leducholdem:LeducholdemEnv'
)

register(
    env_id='uno',
    entry_point='rlcard3.envs.uno:UnoEnv',
)

register(
    env_id='mahjong',
    entry_point='rlcard3.envs.mahjong:MahjongEnv',
)

register(  # 200213
    env_id='gin-rummy',
    entry_point='rlcard3.envs.ginrummy:GinRummyEnv',
)

register(
    env_id='mocsar',
    entry_point='rlcard3.envs.mocsar:MocsarEnv',
)

register(
    env_id='mocsar-cfg',
    entry_point='rlcard3.envs.mocsar_cfg:MocsarCfgEnv',
)
