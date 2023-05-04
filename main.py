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
    ccalist = ccaCollection.findall(["id","name"])
    error = " "
        
    if 'confirm' in request.args:
        cca_name = ccaCollection.find(request.form['cca'], ["name"])["name"]
        form_header["cca"] = "CCA ID"
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
                           form_data = dict(request.form),
                           cca_name = cca_name
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
            cca_name = ccaCollection.find(request.form['cca'], ["name"])["name"]
            form_header["cca"] = "CCA ID"
            span1 = "Register a new Activity(Success)"
            span2 = "The following Activity has been registered!"
            return render_template("add.html",
                               page_type = 'success_activity',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_data =  dict(request.form),
                               cca_name = cca_name
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
            studentClass = studentCollection.viewclass(id)
            studentCCAs = studentCollection.viewcca(id)
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
                'activity_id' : 'Activity ID',
                'activity_name': 'Name',
                'start_date': 'Start Date',
                'end_date': 'End Date',
                'hours': 'Hours'
            }
            table_header2 ={
                'CCA_id': 'CCA ID',
                'CCA_name': 'Name'
            }
            return render_template("view.html",
                               page_type = 'success_student',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               table_header = table_header,
                               table_header2 = table_header2,
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
        id = request.args["id"].strip(" ")
        record = classCollection.find(id)
        if record != None:
            students = classCollection.viewstudent(id)
            span1 = "View a Class(Success)"
            span2 = "Here are the Class details:"
            form_header = {
                           'id' : 'Class ID',
                           'name': 'Name',
                           'level': 'Level'
                               }
            table_header = {
                           'student_id' : 'Student ID',
                           'student_name': 'Student Name',
                           'class': 'Class'
            }
            return render_template("view.html",
                               page_type = 'success_class',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               table_header = table_header,
                               form_data = {
                                   'record':record,
                                   'students':students
                               }
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
    if request.args:
        id = request.args["id"].strip(" ")
        record = ccaCollection.find(id)
        if record != None:
            students = ccaCollection.viewstudent(id)
            activities = ccaCollection.viewactivity(id)
            span1 = "View a CCA(Success)"
            span2 = "Here are the CCA details:"
            form_header = {
                'id' : 'ID',
                'name': 'Name',
                'type': 'Type'
            }
            table_header = {
                           'student_id' : 'Student ID',
                           'student_name': 'Student Name',
                           'class': 'Class'
            }
            table_header2 ={
                'activity_id': 'Activity ID',
                'activity_name': 'Activity Name',
                'start_date': 'Start Date',
                'end_date': 'End Date',
                'hours': 'Hours'
            }
            return render_template("view.html",
                               page_type = 'success_cca',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               table_header = table_header,
                               table_header2 = table_header2,
                               form_data = {
                                   'record':record,
                                   'students':students,
                                   'activities':activities
                               }
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


@app.route('/view/activity', methods = ['GET', 'POST']) 
def view_activity():
    title = 'View an Activity'
    span1 = "View an Activity"
    span2 = "Use the following form to view an Activity"
    form_header = {"id": "Activity ID"}
    error = ' '


    if request.args:
        id = request.args["id"].strip(" ")
        record = activityCollection.find(id)

        if record != None: 
            cca = ccaCollection.find(record["cca_id"],["id","name"])
            students = activityCollection.viewstudent(id)
            span1 = "View an Activity(Submission)"
            span2 = "Here are the details:"
            form_header = {
                'id': 'Activity ID',
                'name': 'Activity Name',
                'start_date': 'Start Date',
                'end_date': 'End Date',
                'description': 'Description',
                "category": 'Category',
                "role": 'Role',
                "award": 'Award',
                "hours": 'Hours',
                "cca_id": 'CCA ID'
            }
            table_header = {
                           'student_id' : 'Student ID',
                           'student_name': 'Student Name',
                           'class': 'Class'
            }
            
            return render_template("view.html",
                               page_type = 'success_activity',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               table_header = table_header,
                               form_data = {
                                   'record':record,
                                   'students':students,
                                   'cca':cca
                               }
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
    table_header = ['Student ID',
                    'Student Name',
                    'Student Age',
                    'Year Enrolled',
                    'Graduating Year',
                    'Class ID',
                    'Class Name',
                   ]

    records = studentCollection.viewall()

    return render_template("view_all.html",
                           page_type = "view_all_students",
                           title = title,
                           span1 = span1,
                           table_header = table_header,
                           table_data = records
                          )
@app.route('/view_all/class')
def view_all_class():
    title = 'View all Class'
    span1 = 'Here are the details of all Classes'
    table_header = ['Class ID',
                    'Class Name',
                    'Class Level',
                   ]

    records = classCollection.findall()

    return render_template("view_all.html",
                           page_type = "view_all_class",
                           title = title,
                           span1 = span1,
                           table_header = table_header,
                           table_data = records
                          )
@app.route('/view_all/cca')
def view_all_cca():
    title = 'View all CCA'
    span1 = 'Here are the details of all CCAs'
    table_header = ['CCA ID',
                    'CCA Name',
                    'CCA Type',
                   ]

    records = ccaCollection.findall()

    return render_template("view_all.html",
                           page_type = "view_all_cca",
                           title = title,
                           span1 = span1,
                           table_header = table_header,
                           table_data = records
                          )
      
@app.route('/view_all/activity')
def view_all_activity():
    title = 'View all Activities'
    span1 = 'Here are the details of all Activities'
    table_header = ['Activity ID',
                    'Activity Name',
                    'Start Date',
                    'End Date',
                    'Hours'
                   ]
    columns = ['id', 'name', 'start_date', 'end_date', 'hours']
    records = activityCollection.findall(columns)

    return render_template("view_all.html",
                           page_type = 'view_all_activities',
                           title = title,
                           span1 = span1,
                           table_header = table_header,
                           table_data = records
                          )

@app.route('/edit/cca', methods = ['POST', 'GET'])
def edit_cca():
    title = "Update CCA Membership"
    span1 = "Update a CCA Membership"
    span2 = "Use the following form to update a CCA membership:"
    form_header  = {"student_id": "Student ID",
                   'id': ' Student ID',
                   'name': 'Name',
                   'CCA_id': 'CCA ID',
                   'CCA_name': 'CCA Name'}
    ccalist = ccaCollection.findall(["id","name"])
    error = " "
    updateSuccess = True
    insertSuccess = True
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
            form_header = {'id':'CCA ID',
                           'name': 'CCA Name'
            }
            return render_template("edit.html",
                           page_type = 'success',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_data = {
                               'id': ccaRecord['id'],
                               'name': ccaRecord['name']
                           },
                           student_id = request.form['student_id']
                           )
    if 'add' in request.args:
            studentRecord = studentCollection.find(request.form["student_id"],["id","name"])
            span1 = "Add a CCA to this Student"
            span2 = "Use the following form to add a CCA to this student:"

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
        old_record = {"student_id":request.form["student_id"], 
                      "cca_id":request.form["old_cca_id"]}
        new_record = {"student_id":request.form["student_id"], 
                      "cca_id":request.form["new_cca_id"]}
        updateSuccess = studentCCACollection.update(old_record, new_record)

        if updateSuccess is False:
            error = "Error: The new record already exists in the database!"
        else:
            ccaRecord = ccaCollection.find(request.form['new_cca_id'])
            
            span1 = "Update a CCA Membership (Success)"
            span2 = "The CCA Membership has been successfully updated!"
            form_header = {
                'id':'New CCA ID',
                'name': 'New CCA Name'
            }
            
            return render_template("edit.html",
                           page_type = 'success',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_data = {
                               'id': ccaRecord['id'],
                               'name': ccaRecord['name']
                           },
                           student_id = request.form['student_id']
                           )
    if 'confirm' in request.args: 
            studentRecord = studentCollection.find(request.form['student_id'], ['id', 'name'])
            ccaRecord = ccaCollection.find(request.form['cca_id'])
        
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
        id = request.form['student_id'].strip(" ")
        record = studentCollection.find(id, ['id','name'])

        if record is not None:
            cca_data = studentCollection.viewcca(id)
            
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

@app.route('/edit/activity', methods = ['POST', 'GET'])
def edit_activity():
    title = "Update an Activity "
    span1 = "Update an Activity participation"
    span2 = "Use the following form to update a Activity participation:"
    form_header  = {"student_id": "Student ID",
                   'id': ' Student ID',
                   'name': 'Name',
                   'activity_id': "Activity ID",
                   'activity_name': "Activity Name",
                   'start_date': "Start Date",
                   'end_date': "End Date",
                   'hours': "Hours"}
    error = " "
    updateSuccess = True
    insertSuccess = True
    activitylist = activityCollection.findall(['id','name'])
    
    if 'addattempted' in request.args:
        new_record = {"student_id":request.form["student_id"],
                      "activity_id":request.form["activity_id"]}
        insertSuccess = studentActivityCollection.insert(new_record)
        if insertSuccess is False:
            error = "Error: The new record already exists in the database!"
        else:
            activityRecord = activityCollection.find(request.form['activity_id'])
            span1 = "Add an Activity Participation (Success)"
            span2 = "The Activity Participation has been successfully added!"
            form_header = {
                'id':'Activity ID',
                'name': 'Name'
            }
            return render_template("edit.html",
                           page_type = 'success',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_data = {
                               'id': activityRecord['id'],
                               'name': activityRecord['name']
                           },
                           student_id = request.form['student_id']
                           )
    if 'add' in request.args:
            studentRecord = studentCollection.find(request.form["student_id"],['id','name'])
            span1 = "Add an Activity to this Student"
            span2 = "Use the following form to add an Activity to this student:"
            return render_template("edit.html",
                       page_type = 'add_activity',
                       title = title,
                       span1 = span1,
                       span2 = span2,
                       form_header = form_header,
                       form_meta={
                           'action': '/edit/activity?addattempted',
                           'method': 'post'
                       },
                       form_data =  {
                           'studentRecord': studentRecord,
                       },
                       activitylist = activitylist
                      )
    
    if 'updateattempted' in request.args:
        old_record = {"student_id":request.form["student_id"], 
                      "cca_id":request.form["old_activity_id"]}
        new_record = {"student_id":request.form["student_id"], 
                      "cca_id":request.form["new_activity_id"]}
        updateSuccess = studentActivityCollection.update(old_record, new_record)
        if updateSuccess is False:
            error = "Error: The new record already exists in the database!"
        else:
            activityRecord = activityCollection.find(request.form['new_activity_id'])
            
            span1 = "Update an Activity Participation (Success)"
            span2 = "The Activity Participation has been successfully updated!"
            form_header = {
                'id':'New Activity ID',
                'name': 'New Activity Name'
            }
            
            return render_template("edit.html",
                           page_type = 'success',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           form_header = form_header,
                           form_data = {
                               'id': activityRecord['id'],
                               'name': activityRecord['name']
                           },
                           student_id = request.form['student_id']
                           )
            
    if 'confirm' in request.args: 
            studentRecord = studentCollection.find(request.form['student_id'],['id','name'])
            activityRecord = activityCollection.find(request.form['activity_id'])
        
            return render_template("edit.html",
                       page_type = 'confirm_activity',
                       title = title,
                       span1 = span1,
                       span2 = span2,
                       form_header = form_header,
                       form_meta={
                           'action': '/edit/activity?updateattempted',
                           'method': 'post'
                       },
                       form_data =  {
                           'studentRecord': studentRecord,
                           'activityRecord': activityRecord
                       },
                       activitylist = activitylist
                      )

    if 'check' in request.args or updateSuccess is False or insertSuccess is False:
        id = request.form['student_id'].strip(" ")
        record = studentCollection.find(id,['id','name'])

        if record is not None:
            activity_data = studentCollection.viewactivity(id)
            span1 = "Edit this Student's Activity participation"
            span2 = "Please edit the Student's Activity participation details below:"
            return render_template("edit.html",
                       page_type = 'check_activity',
                       title = title,
                       span1 = span1,
                       span2 = span2,
                       form_header = form_header,
                       error = error,
                       form_meta={
                           'action': '/edit/activity?confirm',
                           'action2': '/edit/activity?add',
                           'method': 'post'
                       },
                       form_data =  record,
                       activity_data = activity_data
                      )
        else:
            error = f'Student ID {request.form["id"]} not found! Try again!' 
    
    return render_template("edit.html",
                           page_type = 'edit_activity',
                           title = title,
                           span1 = span1,
                           span2 = span2,
                           error = error,
                           form_header = form_header,
                           form_meta = {
                               'action': '/edit/activity?check',
                               'method': 'post'
                           },
                           form_data = {
                               'student_id':  ' '
                           }
                          )
    
if __name__ == '__main__':
    app.run('0.0.0.0')