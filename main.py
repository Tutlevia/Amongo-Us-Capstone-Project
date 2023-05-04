from flask import Flask, render_template, request
from storage import StudentCollection, SubjectCollection, CCACollection, ClassCollection, ActivityCollection, StudentActivity, StudentCCA, StudentSubject

studentCollection = StudentCollection()
subjectCollection = SubjectCollection()
ccaCollection = CCACollection()
classCollection = ClassCollection()
activityCollection = ActivityCollection()
studentActivityCollection = StudentActivity()
studentCCACollection = StudentCCA()
studentSubjectCollection = StudentSubject()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html") 

@app.route('/add_cca', methods=['GET', 'POST'])
def add_cca():
    title = "Add a new CCA"
    span1 = "Register a new CCA"
    span2 = "Use the following form to register a new CCA:"
    form_header = {"id": "CCA ID",
                   "name": "CCA Name",
                   "type":"CCA Type"
    }
    error = " "
    
    if 'confirm' in request.args:
        span1 = 'Register a new CCA(Submission)'
        span2 = 'Please confirm the following details below:'
        return render_template("add.html",
                           page_type = 'confirm_cca',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_meta={
                               'action': '/add_cca?attempted',
                               'method': 'post'
                           },
                           form_data =  dict(request.form)
                          )
    if 'attempted' in request.args:
        record = dict(request.form)

        for key, value in record.items():
            record[key] = record[key].strip(" ")
        
        insertSuccess = ccaCollection.insert(record)

        if insertSuccess is True: 
            span1 = 'Register a new CCA(Success)'
            span2 = 'The following CCA has been registered!'
            return render_template("add.html",
                               page_type = 'success_cca',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_data = dict(request.form)
                              )
        else:
            error = "Error: A CCA record with the same ID already exists in the database!"
        
    
    return render_template("add.html",
                           page_type = 'add_cca',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           error = error,
                           form_header = form_header,
                           form_meta={
                               'action': '/add_cca?confirm',
                               'method': 'post'
                           },
                           form_data =  {
                               'id': " ",
                               'name': " ",
                               "type": " "
                           }  
                          )

@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    title = "Add a new Activity"
    span1 = "Register a new Activity"
    span2 = "Use the following form to register a new Activity:"
    form_header = {
                  "id": "Activity ID",
                  "name": "Name",
                  "start_date": "Start Date (YYYYMMDD)",
                  "end_date": "End Date (YYYYMMDD)",
                  "description": "Description",
                  "category": "Category",
                  "role": "Role",
                  "award": "Award",
                  "hours": "Hours",
                  "cca" : "CCA"
    }
    ccalist = [{'name':"Basketball",
                 'id':'1'
               }, 
               {'name':"Tchoukball",
                'id':'2'
               }]
    error = " "
        
    if 'confirm' in request.args:
        print(request.form['id'])
        span1 = "Register a new Activity(Submission)"
        span2 = "Please confirm the following details below:"
        return render_template("add.html",
                           page_type = 'confirm_activity',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_meta={
                               'action': '/add_activity?attempted',
                               'method': 'post'
                           },
                           form_data = dict(request.form)
                          )
    if 'attempted' in request.args:

        record = dict(request.form)
        for key, value in record.items():
            if(key == 'hours'):
                record[key] = int(record[key])
            else:
                record[key] = record[key].strip(" ")
    
        insertSuccess = activityCollection.insert(record)

        if insertSuccess is True:
            span1 = "Register a new Activity(Success)"
            span2 = "The following Activity has been registered!"
            return render_template("add.html",
                               page_type = 'success_activity',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_data =  dict(request.form)
                              )
        else: 
            error = "Error: An activity record with the same ID already exists in the database!"
    return render_template("add.html",
                            
                           page_type = 'add_activity',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           error = error,
                           form_header = form_header,
                           ccalist = ccalist,
                           form_meta = {
                               'action': '/add_activity?confirm',
                               'method': 'post'
                           },
                           form_data = {
                               "id": " ",
                               "name": " ",
                               "start_date": " ",
                               "end_date": " ",
                               "description" : " ",
                               "category": " ",
                               "role": " ",
                               "award": " ",
                               "hours": " ",
                               'cca' : " ",
                           }
                          )


