import atexit

from position import Position
from scraper import Scraper


NEEDLE_TOOL_OFFSET = Position(x=15.5, y=12, z=2)
SAMPLE_POSITION = Position(x=100, y=100, z=0)
SAMPLE_SIZE = 5 # millimeters


def test_bed_position(scraper):
    # TODO: function to help find a point on the bed
    return


scraper = Scraper()
scraper.connect()
atexit.register(scraper.disconnect)
scraper.home()
scraper.set_tool_offset(NEEDLE_TOOL_OFFSET)

# # find the TOOL-OFFSET
# scraper.move_to(Position(x=0, y=0, z=0), safe_z=20)

# # find the SAMPLE position
# scraper.move_to(SAMPLE_POSITION, safe_z=20)

# actually SCRAPE
scraper.scrape(SAMPLE_POSITION, SAMPLE_SIZE, speed=100, accel=100)
scraper.resting_position()

scraper.finish_moves()
