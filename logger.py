from loguru import logger

logger.add(
    "app.log",
    rotation="10 MB",
    level="INFO",
    format="{time} | {level} | {message}"
)

def get_logger():
    return logger
