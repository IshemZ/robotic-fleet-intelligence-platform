
from loggers import loggers, do_something
import logging
from loggers import do_something
from sensors.sensor import read_temperature
from navigation.navig import move_forward

loggers.info("Démarrage du robot")

read_temperature()
move_forward()

logger.info("Fin du programme")



