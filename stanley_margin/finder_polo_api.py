from datetime import datetime
import requests
import time
import poloniexAPI
import os
from urllib.request import urlopen



def current_time():
    current_time = datetime.now()
    print("Date Time:%s  " % (current_time))


def net_margin():
    net_margin = poloniexAPI.get_net_margin()
    print(": %s  " % (net_margin))


def lambda_handler(event, context):
    current_time()

    # current margin
    net_margin()
