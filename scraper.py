import logging

from motion_control import MotionController
from position import Position
from scrape_planner import generate_scrape_lines_square


logger = logging.getLogger('ender_3_test.scraper')

SCRAPER_DEFAULT_OFFSET = Position(x=15.5, y=12, z=2)
SCRAPER_DEFAULT_WIDTH = 2 # TODO: get actual width of needle
SCRAPER_DEFAULT_RESTING_POS = Position(x=0, y=200, z=10)


class Scraper(MotionController):

    def __init__(self, needle_width=1, offset=SCRAPER_DEFAULT_OFFSET):
        super().__init__()
        self.set_tool_offset(offset)
        self.needle_width = needle_width

    def resting_position(self):
        self.move_to(SCRAPER_DEFAULT_RESTING_POS)

    def scrape(self, pos, width):
        step_size = self.needle_width / 2
        lines = generate_scrape_lines_square(pos, width, step_size, horizontal=False, start='tl')


if __name__ == '__main__':
    import sys

    logging.basicConfig(
        # filename='logfile.log',
        stream=sys.stdout, 
        filemode='w',
        format='%(levelname)s %(asctime)s - %(message)s', 
        level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    scraper = Scraper()
    scraper.connect()
    scraper.home()
    scraper.resting_position()
    scraper.scrape(Position(x=100, y=100, z=0), 10)
    scraper.resting_position()



