import json
import random
from datetime import datetime
from pathlib import Path
from time import sleep

class Settings:
    @staticmethod
    def load(self, object):
        self.version = object['version']
        self.startTime = object['application']['startTime']
        self.endTime = object['application']['endTime']
        self.sleep_interval = object['application']['visit-interval']
        self.sleep_interval_error = object['application']['visit-interval-error']

    def sleep(self):
        interval=self.sleep_interval * random.uniform(0.7, 1.3)
        sleep(interval)

    def sleep_error(self):
        interval=self.sleep_interval_error * random.uniform(0.7, 1.3)
        sleep(interval)

PATH=Path(__file__, "../settings.json").resolve()
SETTINGS=Settings()

def load_settings():
    global SETTINGS

    with open(PATH) as f:
        SETTINGS.load(SETTINGS, object = json.load(f))