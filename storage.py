import sqlite3

class Collection:
    """
    A Collection parent class that can be inherited from.
    Attributes: 
    (-) dbname: str -> The name of the database.
    (-) tblname: str -> The name of the table that the class is using.
    Methods:
    (+) insert(record) -> Inserts a record into the collection, after checking whether it is present.
    
    (+) update(key, record) -> Updates the record with the matching name, by replacing its elements with the given record.
    
    (+) find(key) -> Finds the record with a matching key and returns a copy of it.

    (+) findall() -> Returns all the records in the table from the database.

    (+) delete(key) -> Deletes the record with a matching key.
    """
    def __init__(self):
        pass
    def __repr__(self):
        pass

    def insert(self, record):
        pass

    def update(self, key, record):
        pass
        
    def find(self, key):
        pass

    def find_all(self):
        pass

    def delete(self, key):
        pass
