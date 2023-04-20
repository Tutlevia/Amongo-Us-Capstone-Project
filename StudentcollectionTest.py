from storage import StudentCollection

def test():
    sc = StudentCollection()
    
    name = "Jack"
    assert sc.find(name) == None, f"Found {name}, when not added"
    
    record = {"Name" : name,
              "Student_age" : 20,
              "Year_enrolled" : 2200,
              "Graduating_year" : 2220,
              "Class_name" : "Y1234"}
    
    print(f"Inserting {record}...")
    res = sc.insert(record)
    if res:
        print(f"Successfully added: {record['Name']}")
    else:
        print(f"Unsuccesfully added: {record['Name']}")
    
    print(f"Inserting {record} again...")
    res = sc.insert(record)
    if res:
        print(f"Successfully added: {record['Name']} again")
    else:
        print(f"Unsuccesfully added: {record['Name']} again")
    
    new_name = "JACKIE"
    record["Name"] = new_name
    print(record)
    
    print(f"Updating record with {name}...")
    res = sc.update(name, record)
    if res:
        print(f"Successfully updated record with {new_name} instead of {name}")
    else:
        print(f"Unsuccessfully updated record with {new_name} instead of {name}")
        
    print(f"Updating record with {name} again...")
    res = sc.update(name, record)
    if res:
        print(f"Successfully updated record with {new_name} instead of {name} again")
    else:
        print(f"Unsuccessfully updated record with {new_name} instead of {name} again")
    
    assert sc.find(name) == None, f"Found {name}, when not added"
    assert sc.find(new_name) != None, f"Failed to find {new_name} when already added"
    
    
    record2 = {"Name" : "Johnny",
              "Student_age" : 20,
              "Year_enrolled" : 2200,
              "Graduating_year" : 2220,
              "Class_name" : "Y1234"}
    
    print(sc.findall())
    
    print(f"Deleting record with {new_name}")
    sc.delete(new_name)
    sc.delete(record2["Name"])
    print(sc.findall())
    