from bin.server import server
from packages.lib.module import location
from packages.lib.solarmodule import nearest_station, searchData, metricApplications
#from bin.client import client
import os
import argparse
import asyncio
import select

dir_base = os.path.dirname(os.path.abspath("./linuxServer"))
dir_data = os.path.join(dir_base, "data/")
#dir_bin = os.path.join(dir_base, "bin/")

if __name__ == '__main__':
    interface = ''
    port = 50000

    while True:
        server.server(interface, port)
        data = server.returnData()
  