""" A toy example of playing against random bot on Mocsár
"""

import rlcard

# Make environment and enable human mode
env = rlcard.make(env_id= 'mocsar', config={'human_mode' : True})

# Reset environment
state = env.reset()  # TODO ez még nem fut

while not env.is_over():
    action = input('>> You choose action (integer): ')
    if action == '-1':
        print('Break the game...')
        break
    while not action.isdigit() \
            or int(action) not in state['legal_actions']:
        print('Action illegal...')
        action = input('>> Re-choose action (integer): ')
    state, reward, done = env.step(int(action))
