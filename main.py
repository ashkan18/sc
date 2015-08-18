__author__ = 'ashkan'

import config
from follower_maze import FollowerMaze
import logging

logging.basicConfig(level=config.LOG_LEVEL)

if __name__ == '__main__':
    follower_maze = FollowerMaze(event_port=config.SERVICE_PORT, client_port=config.CLIENT_PORT)
    follower_maze.start()

    raw_input('Press enter to stop servers.\n')

    follower_maze.stop()