@app.route('/view/student', methods=['GET', 'POST'])
def view_student():
    title = "View a Student"
    span1 = "View a Student"
    span2 = "Use the following form to view a Student"
    form_header = {"id": "Student ID"}
    error = " "
    
    if request.args:
        id = request.args['id'].strip(" ")
        record = studentCollection.find(id)
        
        if record != None:
            # studentClass = studentCollection.viewclass(id)
            # studentCCAs = studentCollection.viewcca(id)
            studentClass = {'name':'2227',
                           'id':'1'}
            # studentCCAs = [{'name':'toiletcleaner',
            #                'id':'1'}]
            studentCCAs = None
            studentActivities = studentCollection.viewactivity(id)
            
            span1 = "View a Student(Success)"
            span2 = "Here are the students details:"
            form_header = {
                'id': 'ID',
                'name': 'Name',
                'student_age': 'Student Age',
                'year_enrolled': 'Year Enrolled',
                'graduating_year': 'Graduating Year',
                'class_id': 'Class ID',      
            }
            table_header = {
                'id' : 'Activity ID',
                'name': 'Name',
                'start_date': 'Start Date',
                'end_date': 'End Date',
                'hours': 'Hours'
            }
            table_header2 ={
                'id': 'CCA ID',
                'name': 'Name'
            }
            return render_template("view.html",
                               page_type = 'success_student',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               table_header = table_header,
                               table_header2 = table_header2,
                               form_meta={
                                   'action': '/view/student?success',
                                   'method': 'get'
                               },
                               form_data ={
                                   'record':record,
                                   'class':studentClass,
                                   'activities':studentActivities,
                                   'ccas':studentCCAs,
                               }
                              )
        else:
            error = f'Student ID {request.args["id"]} not found! Try again!' 
    
    return render_template("view.html",
                           page_type = "view_student",
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           error = error,
                           form_meta = {
                                'action': ' ',
                                'method': 'get'
                            },
                           form_data = {
                                "id": " "
                            }
                          )

@app.route('/view/class', methods = ["GET", 'POST'])
def view_class():
    title = 'View a Class'
    span1 = "View a Class"
    span2 = "Use the following form to view a Class"
    form_header = {"id": "Class ID"}
    error = ' '

    if request.args:
        record = classCollection.find(request.args['id'])
        if record != None:
            students = classCollection.viewstudent(request.args['id'])
            span1 = "View a Class(Success)"
            span2 = "Here are the Class details:"
            form_header = {
                           'id' : 'Class ID',
                           'name': 'Name',
                           'level': 'Level'
                               }
            return render_template("view.html",
                               page_type = 'success_class',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_meta={
                                   'action': '',
                                   'method': 'get'
                               },
                               form_data =  record,
                               students = students
                              )
        else: 
            error = f'Class ID {request.args["id"]} not found! Try again!'
    
    return render_template("view.html",
                           page_type = "view_class",
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           error = error,
                           form_header = form_header,
                           form_meta = {
                                'action': '/view/class?confirm',
                                'method': 'get'
                            },
                           form_data = {
                                "id": " "
                            }
                          )

@app.route('/view/cca', methods = ["GET", 'POST'])
def view_cca():
    title = 'View a CCA'
    span1 = "View a CCA"
    span2 = "Use the following form to view a CCA"
    form_header = {"id": "CCA ID"}
    error = ' '
    record = {
        'id' : 1,
        'name': 'Tchoukball',
        'type': 'Sports'
    }
    students = [
        {
            'id': 1,
            'name': 'john',
            'class_id': 2227
        },
        {
            'id': 2,
            'name': 'nolan',
            'class_id': 2228
        }
        
    ]

    if request.args:
        # record = SC.find(request.args['id'])
        if record != None:
            span1 = "View a CCA(Success)"
            span2 = "Here are the CCA details:"
            form_header = {
                'id' : 'ID',
                'name': 'Name',
                'type': 'Type'
            }

            
            return render_template("view.html",
                               page_type = 'success_cca',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               error=error,
                               form_header = form_header,
                               form_meta={
                                   'action': ' ',
                                   'method': 'get'
                               },
                               form_data =  record,
                               students = students
                              )
        else:
            error = f'CCA ID {request.args["id"]} not found! Try again!'
    
    return render_template("view.html",
                           page_type = "view_cca",
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           error = error,
                           form_header = form_header,
                           form_meta = {
                                'action': '/view/cca?confirm',
                                'method': 'get'
                            },
                           form_data = {
                                "id": " "
                            }
                          )


