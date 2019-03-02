import datetime
import logging
import os
import subprocess
import time
from logging.handlers import TimedRotatingFileHandler

import schedule as schedule
from pushover import init, Client, RequestError

# interval = 60
start = datetime.time(17, 55, 0)
end = datetime.time(23, 5, 0)
my_exception_count = 0

logHandler = TimedRotatingFileHandler(filename="/home/pi/myScheduler.log", when="midnight", backupCount=10)
logFormatter = logging.Formatter('%(asctime)s %(message)s')
logHandler.setFormatter(logFormatter)
logger = logging.getLogger('mySchedulerLogger')
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

init("acwd9d9phzugsahyd4d25hcafr7o8s")


def send_message(title, message):
    try:
        Client("uwzge2h9rv1c2bex93dr3fqf6wc1qz").send_message(message, title=title)
    except RequestError as myError:
        logger.error("Could not send Pushover message")
        logger.error(myError)
    except Exception as ex:
        logger.error("General error sending pushover message")
        logger.error(ex)
    finally:
        global my_exception_count
        my_exception_count += 1


def time_in_range(my_start, my_end, my_current_time):
    """Return true if x is in the range [start, end]"""
    if my_start <= my_end:
        return my_start <= my_current_time <= my_end
    else:
        return my_start <= my_current_time or my_current_time <= my_end


def do_something():
    global my_exception_count
    current_time = datetime.datetime.now().time()
    wireless_network = subprocess.check_output(['iwgetid', 'wlan0', '--raw']).strip()
    logger.info("Current network is: " + wireless_network)

    if time_in_range(start, end, current_time):
        if wireless_network != "Morpheus2":
            logger.info(subprocess.check_output(['wpa_cli', '-i', 'wlan0', 'select_network', '0']))
            logger.info("Network changed to Morpheus2")
            send_message("Network changed to Morpheus2", "Internet Connection")
            logger.info("Message send complete")
    else:
        if wireless_network != "Morpheus3":
            logger.info(subprocess.check_output(['wpa_cli', '-i', 'wlan0', 'select_network', '1']))
            logger.info("Network changed to Morpheus3")
            send_message("Network changed to Morpheus3", "Internet Connection")
            logger.info("Message send complete")
    if my_exception_count >= 10:
        os.symlink("reboot")


schedule.every(1).minutes.do(do_something)

while 1:
    schedule.run_pending()
    time.sleep(1)

logger.info("Application came to an end!!")
