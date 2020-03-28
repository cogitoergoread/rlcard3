"""
A toy example of playing against random bot on Mocsár
Using env "mocsar" and 'human_mode'. It implies using random agent.
"""

import rlcard3

# Make environment and enable human mode
env = rlcard3.make(env_id='mocsar', config={'human_mode': True})

# Reset environment
state = env.reset()

while not env.is_over():
    legal_actions = state['legal_actions']
    legal_actions.insert(0, 0)
    action = input('>> You choose action (integer): ')
    if action == '-1':
        print('Break the game...')
        break
    while not action.isdigit() \
            or int(action) not in legal_actions:
        print('Action illegal...')
        action = input('>> Re-choose action (integer): ')
    state, reward, done = env.step(int(action))
