"""Database intefaces for darp"""

from tinydb import TinyDB

class DBWrapper(object):
    """ Provides wrapper for darp database """
    def __init__(self, db_path):
        self.database = TinyDB(db_path)

    #TODO: finish DBWrapper
