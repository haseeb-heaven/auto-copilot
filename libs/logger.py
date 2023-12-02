import logging



class Logger:
    logger = None

    @staticmethod
    def setup_logger():
        if Logger.logger is None:
            # Create a logger
            Logger.logger = logging.getLogger('auto-copilot')
            Logger.logger.setLevel(logging.INFO)

            # Create a formatter with HH:MM:SS date format
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')

            # Create a file handler
            file_handler = logging.FileHandler('auto-copilot.log')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)

            # Add the handler to the logger
            Logger.logger.addHandler(file_handler)

        return Logger.logger
