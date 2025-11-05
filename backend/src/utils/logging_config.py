"""Logging configuration module for the application."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging(
    log_level: str = "INFO",
    log_dir: Path | None = None, 
    enable_file_logging: bool = True, 
    enable_console_logging: bool = True    
) -> None:  
    """Configure application-wide logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (default: backend/logs)
        enable_file_logging: Whether to write logs to files
        enable_console_logging: Whether to output logs to console
    """

    # Check if "log_dir" is being passed, else set it to standard /logs
    if log_dir is None: 
        log_dir = Path(__file__).parents[2] / "logs"
    log_dir.mkdir(exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    if enable_console_logging:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if enable_file_logging:
        file_handler = RotatingFileHandler(
            filename=log_dir / "app.log",
            maxBytes=10 * 1024 * 1024, # 10 MB
            backupCount=5,
            encoding="utf-8"
        )

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # When app is running at all times this created one error log for each day at midnight.
        """
        error_handler = TimedRotatingFileHandler(
            filename=log_dir / "error.log",
            when="midnight",
            interval=1,
            backupCount=30, 
            encoding="utf-8"
        )
        """

        # At this development stage, it's better to have a size based error handler. 
        error_handler = RotatingFileHandler(
            filename=log_dir / "error.log",
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=10,
            encoding="utf-8"
        )

        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)

    # Silence noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.INFO)

    logging.info("Logging system initialized")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)