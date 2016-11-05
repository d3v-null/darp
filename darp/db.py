"""Database intefaces for darp"""

from tinydb import TinyDB, where

from helpers import get_safe_timestamp

class DBWrapper(object):
    """ Provides wrapper for darp database """
    def __init__(self, db_path):
        self.database = TinyDB(db_path)

    #TODO: finish DBWrapper

    def insert_sighting(self, mac, address, name, stamp=None):
        """ Inserts a sighting into the database """
        if not mac:
            return
        if not stamp:
            stamp = get_safe_timestamp()
        sightings = self.database.table('sightings')
        sightings.insert({
            'mac':mac,
            'address':address,
            'name':name,
            'stamp':stamp,
        })

    def last_sighting(self, mac):
        """ Returns the last sighting for a given mac """
        if not mac:
            return

        sightings = self.database.table('sightings')
        mac_sightings = sightings.search(where('mac') == mac)
        mac_sightings = sorted(mac_sightings, key=(lambda r: r['stamp']))
        if mac_sightings:
            return mac_sightings[-1]

    def stamped_sightings(self, stamp):
        """ Returns a list of the sightings that match a particular stamp """
        if not stamp:
            return

        sightings = self.database.table('sightings')
        stamp_sightings = sightings.search(where('stamp') == stamp)
        if stamp_sightings:
            return stamp_sightings

    def purge(self):
        self.database.purge_tables()
