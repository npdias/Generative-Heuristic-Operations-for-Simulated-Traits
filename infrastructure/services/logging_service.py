import logging
import os
from config import console_log_toggle, LOG_DIR
from datetime import datetime

os.makedirs(LOG_DIR, exist_ok=True)

# Store console handlers globally to manage toggles
console_handlers = {}

def setup_logger(name):
    """
    Sets up a logger with file and optional console logging.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger.
    """
    toggle_console_logs(console_log_toggle)
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"session_{session_id}.log")
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'))
        logger.addHandler(file_handler)

        # Console handler (disabled by default)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(levelname)s:\t%(funcName)s\t%(message)s'))
        logger.addHandler(console_handler)
        console_handlers[name] = console_handler
        console_handler.setLevel(logging.CRITICAL)  # Default to no console output

        logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Prevent propagation to the root logger
    return logger

def toggle_console_logs(enable: bool):
    """
    Toggles console logging for all loggers.

    Args:
        enable (bool): Whether to enable or disable console logs.
    """
    level = logging.DEBUG if enable else logging.CRITICAL
    for name, handler in console_handlers.items():
        handler.setLevel(level)
        logging.getLogger("logging_service").debug(
            f"Console logging {'enabled' if enable else 'disabled'} for {name}."
        )


# Example setup
memory_manager_logger = setup_logger("memory_manager")
chat_manager_logger = setup_logger("chat_manager")
coordinator_logger = setup_logger("coordinator")


