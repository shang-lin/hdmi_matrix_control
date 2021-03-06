""" cli interface """
import argparse
import logging
import threading
import time

import serial

from . import driver, hw
from .web import flask_thread


def main():
    """
    Main cli entrypoint
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="count", help="increase output verbosity"
    )
    parser.add_argument(
        "-t", "--virtual", action="store_true", help="use test or virtual matrix"
    )
    args = parser.parse_args()
    loglevel = logging.ERROR
    if args.verbose == 1:
        loglevel = logging.WARNING
    elif args.verbose == 2:
        loglevel = logging.INFO
    elif args.verbose == 3:
        loglevel = logging.DEBUG

    logging.basicConfig(
        level=loglevel, format="(%(threadName)-13s)[%(levelname)-8s] %(message)s"
    )
    if args.virtual:
        serial_port = ""
        driver.DRIVER = hw.MatrixDriver()
    else:
        serial_port = serial.Serial("/dev/ttyUSB0")  # open serial port
        logging.debug(serial_port.name)
        time.sleep(20)
        driver.DRIVER = hw.TESmartMatrix(serial_port)
    driver.DRIVER.start()
    logging.debug("This is a debug.")
    logging.info("This is a info.")
    logging.warning("This is a warning.")
    logging.error("This is an error.")
    logging.critical("This is a critical.")

    thread1 = threading.Thread(target=flask_thread, name="webThread")
    thread1.start()
    thread1.join()
    driver.DRIVER.join()

    serial_port.close()


if __name__ == "__main__":
    main()
