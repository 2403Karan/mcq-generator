import logging
import os
from datetime import datetime

# Create filename using current datetime
log_file = f"{datetime.now().strftime('%m_%d-%Y %H-%M-%S')}.log"

# Create logs directory path
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

# Full path to the log file
log_file_path = os.path.join(log_path, log_file)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

# Test log
logging.info("Logging system initialized.")
