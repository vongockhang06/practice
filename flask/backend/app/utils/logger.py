# utils/logger.py
import logging
import sys

def setup_pipeline_logging(log_filename="pipeline.log"):
    """Configures centralized logging for files and console output."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) -> %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout) # 🌟 Production tip: Also prints out cleanly to terminal
        ]
    )
    return logging.getLogger("weather_pipeline")