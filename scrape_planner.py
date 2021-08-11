import logging
import math

from position import Position

logger = logging.getLogger('ender_3_test.scrape_planner')

# take center coordinate, and create scrapping lines
# shape? (circle/square)


def generate_scrape_lines_square(pos, width, step_size):
    # start at top-left
    # 
    return


def generate_scrape_lines_circle(pos, diameter, step_size):
    return


if __name__ == '__main__':
    import sys

    logging.basicConfig(
        # filename='logfile.log',
        stream=sys.stdout, 
        filemode='w',
        format='%(levelname)s %(asctime)s - %(message)s', 
        level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    #
