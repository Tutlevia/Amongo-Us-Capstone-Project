import sqlite3
from typing import Optional

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

    def _executedql(self, query: str, type: str, params: tuple) -> Optional[sqlite3.Row]:
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

            elif type == "join":
                cur.execute(query, params)
                result = cur.fetchall()

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

        if result != []:
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

    (+) viewactivity(key) -> Returns all activity a given student is involved in
    
    (+) viewclass(key) -> Returns the class of the given student

    (+) viewcca(key) -> Return the cca of the given student

    (+) viewall() -> Returns all information about student, their class and cca
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "Student"
        super().__init__(self._dbname, self._tblname, "id")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "id" TEXT UNIQUE,
                "name" TEXT,
                "student_age" INT,
                "year_enrolled" INT,
                "graduating_year" INT,
                "class_id" TEXT,
                Primary Key("id")
                Foreign Key("class_id") REFERENCES Class("id")
                );'''

                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record) -> bool:
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
                    VALUES (?,?,?,?,?,?);
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
                    SET "name" = ?,
                        "student_age" = ?,
                        "year_enrolled" = ?,
                        "graduating_year" = ?,
                        "class_id" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False

    def viewactivity(self, key: str) -> Optional[list[dict]]:
        '''
        Views all the activity of the record with the matching name.

        Parameter:
        key: str -> used to identify the original entity

        Return:
        Returns a list of dictionary for the activities that the student took part in if they exists, else return None
        '''

        query = f'''SELECT "Activity"."id" as "id",
                           "Activity"."name" as "name",
                           "Activity"."start_date" as "start_date",
                           "Activity"."end_date" as "end_date",
                           "Activity"."hours" as "hours"
                    FROM "StudentActivity"
                    INNER JOIN "{self._tblname}"
                        ON "StudentActivity"."student_id" = "{self._tblname}"."id"
                    INNER JOIN "Activity"
                        ON "StudentActivity"."activity_id" = "Activity"."id"
                    WHERE "Student"."id" = ?                  
                    ORDER BY "Activity"."id";
                '''
        result = self._executedql(query, "join", (key,))
        if result != []:
            lst = []
            for record in result:
                lst.append(dict(record))
            return lst
        else:
            return None

    def viewclass(self, key: str) -> Optional[str]:
        '''
        Returns the class of the given student

        Parameter:
        key: str -> the student id to be queried

        Returns:
        Returns the class of the given student if it exists, else returns None
        '''

        query = f'''
                SELECT "Class"."name" as "class"
                FROM "{self._tblname}"
                INNER JOIN "Class"
                        ON "Class"."id" = "{self._tblname}"."class_id" 
                WHERE "{self._tblname}"."{self._key}" =?;
                '''
        result = self._executedql(query, "one", (key,))
        if result is not None:
            return str(dict(result)["class"])
        else:
            return None
            
    def viewcca(self, key: str) -> Optional[str]:
        '''
        Returns the cca of the given student

        Parameter:
        key: str -> the student id to be queried

        Returns:
        Returns the cca of the given student if it exists, else returns None
        '''

        query = f'''
                SELECT "CCA"."name" as "CCA"
                FROM "StudentCCA"
                INNER JOIN "CCA"
                       ON "StudentCCA"."cca_id" = "CCA"."id"
                INNER JOIN "{self._tblname}"
                       ON "StudentCCA"."student_id" = "{self._tblname}"."{self._key}"
                WHERE "{self._tblname}"."{self._key}" =?;
                '''
        result = self._executedql(query, "one", (key,))
        if result is not None:
            return str(dict(result)["CCA"])
        else:
            return None

    def viewall(self) -> Optional[dict]:
        '''
        Returns all info about every student
        '''

        query = f'''
                SELECT "Student"."id", "Student"."name", "Student"."student_age", "Student"."year_enrolled", "Student"."graduating_year", "CCA"."name", "Class"."name"
                FROM StudentCCA
                INNER JOIN "CCA"
                       ON "StudentCCA"."cca_id" = "CCA"."id"
                INNER JOIN "Student"
                       ON "StudentCCA"."student_id" = "Student"."id"                           INNER JOIN "Class"
                        ON "Class"."id" = "Student"."class_id" 
                ORDER BY "Student"."id";
                '''
        result = self._executedql(query, "many", (None,))

        if result != []:
            lst = []
            for record in result:
                lst.append(dict(record))
            return lst
        else:
            return None
        
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

    (+) viewstudent(key) -> Returns all the records of student from a class
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "Class"
        super().__init__(self._dbname, self._tblname, "id")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "id" TEXT UNIQUE,
                "name" TEXT,
                "level" TEXT,
                Primary Key("id")
                );'''
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record) -> bool:
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
                    VALUES (?,?,?);
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
                    SET "name" = ?,
                        "level" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False
            
    def viewstudent(self, key: str) -> Optional[list[dict]]:
        '''
        Views all the student record with the matching class id.

        Parameter:
        key: str -> used to identify the original entity

        Return:
        Returns a list of dictionary for the students that are in a class if they exists, else return None
        '''
        query = f'''SELECT "Student"."id" as "id",
                           "Student"."name" as "name",
                           "Class"."name" as "class"
                    FROM "{self._tblname}"
                    INNER JOIN "Student"
                        ON "Class"."id" = "Student"."class_id" 
                    WHERE "Class"."id" = ?
                    ORDER BY "Student"."id";                    
                '''
        result = self._executedql(query, "join", (key,))
        if result != []:
            lst = []
            for record in result:
                lst.append(dict(record))
            return lst
        else:
            return None
        
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
        super().__init__(self._dbname, self._tblname, "id")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "id" TEXT UNIQUE,
                "name" TEXT,
                "level" TEXT,
                Primary Key("id")
                );'''
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record) -> bool:
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
                    VALUES (?,?,?);
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
                    SET "name" = ?,
                        "level" = ?
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

    (+) viewstudent(key) -> Returns all the record of student in a matching CCA
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "CCA"
        super().__init__(self._dbname, self._tblname, "id")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "id" TEXT UNIQUE,
                "name" TEXT,
                "type" TEXT,
                Primary Key("id")
                );'''
                
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record) -> bool:
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
                    VALUES (?,?,?);
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
                    SET "name" = ?,
                        "type" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False

    def viewstudent(self, key: str) -> Optional[list[dict]]:
        '''
        Views all the student record with the matching CCA

        Parameter:
        key: str -> used to identify the original entity

        Return:
        Returns a list of dictionary for the students that are in a CCA if they exists, else return None
        '''

        query = f'''SELECT "Student"."id" as "id",
                           "Student"."name" as "name",
                           "Class"."name" as "class"
                    FROM "StudentCCA"
                    INNER JOIN "{self._tblname}"
                        ON "StudentCCA"."cca_id" = "CCA"."id"
                    INNER JOIN "Student"
                        ON "StudentCCA"."student_id" = "Student"."id"
                    INNER JOIN "Class"
                        ON "Student"."class_id" = "Class"."id"
                    WHERE "CCA"."id" = ?
                    ORDER BY "Student"."id";
                '''
        result = self._executedql(query, "join", (key,))
        if result != []:
            lst = []
            for record in result:
                lst.append(dict(record))
            return lst
        else:
            return None

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

    (+) viewstudent(key) -> Returns all students given an activity
    """

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "Activity"
        super().__init__(self._dbname, self._tblname, "id")
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "id" TEXT UNIQUE,
                "name" TEXT,
                "start_date" TEXT,
                "end_date" TEXT,
                "description" TEXT,
                "category" TEXT,
                "role" TEXT,
                "award" TEXT,
                "hours" INT,
                "cca_id" TEXT,
                Primary Key("id")
                Foreign Key("cca_id") REFERENCES CCA("id")
                );'''
                
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

    def insert(self, record) -> bool:
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
                    VALUES (?,?,?,?,?,?,?,?,?,?);
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
                    SET "name" = ?,
                        "start_date" = ?,
                        "end_date" = ?,
                        "description" = ?,
                        "category" = ?,
                        "role" = ?,
                        "award" = ?,
                        "hours" = ?,
                        "cca_id" = ?
                    WHERE {self._key} = ?;
            '''
            self._executedml(query, params)
            return True
        else:
            return False

    def viewstudent(self, key: str) -> Optional[list[dict]]:
        '''
        Views all the student record with the matching activity name.

        Parameter:
        key: str -> used to identify the original entity

        Return:
        Returns a list of dictionary for the students that took part in an activity if they exists, else return None
        '''

        query = f'''SELECT "Student"."id" as "id",
                           "Student"."name" as "name",
                           "Class"."name" as "class"
                    FROM "StudentActivity"
                    INNER JOIN "{self._tblname}"
                        ON "StudentActivity"."student_id" = "Activity"."id"
                    INNER JOIN "Student"
                        ON "StudentActivity"."activity_id" = "Student"."id"
                    INNER JOIN "Class"
                        ON "Student"."class_id" = "Class"."id"
                    WHERE "Activity"."id" = {key}
                    ORDER BY "Student"."id";
                '''
        result = self._executedql(query, "join", (key,))
        if result != []:
            lst = []
            for record in result:
                lst.append(dict(record))
            return lst
        else:
            return None
        
            
#===========================================================================================================================================

class Junctiontable:
    '''
    A base junction table class that can be inherited from.
    
    Attribute:
    (-) dbname: str -> The name of the database
    (-) tblname: str -> The name of the junction table
    (-) leftkey: str -> The key of the left table in the junction table
    (-) rightkey: str -> The key of the right table in the junction table

    Methods:
    (+) find(record) -> check if a certain record exists
    
    (+) insert(record) -> Inserts a record into the junction table, after checking whether it is present.

    (+) update(old_record, new_record) -> Updates a record in the junction table, after checking whether it is present. 

    (+) delete(record) -> Delete a record in the junction table, after checking whether it is present.
    
    '''

    def __init__(self, dbname: str, tblname: str, left_key: str, right_key: str):
        self._dbname = dbname
        self._tblname = tblname
        self._leftkey = left_key
        self._rightkey = right_key

    def _executedql(self, query: str, type: str, params: tuple) -> Optional[sqlite3.Row]:
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
                cur.execute(query, params)
                result = cur.fetchall()
                
            elif type == "join":
                cur.execute(query, params)
                result = cur.fetchall()

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

    def find(self, record: dict) -> bool:
        '''
        Checks if a certain record exists within the junction table given the record

        Parameter:
        record: dict -> A dictionary containing the record to be checked if it exists

        Return:
        Returns True if the record is found, False if it is not found
        '''
        query = f'''SELECT * FROM {self._tblname}
                    WHERE {self._leftkey} = ? and {self._rightkey} = ?;'''
        key = tuple(record.values())
        result = self._executedql(query, "one", key)
        if result is not None:
            return True
        return False


    def insert(self, record: dict) -> bool:
        '''
        Inserts a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be added to the database

        Return:
        Returns True if the record has successfully been added, False otherwise
        '''
        if self.find(record) is not True:
            query = f'''INSERT INTO "{self._tblname}"
                        VALUES(?,?);'''
    
            params = tuple(record.values())
            self._executedml(query, params)
            return True
        else:
            return False
        
    def update(self, old_record: dict, new_record: dict) -> bool:
        '''
        Updates a record into the collection, after checking whether it is present.

        Parameter:
        old_record: dict -> A dictionary containing the record of the old entity to be updated from the database
        new_record: dict -> A dictionary containing the record of the entity to be updated to the database

        Return:
        Returns True if the record has successfully been updated, False otherwise
        '''
        if self.find(old_record):
            values = tuple(new_record.values()) + tuple(old_record.values())
            query = f'''UPDATE "{self._tblname}"
                        SET "{self._leftkey}" = ?,
                            "{self._rightkey}" = ?
                        WHERE "{self._leftkey}" = ? and
                              "{self._rightkey}" = ?;
                        '''
            self._executedml(query, values)
            return True
        else:
            return False

    def delete(self, record: dict) -> bool:
        '''
        Updates a record into the collection, after checking whether it is present.

        Parameter:
        record: dict -> A dictionary containing the record of the entity to be deleted from the database


        Return:
        Returns True if the record has successfully been deleted, False otherwise
        '''
        
        if self.find(record):
            values = tuple(record.values())
            query = f'''DELETE FROM "{self._tblname}"
                        WHERE {self._leftkey} = ? and {self._rightkey} = ?;
                        '''
            self._executedml(query, values)
            return True
        else:
            return False
#===========================================================================================================================================

class StudentActivity(Junctiontable):
    '''
    A StudentActivity class used to modify the junction table between the Student class and Activity class
    
    Attribute:
    (-) dbname: str -> The name of the database
    (-) tblname: str -> The name of the junction table
    (-) leftkey: str -> The key of the left table in the junction table
    (-) rightkey: str -> The key of the right table in the junction table

    Methods:
    (+) find(record) -> check if a certain record exists
    
    (+) insert(record) -> Inserts a record into the junction table, after checking whether it is present.

    (+) update(old_record, new_record) -> Updates a record in the junction table, after checking whether it is present. 

    (+) delete(record) -> Delete a record in the junction table, after checking whether it is present.
    '''

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "StudentActivity"
        keys = ("student_id", "activity_id")

        super().__init__(self._dbname, self._tblname, keys[0], keys[1])
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "student_id" TEXT,
                "activity_id" TEXT,
                Foreign Key("student_id") REFERENCES Student("id")
                Foreign Key("activity_id") REFERENCES Activity("id")
                );'''

        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()

#===========================================================================================================================================


class StudentCCA(Junctiontable):
    '''
    A StudentCCA class used to modify the junction table between the Student class and CCA class
    
    Attribute:
    (-) dbname: str -> The name of the database
    (-) tblname: str -> The name of the junction table
    (-) leftkey: str -> The key of the left table in the junction table
    (-) rightkey: str -> The key of the right table in the junction table

    Methods:
    (+) find(record) -> check if a certain record exists
    
    (+) insert(record) -> Inserts a record into the junction table, after checking whether it is present.

    (+) update(old_record, new_record) -> Updates a record in the junction table, after checking whether it is present. 

    (+) delete(record) -> Delete a record in the junction table, after checking whether it is present.
    '''

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "StudentCCA"
        keys = ("student_id", "cca_id")

        super().__init__(self._dbname, self._tblname, keys[0], keys[1])
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "student_id" TEXT,
                "cca_id" TEXT,
                Foreign Key("student_id") REFERENCES Student("id")
                Foreign Key("cca_id") REFERENCES CCA("id")
                );'''

        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()
#===========================================================================================================================================

class StudentSubject(Junctiontable):
    '''
    A StudentSubject class used to modify the junction table between the Student class and Subject class
    
    Attribute:
    (-) dbname: str -> The name of the database
    (-) tblname: str -> The name of the junction table
    (-) leftkey: str -> The key of the left table in the junction table
    (-) rightkey: str -> The key of the right table in the junction table

    Methods:
    (+) find(record) -> check if a certain record exists
    
    (+) insert(record) -> Inserts a record into the junction table, after checking whether it is present.

    (+) update(old_record, new_record) -> Updates a record in the junction table, after checking whether it is present. 

    (+) delete(record) -> Delete a record in the junction table, after checking whether it is present.
    '''

    def __init__(self):
        self._dbname = "MyWebApp.db"
        self._tblname = "StudentSubject"
        keys = ("student_id", "subject_id")

        super().__init__(self._dbname, self._tblname, keys[0], keys[1])
        self._create_table()

    def _create_table(self):
        """
        A helper function used to create the table in the database for the entity collection if it does not already exists
        """
        
        query = f'''CREATE TABLE IF NOT EXISTS "{self._tblname}"(
                "student_id" TEXT,
                "subject_id" TEXT,
                Foreign Key("student_id") REFERENCES Student("id")
                Foreign Key("subject_id") REFERENCES Subject("id")
                );'''

        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            #conn.close()
#===========================================================================================================================================