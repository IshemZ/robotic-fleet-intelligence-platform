import logging
import loggers
from loggers import do_something

loggers = logging.getLogger(__name__)

def read_temperature():
    logging.basicConfig(filename="logs/robot.log", level=logging.DEBUG)
    loggers.info("Démarrage de la lecture de la température")
    loggers.do_something()
    loggers.debug("Lecture de la température en cours")

if __name__ == "__main__":
    read_temperature()