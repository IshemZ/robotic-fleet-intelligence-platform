import logging
import loggers

loggers = logging.getLogger(__name__)

def move_forward():
    logging.basicConfig(filename="logs/robot.log", level=logging.DEBUG)
    loggers.info("Démarrage du mouvement")
    loggers.debug("Le robot avance")
    loggers.debug("Détails du mouvement : vitesse 1 m/s, direction nord")
    loggers.info("Le robot avance")
    loggers.warning("Proximité d’un obstacle")
    loggers.critical("Erreur critique : le robot est bloqué")
    loggers.info("Fin du mouvement")
    
if __name__ == "__main__":
    move_forward()
