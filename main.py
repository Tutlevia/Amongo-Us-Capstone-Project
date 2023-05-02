from flask import Flask, render_template, request
import storage 
import front 

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
                           form_data =  {
                               'id': request.form['id'],
                               'name': request.form['name'],
                               'type': request.form['type']
                           }  
                          )
    if 'attempted' in request.args:
        # record = {
        #     'id': request.form['id'],
        #     'name': request.form["name"],
        #     'type': request.form['type']
        # }
        # insertSuccess = CCA.insert(record)
        insertSuccess = True
        if insertSuccess is True: 
            span1 = 'Register a new CCA(Success)'
            span2 = 'The following CCA has been registered!'
            return render_template("add.html",
                               page_type = 'success_cca',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_data =  {
                                   'id': request.form['id'],
                                   'name': request.form['name'],
                                   'type': request.form['type']
                               }      
                              )
        else:
            error = "Error: The CCA record already exists in the database!"
        
    
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
                  "start_date": "Start Date (YYYYMMDD)",
                  "end_date": "End Date (YYYYMMDD)",
                  "category": "Category",
                  "role": "Role",
                  "award": "Award",
                  "hours": "Hours",
                  "cca" : "CCA"
    }
    # ccaRecords = CCA.findall()
    # ccalist = []
    # for record in ccaRecords:
    #     ccalist.append(record['name'])
    ccalist = ["Basketball", "Tchoukball"]
    error = " "
        
    if 'confirm' in request.args:
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
                           form_data =  {
                               'id': request.form['id'],
                               'start_date': request.form['start_date'],
                               'end_date': request.form['end_date'],
                               'category': request.form['category'],
                               'role': request.form['role'],
                               'award': request.form['award'],
                               'hours': request.form['hours'],
                               'cca' : request.form['cca']
                           }  
                          )
    if 'attempted' in request.args:
        # record = {
        #     'id': request.form['id'],
        #     'start_date': request.form['start_date'],
        #     'end_date': request.form['end_date'],
        #     'duration': request.form['duration'],
        #     'category': request.form['category'],
        #     'role': request.form['role'],
        #     'award': request.form['award'],
        #     'hours': request.form['hours'],   
        #     'cca' : request.form['cca']
        # }
        # insertSuccess = Activity.insert(record)
        insertSuccess = True
        if insertSuccess is True:
            span1 = "Register a new Activity(Success)"
            span2 = "The following Activity has been registered!"
            return render_template("add.html",
                               page_type = 'success_activity',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_data =  {
                                   'id': request.form['id'],
                                   'start_date': request.form['start_date'],
                                   'end_date': request.form['end_date'],
                                   'category': request.form['category'],
                                   'role': request.form['role'],
                                   'award': request.form['award'],
                                   'hours': request.form['hours'],
                                   'cca' : request.form['cca']
                               }  
                              )
        else: 
            error = "Error: The activity record already exists in the database!"
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
                               "start_date": " ",
                               "end_date": " ",
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
        # record = SC.find(request.args['id'])
        record = {
              "id": '1',
              "name" : "john",
              "student_age" : 18,
              "year_enrolled" : 2022,
              "graduating_year" : 2023,
              "class_id" : "2227"
        }
        activities = [{
              "id": 1,
              "name": "cce project",
              "start_date": "20230404",
              "end_date": "20230405",
              "duration": 5
        },
        {     
              "id": 2,
              "name": "beach clean up",
              "start_date": "20230804",
              "end_date": "20230419",
              "duration": 10
        }]

        if record != None:
        
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

            return render_template("view.html",
                               page_type = 'success_student',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               form_header = form_header,
                               form_meta={
                                   'action': '/view/student?success',
                                   'method': 'get'
                               },
                               form_data =  record,
                               activities = activities
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
        record = SC.find(request.args['id'])
        if record != None:
            
            span1 = "View a Class(Success)"
            span2 = "Here are the Class details:"
            return render_template("view.html",
                               page_type = 'success_class',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               error = error,
                               form_header = form_header,
                               form_meta={
                                   'action': '/view/class?success',
                                   'method': 'get'
                               },
                               form_data =  record      
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
                                'action': '',
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
        record = SC.find(request.args['id'])
        if record != None:
            span1 = "View a CCA(Success)"
            span2 = "Here are the CCA details:"
            return render_template("view.html",
                               page_type = 'success_cca',
                               title = title,
                               span1 = span1,
                               span2 = span2,
                               error=error,
                               form_header = form_header,
                               form_meta={
                                   'action': '/view/cca?success',
                                   'method': 'get'
                               },
                               form_data =  record
                               
                              )
    
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




@app.route('/edit/membership')
def edit_membership():
    return render_template("edit.html")

@app.route('/edit/participation')
def edit_participation():
    return render_template("edit.html")

if __name__ == '__main__':
    app.run('0.0.0.0')


#click on name go to another page
#or have multiple links, student activity link, student cca link,
#will have a query to pass on to the respective pages