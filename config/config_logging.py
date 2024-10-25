import logging


def config_root(name=__name__, level=logging.INFO):
    filename = 'log.txt'

    formatter = logging.Formatter("%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(message)s")
    logging.getLogger(name).setLevel(level)

    # file handler
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logging.getLogger(name).addHandler(file_handler)

    # add stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logging.getLogger(name).addHandler(stream_handler)

    return logging.getLogger(name)
