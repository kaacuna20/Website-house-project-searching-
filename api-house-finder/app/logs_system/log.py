import logging
import sys

h = [
    logging.FileHandler("log.log"),
    logging.StreamHandler(stream=sys.stdout)
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=h
)

logger = logging.getLogger(__name__)

class Logger:
    
    def info(self, input_event):
        logging.info(input_event)
        
    def warning(self, input_event):
        logging.warning(input_event)
        
    def error(self, input_event):
        logging.error(input_event)
        
    def critical(self, input_event):
        logging.critical(input_event)