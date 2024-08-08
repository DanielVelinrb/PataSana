import logging
from datetime import datetime
import os

log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_filename = os.path.join(log_directory, datetime.now().strftime("log_%Y-%m-%d.log"))

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
                    filename=log_filename, 
                    filemode='a', 
                    level=logging.DEBUG)

def get_logger(name):
    return logging.getLogger(name)
