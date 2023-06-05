import logging


class LoggerFactory(object):
    _LOG = None

    @staticmethod
    def __create_logger(log_file, log_level):

        log_format = "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s"

        LoggerFactory._LOG = logging.getLogger(log_file)
        logging.basicConfig(level=logging.INFO,
                            format=log_format,
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename="log.log",
                            )

        if log_level == "INFO":
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == "ERROR":
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            LoggerFactory._LOG.setLevel(logging.DEBUG)
        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_file, log_level):

        logger = LoggerFactory.__create_logger(log_file, log_level)

        return logger


