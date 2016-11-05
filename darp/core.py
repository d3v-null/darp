"""Core functions for darp"""

import argparse

from db import DBWrapper
from diff import ScanDiff
from arp_scan import ArpScan
from helpers import get_safe_timestamp

def refresh_db(database_path, arp_scan_settings):
    """ Refreshes a darp database with the latest scan results, returning alerts """

    alerts = {}
    dbwrapper = DBWrapper(database_path)

    # do a scan
    newScan = ArpScan(**arp_scan_settings).results
    newDevices = []
    if newScan:
        newDevices = newScan.get('devices')

    # get latest scan
    oldDevices = dbwrapper.latest_scan()

    stamp = get_safe_timestamp()
    for device in newDevices:
        dbwrapper.insert_sighting(stamp=stamp, **device)

    # print "newDevices", newDevices
    # print "oldDevices", oldDevices

    # compare scans for alerts
    diff = ScanDiff(oldDevices, newDevices)
    added, removed = diff.mac_difference()

    if added:
        alerts['added'] = added

    if removed:
        alerts['removed'] = removed

    return alerts

def main():
    """ Main function for Darp core """
    parser = argparse.ArgumentParser(description="detect changes on a subnet")
    parser.add_argument('--db', help='The path of the database. e.g. darp_db.json',
                        default='darp_db_default.json')
    args = parser.parse_args()

    arp_scan_settings = {}

    if args:
        db_path = args.db

        alerts = refresh_db(db_path, arp_scan_settings)
        if alerts:
            print "alerts", alerts

if __name__ == '__main__':
    main()
