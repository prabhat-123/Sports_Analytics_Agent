from loguru import logger

# Add a log file named "my_logs.log" and set logging level to DEBUG
logger.add("my_logs.log", level="DEBUG")

def main():
    logger.info("This message will be logged to both console and 'my_logs.log'")
    logger.debug("This is a debug message")

if __name__ == "__main__":
    main()
