import logging
import logging


def setup_logger():
    # Create a logger
    logger = logging.getLogger('live_coding_editor')
    logger.setLevel(logging.INFO)

    # Create a formatter with HH:MM:SS date format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')

    # Create a file handler
    file_handler = logging.FileHandler('live_coding_editor.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    return