@app.route('/view/activity', methods = ['GET', 'POST']) #there is a problem here what is the primary key of the activity?
def view_activity():
    title = 'View an Activity'
    span1 = "View an Activity"
    span2 = "Use the following form to view an Activity"
    form_header = {"id": "Activity ID"}
    error = ' '

    students = [
        {
              "id": '1',
              "name" : "john",
              "student_age" : 18,
              "year_enrolled" : 2022,
              "graduating_year" : 2023,
              "class_id" : "2227"
        }, 
        {
              "id": '2',
              "name" : "nolan",
              "student_age" : 19,
              "year_enrolled" : 2022,
              "graduating_year" : 2023,
              "class_id" : "2228"
        }
    ]
        

    if request.args:
        record = {
              "name": "cce project",
              "start_date": "20230404",
              "end_date": "20230405",
              "duration": 5
        }

        if record != None: 
            span1 = "View an Activity(Submission)"
            span2 = "Here are the details:"
            form_header = {
                'name': 'Activity Name',
                'start_date': 'Start Date',
                'end_date': 'End Date',
                'duration': 'Duration'
            }
            
            return render_template("view.html",
                               page_type = 'success_activity',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_meta={
                                   'action': '',
                                   'method': 'get'
                               },
                               form_data =  record,
                               students = students
                            
                              )
        else:
            error = f'Activity {request.args["id"]} not found! Try again!'
    
    return render_template("view.html",
                           page_type = "view_activity",
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           error = error,
                           form_header = form_header,
                           form_meta = {
                                'action': ' ',
                                'method': 'get'
                            },
                           form_data = {
                                "id": " "
                            }
                          )
@app.route('/view_all/student')
def view_all_student():
    title = 'View all Students'
    span1 = 'Here are the details of all students'
    form_header = {'id': 'Student ID',
                  'name': 'Student Name',
                  'class': 'Student Class',
                  'acitivity': 'Activity'
                    }
    record = [
        {
        'id': '1',
        'name': 'John',
        'class': '2227',
        'activity': ['beach clean up', 'elderly home']      
        },
        {'id': '2',
         'name': 'Nolan',
         'class': '2228',
         'activity': ['old folks home', 'painting']
        }]

    
    return render_template("view_all.html",
                           page_type = "view_all_student",
                           title = title,
                           span1 = span1,
                           form_header = form_header,
                           form_data = record
                          )
      
@app.route('/view_all/activity')
def view_all_activity():
    title = 'View all Activities'
    span1 = 'Here are the details of all Activities'
    form_header = {'id': 'Activity ID',
                  'name': 'Acitity Name',
                  'start_date': 'Start Date',
                  'end_date': 'End Date',
                  'duration': 'Duration'
                    }

    record = [
        {'id': '1',
          'name': 'beach clean up',
          'start_date': '20190212',
          'end_date': '20190212',
          'duration': '50'
        },
        {'id': '2',
          'name': 'painting',
          'start_date': '20230415',
          'end_date': '20230519',
          'duration': '50'
        }
    ]

    return render_template("view_all.html",
                           page_type = 'view_all_activities',
                           title = title,
                           span1 = span1,
                           form_header = form_header,
                           form_data = record
                          )

