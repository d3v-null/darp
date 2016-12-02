"""Database intefaces for darp"""

from tinydb import TinyDB, where, Query

from helpers import get_safe_timestamp
from tabulate import tabulate

class DBWrapper(object):
    """ Provides wrapper for darp database """
    def __init__(self, db_path):
        self.database = TinyDB(db_path)

    #TODO: finish DBWrapper

    def insert_sighting(self, mac, address, name=None, stamp=None):
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

    def last_name(self, mac):
        """ gets the name that was most recently associated with this mac """
        if not mac:
            return

        sightings_table = self.database.table('sightings')
        # mac_name_sightings = sightings_table.search(where('mac') == mac)
        # mac_name_sightings = [sighting for sighting in mac_name_sightings if 'name' in sighting]

        mac_name_sightings = sightings_table.search(
            (Query().name.exists())
            & (Query().mac == mac)
        )
        mac_name_sightings = sorted(mac_name_sightings, key=(lambda r: r['stamp']))
        if mac_name_sightings:
            return mac_name_sightings[-1]['name']

    def stamped_sightings(self, stamp):
        """ Returns a list of the sightings that match a particular stamp """
        if not stamp:
            return

        sightings_table = self.database.table('sightings')
        stamp_sightings = sightings_table.search(where('stamp') == stamp)
        if stamp_sightings:
            return stamp_sightings

    def latest_scan(self):
        """ gets the latest scan, which is the list of signtings that correspond
            to the latest stamp """
        sightings = self.database.table('sightings')
        stamps = set([sighting.get('stamp') for sighting in sightings.all()])
        if stamps:
            latest_stamp = sorted(stamps)[-1]
            return self.stamped_sightings(latest_stamp)

    def get_owner(self, mac):
        """ gets the owner of a given mac """
        if not mac:
            return

        owners_table = self.database.table('owners')
        # owners = owners_table.search(where('mac') == mac)
        # owners = [owner for owner in owners if 'owner' in owner]

        owners = owners_table.search(
            (Query().mac == mac)
            & (Query().owner.exists())
        )

        owners = sorted(owners, key=(lambda r: r['stamp']))
        if owners:
            owner = owners[-1]['owner']
            return owner

    def set_owner(self, mac, owner):
        """ sets the owner of a given mac """
        if not (mac and owner):
            return

        stamp = get_safe_timestamp()
        owners_table = self.database.table('owners')
        owners_table.insert({
            'mac':mac,
            'owner':owner,
            'stamp':stamp
        })

    def get_meta(self, mac):
        """ attempts to get the meta data (name and owner) associated with a given mac """
        if not mac:
            return

        meta = {'mac':mac}
        name = self.last_name(mac)
        if name:
            meta['name'] = name
        owner = self.get_owner(mac)
        if owner:
            meta['owner'] = owner

        return meta


    def purge(self):
        self.database.purge_tables()
