"""Core functions for darp"""

import argparse

from db import DBWrapper
from diff import ScanDiff
from arp_scan import ArpScan
from helpers import get_safe_timestamp
from tabulate import tabulate
import json
import time

def set_owners(database_path, owners_spec_json):
    """ Configures the database to associate the specified macs and owners """
    # print "decoding json spec", owners_spec_json
    owners_spec = json.loads(owners_spec_json)
    # print "owners_spec", owners_spec
    if owners_spec:
        dbwrapper = DBWrapper(database_path)

        for mac, owner in owners_spec.items():
            dbwrapper.set_owner(mac, owner)

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
    added_macs, removed_macs = diff.mac_difference()

    static_macs = [device.get('mac') for device in newDevices if 'mac' in device]

    if (removed_macs or added_macs):
        # if there are any alerts at all

        alerts['stamp'] = stamp

        if added_macs:
            alerts['added'] = []
            for added_mac in added_macs:
                alerts['added'].append(dbwrapper.get_meta(added_mac))
            static_macs = list(set(static_macs) - set(added_macs))

        if removed_macs:
            alerts['removed'] = []
            for removed_mac in removed_macs:
                alerts['removed'].append(dbwrapper.get_meta(removed_mac))

        if static_macs:
            """ only care about staic macs if there has been a change """
            alerts['static'] = []
            for static_mac in static_macs:
                alerts['static'].append(dbwrapper.get_meta(static_mac))

    return alerts

def print_alerts(alerts):
    """ prints a given alerts dictionary """
    if alerts:
        heading = "alerts"
        if 'stamp' in alerts:
            heading += ' at %s' % alerts['stamp']
            alerts.pop('stamp')
        print heading
        if 'added' in alerts:
            print ' -> added'
            print tabulate(alerts['added'], headers='keys')
            # for device in alerts['added']:
            #     print " -->", device
            alerts.pop('added')
        if 'removed' in alerts:
            print " -> removed"
            print tabulate(alerts['removed'], headers='keys')
            # for device in alerts['removed']:
            #     print " -->", device
            alerts.pop('removed')
        if 'static' in alerts:
            print " -> static"
            print tabulate(alerts['static'], headers='keys')
            alerts.pop('static')
        if alerts:
            print " -> other"
            for other_key, other_value in alerts.items():
                print " -->", other_key, other_value
    else:
        print "no alerts"

def main():
    """ Main function for Darp core """
    parser = argparse.ArgumentParser(description="detect changes on a subnet")
    parser.add_argument(
        '--db',
        help='The path of the database. e.g. darp_db.json',
        default='darp_db_default.json')
    parser.add_argument('--set-owners',
        help='Associates a mac with a persistent owner (specify with JSON) e.g.\
 --set-owners \'{"12:34:56:78:9a:bc":"Housemate A"}\'',)
    parser.add_argument(
        '--cycle',
        help='Instructs Darp to repeatedly check changes forecer')
    args = parser.parse_args()

    arp_scan_settings = {}

    if args:
        if args.db:
            db_path = args.db

            if args.set_owners:
                owners_spec_json = args.set_owners
                set_owners(db_path, owners_spec_json)

            if args.cycle:
                seconds = int(args.cycle)
                while True:
                    alerts = refresh_db(db_path, arp_scan_settings)
                    if alerts:
                        print_alerts(alerts)
                    time.sleep(seconds)
            else:
                alerts = refresh_db(db_path, arp_scan_settings)
                print_alerts(alerts)


if __name__ == '__main__':
    main()
