import logging


def create_logger(name, filename='comms.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger
