"""Core functions for darp"""

import argparse

# from db import DBWrapper

def refresh_db(database_path, arp_scan_settings):
    """ Refreshes a darp database with the latest scan results, returning alerts """

    alerts = {}
    if arp_scan_settings or database_path:
        pass
    # dbwrapper = DBWrapper(database_path)
    #TODO: finish refresh_db

    return alerts

def main():
    """ Main function for Darp core """
    parser = argparse.ArgumentParser(description="detect changes on a subnet")
    parser.add_argument('--db', help='The path of the database. e.g. darp_db.json')
    args = parser.parse_args()

    arp_scan_settings = {}

    if args:
        db_path = args.db

        alerts = refresh_db(db_path, arp_scan_settings)
        if alerts:
            print str(alerts)

if __name__ == '__main__':
    main()
