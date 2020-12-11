import logging
from django.conf import settings

formatter = logging.Formatter('%(message)s')

BASE_DIR = settings.BASE_DIR

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# first file logger
first_logger = setup_logger('first_logger', BASE_DIR/'logs/first.log')

# second file logger
second_logger = setup_logger('second_logger', BASE_DIR/'logs/second.log')


def log1(orderID='-',owner='-',lattitude='-',longitude='-',dboy='-',amt='-',order_st='-',timeTaken='-'):
	msg="{}\\\\\\{}\\\\\\{},{}\\\\\\{}\\\\\\{}\\\\\\{}\\\\\\{}"
	msg=msg.format(orderID,owner,lattitude,longitude,dboy,amt,order_st,timeTaken)
	first_logger.info(msg)


def log2(dboy,kms,earnings,orders,drivingTime):
	msg = "{}\\\\\\{}\\\\\\{}\\\\\\{}\\\\\\{}"
	msg=msg.format(dboy,kms,earnings,orders,drivingTime)
	second_logger.info(msg)


	
