import logging
import subprocess
from logging.handlers import TimedRotatingFileHandler

# interval = 60
# ps aux | grep -e myScheduler.py | grep -v grep | awk '{print $2}'

logHandler = TimedRotatingFileHandler(filename="/home/pi/myTest.log", when="midnight", backupCount=10)
logFormatter = logging.Formatter('%(asctime)s %(message)s')
logHandler.setFormatter(logFormatter)
logger = logging.getLogger('mySchedulerLogger')
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

wireless_network = subprocess.check_output(['iwgetid', 'wlan0', '--raw']).strip()
type(wireless_network)
logger.info("Current network is: " + wireless_network.decode())

if wireless_network != "Morpheus3":
    logger.info("Network is not Morpheus3")
else:
    logger.info("Network IS Morpheus3")
