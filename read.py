# coding=utf-8

from threading import Thread
import time


class LerSerial(Thread):
    def __init__(self, serial):
        Thread.__init__(self)

        self.serial = serial
        self.active = False

    def run(self):
        self.active = True

        out = ''
        while self.active:
            while self.serial.inWaiting() > 0:
                out += self.serial.read()

            if out != '':
                print out
                out = ''

            time.sleep(0.01)
