import logging

from motion_control import MotionController
from position import Position
from scrape_planner import generate_scrape_lines_square


logger = logging.getLogger('ender_3_test.scraper')

SCRAPER_DEFAULT_NEEDLE_WIDTH = 1 # TODO: get actual width of needle
SCRAPER_DEFAULT_SAFE_Z = 5 # lift height between normal movements
SCRAPER_DEFAULT_SCRAPE_LIFT_Z_MM = 2 # lift height between scraping lines
SCRAPER_DEFAULT_SCRAPE_SPEED = 100
SCRAPER_DEFAULT_SCRAPE_ACCEL = 100

SCRAPER_DEFAULT_TOOL_OFFSET = Position(x=15.5, y=12, z=1.5)
SCRAPER_DEFAULT_RESTING_POS = Position(x=0, y=200, z=SCRAPER_DEFAULT_SAFE_Z)


class Scraper(MotionController):

    def __init__(self):
        super().__init__()
        self.set_tool_offset(SCRAPER_DEFAULT_TOOL_OFFSET)
        self.set_safe_z(SCRAPER_DEFAULT_SAFE_Z)
        self.needle_width = SCRAPER_DEFAULT_NEEDLE_WIDTH

    def set_needle_width(self, needle_width):
        self.needle_width = needle_width

    def resting_position(self):
        self.move_to(SCRAPER_DEFAULT_RESTING_POS)

    def scrape(self, pos, width, speed=SCRAPER_DEFAULT_SCRAPE_SPEED, accel=SCRAPER_DEFAULT_SCRAPE_ACCEL):
        step_size = self.needle_width
        lines = generate_scrape_lines_square(pos, width, step_size, horizontal=False, start='tl')
        # 1) safe-move to first line
        start_pos_safe = lines[0][0] + Position(x=0, y=0, z=SCRAPER_DEFAULT_SAFE_Z)
        self.move_to(start_pos_safe)
        # 2) direct-move through all lines
        old_speed = int(self.speed)
        old_accel = int(self.acceleration)
        for l in lines:
            self.move_to(l[0], safe_z=SCRAPER_DEFAULT_SCRAPE_LIFT_Z_MM) # smaller "safe" height
            self.set_speed(speed)
            self.set_acceleration(accel)
            self.move_to(l[1], direct=True)
            self.set_speed(old_speed)
            self.set_acceleration(old_accel)
        # 3) rise up
        self.move_to(Position(x=0, y=0, z=SCRAPER_DEFAULT_SAFE_Z), relative=True, direct=True)


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
    # scraper.home()
    scraper.resting_position()
    scraper.scrape(Position(x=100, y=100, z=0), 5)
    scraper.resting_position()



