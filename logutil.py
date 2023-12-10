import logging
import os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('douyin_logger')
logger.setLevel(logging.DEBUG)
os.makedirs("./log",exist_ok=True)
fh = RotatingFileHandler('log/douyin.log', maxBytes=2000*1024*1024, backupCount=5)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)