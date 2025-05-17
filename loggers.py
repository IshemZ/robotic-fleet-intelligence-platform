import logging
#import os
#from pathlib import Path

# Configuration du logger pour le module principal
loggers = logging.getLogger(__name__)

def do_something():
    loggers.info("Doing something...")
    loggers.debug("Debugging something...")
    loggers.warning("Warning: something might be wrong.")
    loggers.error("Error: something went wrong.")
    loggers.critical("Critical error: something is seriously wrong.")
#ROOT_DIR = Path(__file__).parent.resolve()

#os.makedirs("logs", exist_ok=True)

## Format commun
#log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d - %(module)s")
#
## Handler console
#console_handler = logging.StreamHandler()
#console_handler.setFormatter(log_format)
#console_handler.setLevel(logging.DEBUG)  # Niveau de log pour la console
#
## Handler fichier rotatif (5 fichiers de 1MB max)
#file_handler = RotatingFileHandler("logs/robot.log", maxBytes=1_000_000, backupCount=5)
#file_handler.setFormatter(log_format)
#file_handler.setLevel(logging.DEBUG)  # Niveau de log pour le fichier
#
## Crée le logger principal
#logger = logging.getLogger("robotic_platform")
#logger.setLevel(logging.DEBUG)
#
#sensor = logging.getLogger("robotic_platform.sensors.sensor")
#sensor.setLevel(logging.DEBUG)        
#navigation = logging.getLogger("robotic_platform.navigation")
#navigation.setLevel(logging.DEBUG)  

# Évite les doublons de handlers si le fichier est rechargé
#if not logger.handlers:
#    logger.addHandler(console_handler)
#    logger.addHandler(file_handler)
#    sensor.addHandler(console_handler)
#    sensor.addHandler(file_handler)
#    navigation.addHandler(console_handler)
#    navigation.addHandler(file_handler)