mport logging

#creates the logger
logger = logging.getlogger(__name__)
logger.setLevel(logging.DEBUG) #SET INFO, or error for prod

#create console dangler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s %(funcName)s():%(lineno)i: - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


