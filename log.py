import logging


def configure():
    logging.basicConfig(
        format='%(asctime)s  %(threadName)-25s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )