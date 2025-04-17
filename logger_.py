import logging

logging.basicConfig(
    filename="Project1_logs.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger=logging.getLogger("Project1")