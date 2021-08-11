import logging
import math

from position import Position


logger = logging.getLogger('ender_3_test.scrape_planner')


def generate_scrape_lines_square(pos, width, step_size, horizontal=False, start='tl'):
    # get the start/end corners
    corners = {
        'tl': pos + Position(x=-width/2, y=width/2, z=pos.z),
        'tr': pos + Position(x=width/2, y=width/2, z=pos.z),
        'bl': pos + Position(x=-width/2, y=-width/2, z=pos.z),
        'br': pos + Position(x=width/2, y=-width/2, z=pos.z)
    }
    start_pos = corners.get(start)
    if start_pos is None:
        raise ValueError('Unknown start point: {0}'.format(start))

    # how much to increment on each step
    step_inc = None
    line_inc = None
    if horizontal:
        step_inc = Position(x=0, y=step_size, z=0)
        line_inc = Position(x=width, y=0, z=0)
        if start == 'tr' or start == 'tl':
            step_inc *= -1
        if start == 'tr' or start == 'br':
            line_inc *= -1
    else:
        step_inc = Position(x=step_size, y=0, z=0)
        line_inc = Position(x=0, y=width, z=0)
        if start == 'tr' or start == 'br':
            step_inc *= -1
        if start == 'tr' or start == 'tl':
            line_inc *= -1

    # generate the line
    num_steps = math.floor(width / step_size) + 1
    lines = []
    for i in range(int(num_steps)):
        if i != 0:
            start_pos += step_inc
        l = (start_pos.duplicate(), start_pos + line_inc)
        lines.append(l)

    # add the final leftover line
    leftover_step_scale = (width / step_size) % 1
    if leftover_step_scale != 0:
        step_inc *= leftover_step_scale
        start_pos += step_inc
        l = (start_pos.duplicate(), start_pos + line_inc)
        lines.append(l)

    return lines


if __name__ == '__main__':
    import sys

    logging.basicConfig(
        # filename='logfile.log',
        stream=sys.stdout, 
        filemode='w',
        format='%(levelname)s %(asctime)s - %(message)s', 
        level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    logger.debug('Test: Vertical - TL')
    lines = generate_scrape_lines_square(Position(x=0, y=0, z=0), 6.5, 1.5, horizontal=False, start='tl')
    for l in lines:
        logger.debug('{0} - {1}'.format(l[0], l[1]))
    logger.debug('Test: Vertical - BR')
    lines = generate_scrape_lines_square(Position(x=0, y=0, z=0), 5, 1, horizontal=False, start='br')
    for l in lines:
        logger.debug('{0} - {1}'.format(l[0], l[1]))
    logger.debug('Test: Horizontal - BR')
    lines = generate_scrape_lines_square(Position(x=0, y=0, z=0), 5, 1, horizontal=True, start='br')
    for l in lines:
        logger.debug('{0} - {1}'.format(l[0], l[1]))
