import atexit
import logging
import sys
import time

from position import Position
from scraper import Scraper


NEEDLE_TOOL_OFFSET = Position(x=15.5, y=12, z=0)
NEEDLE_WIDTH = 1.5 # millimeters
SAMPLE_POSITION = Position(x=125, y=91, z=0.8)
SAMPLE_SIZE = 15 # millimeters

scraper = Scraper()
scraper.connect()
atexit.register(scraper.disconnect)

scraper.set_tool_offset(NEEDLE_TOOL_OFFSET)
scraper.set_needle_width(NEEDLE_WIDTH)
scraper.set_speed(500)
scraper.set_acceleration(3000)

# scraper.enable_axis()
scraper.home()

# scraper.move_to(SAMPLE_POSITION)
# input('done?')

# actually SCRAPE
# scraper.scrape(SAMPLE_POSITION, SAMPLE_SIZE, crossover=1.25, speed=500, accel=1000)
# scraper.resting_position()

# scraper.move_to(Position(x=0, y=0, z=50), relative=True, direct=True)

scraper.finish_moves()
