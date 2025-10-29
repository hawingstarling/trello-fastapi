import logging
import sys
from pathlib import Path
from typing import Optional

from core.config import config

class LoggerFormatter(logging.Formatter):
  """
  Custom formatter with colors for console output
  """

  grey = "\x1b[38;21m"
  blue = "\x1b[38;5;39m"
  yellow = "\x1b[38;5;226m"
  red = "\x1b[38;5;196m"
  bold_red = "\x1b[31;1m"
  reset = "\x1b[0m"

  def __init__(self, fmt = None):
    super().__init__()
    self.fmt = fmt
    self.FORMATS = {
      logging.DEBUG: self.grey + self.fmt + self.reset,
      logging.INFO: self.blue + self.fmt + self.reset,
      logging.WARNING: self.yellow + self.fmt + self.reset,
      logging.ERROR: self.red + self.fmt + self.reset,
      logging.CRITICAL: self.bold_red + self.fmt + self.reset
    }

  def format(self, record):
    log_fmt = self.FORMATS.get(record.levelno)
    formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
    return formatter.format(record)

def setup_logger(
    name: str = __name__,
    level: Optional[int] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup logger with console and optional file handler
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        
    Returns:
        Configured logger
    """
    
    logger = logging.getLogger(name)
    
    # Set level
    if level is None:
        level = logging.DEBUG if config.DEBUG else logging.INFO
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    console_handler.setFormatter(LoggerFormatter(fmt))
    logger.addHandler(console_handler)
    
    # File Handler (optional)
    if log_file:
        Path("logs").mkdir(exist_ok=True)
        file_handler = logging.FileHandler(f"logs/{log_file}")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            fmt,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create default logger
logger = setup_logger("trello-fastapi", log_file="app.log")