@app.route('/edit/cca', methods = ['POST', 'GET'])
def edit_cca():
    title = "Update CCA Membership"
    span1 = "Update a CCA Membership"
    span2 = "Use the following form to update a CCA membership:"
    form_header  = {"student_id": "Student ID"}
    error = " "
    updateSuccess = True
    insertSuccess = True
    cca_data = [
        {
        "id": "1",
        "name": "Tchoukball"
    },
        {
        "id": "2",
        "name": "toiletcleaner"
        }
    ]
    form_header = {
                'id': ' Student ID',
                'name': 'Name'  
            }
    if 'addattempted' in request.args:
        new_record = {"student_id":request.form["student_id"],
                      "cca_id":request.form["cca_id"]}
        insertSuccess = studentCCACollection.insert(new_record)
        if insertSuccess is False:
            error = "Error: The new record already exists in the database!"
        else:
            ccaRecord = ccaCollection.find(request.form['cca_id'])
            
            span1 = "Add a CCA Membership (Success)"
            span2 = "The CCA Membership has been successfully added!"
            form_header = {
                'id':'CCA ID',
                'name': 'Name'
            }
            return render_template("edit.html",
                           page_type = 'success',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_meta={
                               'action': '/edit/cca?success',
                               'method': 'post'
                           },
                           form_data = {
                               'id': ccaRecord['id'],
                               'name': ccaRecord['name']
                           }
                           )
    if 'add' in request.args:
            studentRecord = studentCollection.find(request.form["student_id"])
            span1 = "Add a CCA to this Student"
            span2 = "Use the following form to add a CCA to this student:"
            ccalist = [{'name':"Tchoukball",
                 'id':'1'
               }, 
               {'name':"toiletcleaner",
                'id':'2'
               }]
            return render_template("edit.html",
                       page_type = 'add_cca',
                       title = title,
                       span1 = span1,
                       span2 = span2,
                       form_header = form_header,
                       form_meta={
                           'action': '/edit/cca?addattempted',
                           'method': 'post'
                       },
                       form_data =  {
                           'studentRecord': studentRecord,
                       },
                       ccalist = ccalist
                      )
    if 'updateattempted' in request.args:
        # old_record = {"student_id":request.form["student_id"], 
        #               "cca_id":request.form["old_cca_id"]}
        # new_record = {"student_id":request.form["student_id"], 
        #               "cca_id":request.form["new_cca_id"]}
        # updateSuccess = studentCCACollection.update(old_record, new_record)
        updateSuccess = True
        if updateSuccess is False:
            error = "Error: The new record already exists in the database!"
        else:
            ccaRecord = ccaCollection.find(request.form['new_cca_id'])
            
            span1 = "Update a CCA Membership (Success)"
            span2 = "The CCA Membership has been successfully updated!"
            form_header = {
                'id':'New CCA ID',
                'name': 'New Name'
            }
            
            return render_template("edit.html",
                           page_type = 'success',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_meta={
                               'action': '/edit/cca?success',
                               'method': 'post'
                           },
                           form_data = {
                               'id': ccaRecord['id'],
                               'name': ccaRecord['name']
                           }
                           )
    if 'confirm' in request.args: 
            studentRecord = studentCollection.find(request.form['student_id'])
            ccaRecord = ccaCollection.find(request.form['cca_id'])
        
            ccalist = [{'name':"Tchoukball",
                 'id':'1'
               }, 
               {'name':"toiletcleaner",
                'id':'2'
               }]
        
            return render_template("edit.html",
                       page_type = 'confirm_cca',
                       title = title,
                       span1 = span1,
                       span2 = span2,
                       form_header = form_header,
                       form_meta={
                           'action': '/edit/cca?updateattempted',
                           'method': 'post'
                       },
                       form_data =  {
                           'studentRecord': studentRecord,
                           'ccaRecord': ccaRecord
                       },
                       ccalist = ccalist
                      )
    
    if 'check' in request.args or updateSuccess is False or insertSuccess is False:
        record = studentCollection.find(request.form['student_id'].strip(" "))

        if record is not None:
            span1 = "Edit this Student's CCA"
            span2 = "Please edit the Student's CCA details below:"
            return render_template("edit.html",
                       page_type = 'check_cca',
                       title = title,
                       span1 = span1,
                       span2 = span2,
                       form_header = form_header,
                       error = error,
                       form_meta={
                           'action': '/edit/cca?confirm',
                           'action2': '/edit/cca?add',
                           'method': 'post'
                       },
                       form_data =  record,
                       cca_data = cca_data
                      )
        else:
            error = f'Student ID {request.form["id"]} not found! Try again!' 
        
    return render_template("edit.html",
                           page_type = 'edit_cca',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           error = error,
                           form_header = form_header,
                           form_meta = {
                               'action': '/edit/cca?check',
                               'method': 'post'
                           },
                           form_data = {
                               'student_id':  ' '
                           }
                          )

@app.route('/edit/activity')
def edit_activity():
    return render_template("edit.html")

if __name__ == '__main__':
    app.run('0.0.0.0')


#click on name go to another page
#or have multiple links, student activity link, student cca link,
#will have a query to pass on to the respective pages