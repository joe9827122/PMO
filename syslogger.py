#logger
import logging
import logging.config
import json
import os

class logger:
    def __init__(self, config_name = "logger.json", logger_name = "time-f"):
        with open(config_name) as f:
            data = json.load(f)
        filename = data['handlers']['time-rotating-file']['filename']
        dirPath = os.path.dirname( os.path.relpath(filename) )
        if ( os.path.isdir(dirPath) == False):
            os.mkdir(dirPath)

        logging.config.dictConfig(config=data)
        self.log = logging.getLogger(logger_name)
