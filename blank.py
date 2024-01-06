from datetime import datetime
import logging

logging.basicConfig(
    filename=f"EVSystem_{datetime.now().strftime('%Y%m%d%H%M%S')}.log",
    level=logging.DEBUG,
)
logging.info("test")
