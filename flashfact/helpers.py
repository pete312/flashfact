import logging

DEFAULT_FORMAT = "%(asctime)s %(name)s %(module)s %(funcName)s line %(lineno)s %(levelname)s : %(message)s"

def setup_logger(logger, path_name=None, level="INFO", stdout=False, format=DEFAULT_FORMAT):
    formatter = logging.Formatter(format)
    logger.setLevel(logging.getLevelName(level))
    
    if path_name:
        loghandler = logging.handlers.RotatingFileHandler( path_name, maxBytes=300000, backupCount=5)
        loghandler.setFormatter(formatter)
        logger.addHandler(loghandler)
    
    if stdout:
        loghandler = logging.StreamHandler()
        loghandler.setFormatter(formatter)
        logger.addHandler(loghandler)
        
    if stdout is False and path_name is None:
        loghandler = logging.NullHandler()
        logger.addHandler(loghandler)
        
    return logger
    
    