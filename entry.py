import pygame as pg
import preload.ds as ds
import preload.constants as const
from comp.host import Host
from sys import exit
from preload.segment_tree import Node

import logging

logging.basicConfig(filename='test.log', format='%(filename)s: %(message)s',
                    level=logging.DEBUG)

with open('test.log', 'w'):
    pass

array = [1, 2, 3, 4, 5]
invalid_query_val = float("-inf")
query_function = update_function = max

host = Host(array, invalid_query_val, query_function, update_function)

def draw_node(node: Node):
    pg.draw.circle(ds.screen, "Black", (node.x, node.y), 20, 5)

    if not node.is_leaf():
        pg.draw.line(ds.screen, "Black", (node.x, node.y), (node.left.x, node.left.y), 5)
        pg.draw.line(ds.screen, "Black", (node.x, node.y), (node.right.x, node.right.y), 5)

    if node.is_leaf():
        return

root = host.st.root

def log(root: Node):
    logging.debug(f"{root.preliminary_x=}")
    logging.debug(f"{root.modifier=}")
    logging.debug(f"{root.ID=}\n")

    if not root.is_leaf():
        logging.debug(f"{root.left.preliminary_x=}")
        logging.debug(f"{root.left.modifier=}")
        logging.debug(f"{root.left.ID=}\n")

        logging.debug(f"{root.right.preliminary_x=}")
        logging.debug(f"{root.right.modifier=}")
        logging.debug(f"{root.right.ID=}\n")

        for child in root.children:
            log(child)

log(root)

while True:
    ds.screen.fill("White")
    ds.clock.tick(const.FPS)

    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
    
    host.update(events)
    pg.display.flip()