"""
write log messages to text file and standard output
"""
import logging
import sys
import os

logger = logging.getLogger('space logger')
logger.setLevel(logging.INFO)

fmt='%(asctime)s | %(message)s'
format = logging.Formatter(fmt, datefmt='%m/%d/%Y %I:%M:%S %p')


handler = logging.FileHandler('space.log', mode='w')
handler.setFormatter(format)
logger.addHandler(handler)

if os.getenv("SPACE_LOG_STDOUT"):
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(format)
    logger.addHandler(handler)
