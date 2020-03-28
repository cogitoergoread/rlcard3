"""
A toy example of playing against defined set of bots on Mocsár
Using env "mocsar"-cfg Using 'human_mode'
"""

import rlcard

# Make environment and enable human mode
env = rlcard.make('mocsar-cfg', config={'human_mode': True})

# Register agents
agents = {"mocsar_random": 2, "mocsar_min": 2}
env.model.create_agents(agents)

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
