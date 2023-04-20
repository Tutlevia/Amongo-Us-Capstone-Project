import sqlite3
from typing import Optional, Union

class Collection:
    """
    A Collection parent class that can be inherited from.
    Attributes: 
    (-) dbname: str -> The name of the database.
    (-) tblname: str -> The name of the table that the class is using.
    (-) key: str -> Primary key for query in the table
    Methods:
    (+) insert(record) -> Inserts a record into the collection, after checking whether it is present.
    
    (+) update(key, record) -> Updates the record with the matching name, by replacing its elements with the given record.
    
    (+) find(key) -> Finds the record with a matching key and returns a copy of it.

    (+) findall() -> Returns all the records in the table from the database.

    (+) delete(key) -> Deletes the record with a matching key.
    """
    def __init__(self, dbname: str, tblname: str, key: str) -> None:
        self._dbname = dbname
        self._tblname = tblname
        self._key = key

    def _executedql(self, query: str, type: str, params: tuple) -> sqlite3.Row:
        '''
        A helper function that is used by self.find and self.findall to execute the Data Query Language in sqlite3

        Parameters:
        query: str -> SQL query to execute
        type: str -> Specifies the type of Search Query to execute
        Params: tuple -> Parameterised values to be used in query
        
        Return:
        result: sqlite3.Row -> the sql query result based on the query and type provided.
        '''
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            result = None
            #finding one entry in the table
            if type == 'one':
                cur.execute(query, params)
                result = cur.fetchone()
                
            #getting all entries in the table
            elif type == "many":
                cur.execute(query)
                result = cur.fetchall()
                
            #might want to add error message
            else:
                pass

            #conn.close()
            return result

    def _executedml(self, query: str, params: tuple) -> None:
        '''
        A helper function used to execute by self.insert, self.update, self.delete to execute Data Manipulation Lanaguage in sqlite3

        Parameter:
        query: str -> sqlite3 query to be executed
        params: tuple -> Paramterised values to be used in the query
        '''
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            #conn.close()
        return
        
    def __repr__(self):
        pass

    def insert(self, record: dict) -> bool:
        '''
        Inserts a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be added to the database

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''
    
        raise NotImplementedError
    
    def update(self, key: str, record: dict) -> bool:
        '''
        Updates the record with the matching name, by replacing its elements with the given record.

        Parameter:
        key: str -> used to identify the original entity
        record: dict-> used to modify the original entity

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''
        raise NotImplementedError
        
    def find(self, key: str) -> Optional[dict]:
        '''
        Finds the record with a matching key and returns a copy of it.

        Parameter:
        key: str -> Primary key used to identify the entity in the table

        Return:
        Returns the record of the entity in the form of a dictionary if found, else returns None
        '''

        query = f'''
                SELECT * FROM "{self._tblname}"
                WHERE "{self._key}" =?;
        '''
        result = self._executedql(query, "one", (key,))
        if result is not None:
            return dict(result)
        else:
            return None

    def findall(self) -> Optional[list[dict]]:
        '''
        Finds all entities in the table

        Parameter:
        None

        Return:
        Returns a list of dictionary storing all entities in the table if the table is not empty, else return None
        '''

        query = f'''
                SELECT * FROM "{self._tblname}";
        '''
        result = self._executedql(query, "many", (None,))

        if result is not None:
            lst = []
            for record in result:
                lst.append(dict(record))
            return lst
        else:
            return None
        

    def delete(self, key: str) -> bool:
        '''
        Deletes the record with a matching key

        Parameter:
        key: str -> Primary key used to find the record to be deleted

        Return:
        returns True if the record has been successfully deleted and False otherwise
        '''
        if self.find(key) is not None:
            query = f'''DELETE FROM "{self._tblname}" 
                    WHERE "{self._key}" = ?;
                    '''
            params = (key,)
            self._executedml(query, params)
            return True
        else:
            return False

#===========================================================================================================================================

