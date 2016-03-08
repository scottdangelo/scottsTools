#!/usr/bin/env python

INPUT_FILE = 'stuckCreating.txt'

def get_vol_id_stuck_in_state(self, file, state):
    """
    return a list of volume_ids stuck in state 'state'
    """
    with open(file, 'r') as f:
    for line in f:
        print line


if __name__ == '__main__':
    FLAGS.register_cli_opts(command_opt)
    BockSetResourceStatus().run()
