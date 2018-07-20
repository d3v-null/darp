"""Core functions for darp"""

from __future__ import print_function

import json
import time
from argparse import ArgumentParser

from arp_scan import ArpScan
from db import DBWrapper
from diff import ScanDiff
from helpers import get_safe_timestamp
from tabulate import tabulate


def set_owners(database_path, owners_spec_json):
    """ Configure the database to associate the specified macs and owners. """
    # print "decoding json spec", owners_spec_json
    owners_spec = json.loads(owners_spec_json)
    # print "owners_spec", owners_spec
    if owners_spec:
        dbwrapper = DBWrapper(database_path)

        for mac, owner in owners_spec.items():
            dbwrapper.set_owner(mac, owner)

def generate_mac_alerts(dbwrapper, oldDevices, newDevices, stamp):
    """ Generate alerts based on new and old devices detected. """
    alerts = {}

    # print "newDevices", newDevices
    # print "oldDevices", oldDevices

    # compare scans for alerts
    diff = ScanDiff(oldDevices, newDevices)
    added_macs, removed_macs = diff.mac_difference()

    static_macs = [device.get('mac') for device in newDevices if 'mac' in device]

    if not (removed_macs or added_macs):
        return alerts

    # if there are any alerts at all

    alerts['stamp'] = stamp

    if added_macs:
        static_macs = list(set(static_macs) - set(added_macs))

    for key, macs in [
        ('added', added_macs),
        ('removed', removed_macs),
        ('static', static_macs)
    ]:
        if macs:
            alerts[key] = []
            for mac in macs:
                alerts[key].append(dbwrapper.get_meta(mac))


    return alerts

def refresh_db(database_path, arp_scan_settings):
    """ Refresh a darp database with the latest scan results. """

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

    alerts = generate_mac_alerts(dbwrapper, oldDevices, newDevices, stamp)

    return alerts

def print_alerts(alerts):
    """ Print a given alerts dictionary. """
    if not alerts:
        print("no alerts")
        return

    out = "alerts"
    for type_ in ['stamp', 'added', 'removed', 'static']:
        if type_ not in alerts:
            continue
        if type_ == 'stamp':
            out += ' at %s' % alerts.pop(type_)
            continue
        out += '\n-> %s' % type_
        out += '\n%s' % tabulate(alerts.pop(type_), headers='keys')

    if alerts:
        out += '\n-> other'
        for other_key, other_value in alerts.items():
            out += "\n--> %s, %s" % (other_key, other_value)
    print(out)

def process_args(args, arp_scan_settings):
    if not args.db:
        return
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

    alerts = refresh_db(db_path, arp_scan_settings)
    print_alerts(alerts)

def main():
    """ Main function for Darp core. """
    parser = ArgumentParser(description="detect changes on a subnet")
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
        process_args(args, arp_scan_settings)



if __name__ == '__main__':
    main()