class StudentCollection(Collection):
    """
    A collection class for student entities
    
    Attributes: 
    (-) dbname: str -> The name of the database.
    (-) tblname: str -> The name of the table that the class is using.
    (-) key: str -> Primary key for query in the table
    Methods:
    (+) insert(record) -> Inserts a record into the collection, after checking whether it is present.
    
    (+) update(key, record) -> Updates the record with the matching name, by replacing its elements with the given record.
    
    (+) find(key) -> Finds the record with a matching key and returns a copy of it.

    (+) findall() -> Returns all the records in the table from the database.

    (+) delete(key) -> Deletes the record with a matching key.
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "Student"
        super().__init__(self._dbname, self._tblname, "Name")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "Name" TEXT,
                "Student_age" INT,
                "Year_enrolled" INT,
                "Graduating_year" INT,
                "Class_name" TEXT,
                Primary Key("Name")
                Foreign Key("Class_name") REFERENCES Class("Name")
                );'''

                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record):
        '''
        Inserts a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be added to the database

        Return:
        Returns True if the record has successfully been added, False otherwise

        '''

        #checking if the record already exists
        if self.find(record[self._key]) is None:
            params = tuple(record.values())
            query = f'''
                    INSERT INTO "{self._tblname}"
                    VALUES (?,?,?,?,?);
                    '''
            self._executedml(query,params)
            return True
        else:
            return False
    def update(self, key: str, record: dict) -> bool:
        '''
        Updates the record with the matching name, by replacing its elements with the given record.

        Parameter:
        key: str -> used to identify the original entity
        record: dict-> used to modify the original entity

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''

        if self.find(key) is not None:
            params = (*tuple(record.values()), key)
            print(params)
            query = f'''UPDATE "{self._tblname}"
                    SET "Name" = ?,
                        "Student_age" = ?,
                        "Year_enrolled" = ?,
                        "Graduating_year" = ?,
                        "Class_name" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False
            
#===========================================================================================================================================

class ClassCollection(Collection):
    """
    A collection class for class entities
    
    Attributes: 
    (-) dbname: str -> The name of the database.
    (-) tblname: str -> The name of the table that the class is using.
    (-) key: str -> Primary key for query in the table
    Methods:
    (+) insert(record) -> Inserts a record into the collection, after checking whether it is present.
    
    (+) update(key, record) -> Updates the record with the matching name, by replacing its elements with the given record.
    
    (+) find(key) -> Finds the record with a matching key and returns a copy of it.

    (+) findall() -> Returns all the records in the table from the database.

    (+) delete(key) -> Deletes the record with a matching key.
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "Class"
        super().__init__(self._dbname, self._tblname, "Name")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "Name" TEXT,
                "Level" TEXT,
                Primary Key("Name")
                );'''
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record):
        '''
        Inserts a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be added to the database

        Return:
        Returns True if the record has successfully been added, False otherwise

        '''

        #checking if the record already exists
        if self.find(record[self._key]) is None:
            params = tuple(record.values())
            query = f'''
                    INSERT INTO "{self._tblname}"
                    VALUES (?,?);
                    '''
            self._executedml(query,params)
            return True
        else:
            return False
    def update(self, key: str, record: dict) -> bool:
        '''
        Updates the record with the matching name, by replacing its elements with the given record.

        Parameter:
        key: str -> used to identify the original entity
        record: dict-> used to modify the original entity

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''

        if self.find(key) is not None:
            params = (*tuple(record.values()), key)
            print(params)
            query = f'''UPDATE "{self._tblname}"
                    SET "Name" = ?,
                        "Level" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False
            
#===========================================================================================================================================

class SubjectCollection(Collection):
    """
    A collection class for subject entities
    
    Attributes: 
    (-) dbname: str -> The name of the database.
    (-) tblname: str -> The name of the table that the class is using.
    (-) key: str -> Primary key for query in the table
    Methods:
    (+) insert(record) -> Inserts a record into the collection, after checking whether it is present.
    
    (+) update(key, record) -> Updates the record with the matching name, by replacing its elements with the given record.
    
    (+) find(key) -> Finds the record with a matching key and returns a copy of it.

    (+) findall() -> Returns all the records in the table from the database.

    (+) delete(key) -> Deletes the record with a matching key.
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "Subject"
        super().__init__(self._dbname, self._tblname, "Name")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "Name" TEXT,
                "Level" TEXT,
                Primary Key("Name", "Level")
                );'''
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record):
        '''
        Inserts a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be added to the database

        Return:
        Returns True if the record has successfully been added, False otherwise

        '''

        #checking if the record already exists
        if self.find(record[self._key]) is None:
            params = tuple(record.values())
            query = f'''
                    INSERT INTO "{self._tblname}"
                    VALUES (?,?);
                    '''
            self._executedml(query,params)
            return True
        else:
            return False
    def update(self, key: str, record: dict) -> bool:
        '''
        Updates the record with the matching name, by replacing its elements with the given record.

        Parameter:
        key: str -> used to identify the original entity
        record: dict-> used to modify the original entity

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''

        if self.find(key) is not None:
            params = (*tuple(record.values()), key)
            print(params)
            query = f'''UPDATE "{self._tblname}"
                    SET "Name" = ?,
                        "Level" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False


