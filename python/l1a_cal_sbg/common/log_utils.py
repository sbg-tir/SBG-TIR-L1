import logging
import os

def setup_log_file(log_file_path):
    """
    Set up the logging configuration.
    """
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logging.info(f"Log file created: {log_file_path}\n")

def log_message(message, level=logging.INFO):
    """
    Log a message to the configured log file.
    
    :param message: The message to log.
    :param level: The logging level, default is INFO.
    """
    if isinstance(level, int):
        logging.log(level, message)
    else:
        raise ValueError(f"Invalid logging level: {level}. Must be an integer corresponding to a valid logging level.")

def check_file_exists(file_path):
    """
    Check if a file exists and log the result.
    
    :param file_path: Path to the file to check.
    :return: Boolean indicating if the file exists.
    """
    if os.path.exists(file_path):
        log_message(f"File found: {file_path}")
        return True
    else:
        log_message(f"File not found: {file_path}", level=logging.WARNING)
        return False