#===========================================================================================================================================
class CCACollection(Collection):
    """
    A collection class for CCA entities
    
    Attributes: 
    (-) dbname: str -> The name of the database.
    (-) tblname: str -> The name of the table that the class is using.
    (-) key: str -> Primary key for query in the table
    Methods:
    (+) insert(record) -> Inserts a record into the collection, after checking whether it is present.
    
    (+) update(key, record) -> Updates the record with the matching name, by replacing its elements with the given record.
    
    (+) find(key) -> Finds the record with a matching key and returns a copy of it.

    (+) findall() -> Returns all the records in the table from the database.

    (+) delete(key) -> Deletes the record with a matching key.
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "CCA"
        super().__init__(self._dbname, self._tblname, "Name")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "Name" TEXT,
                "Type" TEXT,
                Primary Key("Name")
                );'''
                
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record):
        '''
        Inserts a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be added to the database

        Return:
        Returns True if the record has successfully been added, False otherwise

        '''

        #checking if the record already exists
        if self.find(record[self._key]) is None:
            params = tuple(record.values())
            query = f'''
                    INSERT INTO "{self._tblname}"
                    VALUES (?,?);
                    '''
            self._executedml(query,params)
            return True
        else:
            return False
    def update(self, key: str, record: dict) -> bool:
        '''
        Updates the record with the matching name, by replacing its elements with the given record.

        Parameter:
        key: str -> used to identify the original entity
        record: dict-> used to modify the original entity

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''

        if self.find(key) is not None:
            params = (*tuple(record.values()), key)
            print(params)
            query = f'''UPDATE "{self._tblname}"
                    SET "Name" = ?,
                        "Type" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False
#===========================================================================================================================================

class ActivityCollection(Collection):
    """
    A collection class for Activity entities
    
    Attributes: 
    (-) dbname: str -> The name of the database.
    (-) tblname: str -> The name of the table that the class is using.
    (-) key: str -> Primary key for query in the table
    Methods:
    (+) insert(record) -> Inserts a record into the collection, after checking whether it is present.
    
    (+) update(key, record) -> Updates the record with the matching name, by replacing its elements with the given record.
    
    (+) find(key) -> Finds the record with a matching key and returns a copy of it.

    (+) findall() -> Returns all the records in the table from the database.

    (+) delete(key) -> Deletes the record with a matching key.
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "Activity"
        super().__init__(self._dbname, self._tblname, "Name")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "Name" TEXT,
                "Start_date" TEXT,
                "End_date" TEXT,
                "Description" TEXT,
                "Category" TEXT,
                "Role" TEXT,
                "Award" TEXT,
                "Hour" INT,
                "CCA_name" TEXT,
                Primary Key("Name")
                Foreign Key("CCA_name") REFERENCES CCA("Name")
                );'''
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record):
        '''
        Inserts a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be added to the database

        Return:
        Returns True if the record has successfully been added, False otherwise

        '''

        #checking if the record already exists
        if self.find(record[self._key]) is None:
            params = tuple(record.values())
            query = f'''
                    INSERT INTO "{self._tblname}"
                    VALUES (?,?,?,?,?,?,?,?,?);
                    '''
            self._executedml(query,params)
            return True
        else:
            return False
    def update(self, key: str, record: dict) -> bool:
        '''
        Updates the record with the matching name, by replacing its elements with the given record.

        Parameter:
        key: str -> used to identify the original entity
        record: dict-> used to modify the original entity

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''

        if self.find(key) is not None:
            params = (*tuple(record.values()), key)
            print(params)
            query = f'''UPDATE "{self._tblname}"
                    SET "Name" = ?,
                        "Start_date" = ?,
                        "End_date" = ?,
                        "Description" = ?,
                        "Category" = ?,
                        "Role" = ?,
                        "Award" = ?,
                        "Hour" = ?,
                        "CCA_name" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False
            
#===========================================================================================================================================