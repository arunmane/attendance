# coding: utf-8
#!/usr/bin/python; 
from flask import Flask, redirect, url_for, request, render_template,session,flask_excel as excel
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'arun'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app) 


app = Flask(__name__)
app.secret_key = 'hello'

@app.route('/success/<name>')
def success(name):
   ses = check_session()
   if ses != '1':
        return redirect(url_for('index')) 	
   #return 'welcome %s' % name
   return render_template('dashboard.html',name = name)
  
@app.route('/check_session')
def check_session():
	 if 'username' in session:
      		username = session['username']
		role = session['role']	
         	return '1'

@app.route('/log_out')
def log_out():
	session.pop('username', None)
   	return redirect(url_for('index'))

@app.route('/index')
def index():
	#return redirect(url_for('show_teachers'))
		 
	return render_template('login.html') 

@app.route('/add_teachers_view')
def add_teachers_view():
	#return redirect(url_for('show_teachers'))
	data = get_class()		 
	return render_template('add_teachers.html',name=data) 

@app.route('/get_class')
def get_class():
        data = 'this data we are passing'
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from class")
	data  = cursor.fetchall()
	return data
	
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
	user  = request.form['nm']
      	passw = request.form['pass']
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from User where Username='" + user + "' and Password='" + passw + "'")
	data = cursor.fetchone()	

	if data is None:
	     return "Username or Password is wrong"
	else:
	      session['username'] = user
	      session['role'] = data[1] 	
	      return redirect(url_for('success',name = data))
   else:
      user = request.args.get('nm')
      user = request.args.get('pass')
      return redirect(url_for('success',name = user))


@app.route('/add_teachers',methods = ['POST', 'GET'])
def add_teachers():

	ses = check_session()
        if ses != '1':
             return redirect(url_for('index'))
           
	if request.method == 'POST':
		name   = request.form['name']
                passw  = request.form['pwd']
		tclass = request.form['class']
		conn   = mysql.connect()
		#cursor = mysql.connect().cursor()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO User (userName, password, name, role, status,class_id) VALUES ('"+ name +"','"+ passw +"','"+ name +"',2,1,'"+tclass+"' )")		
		conn.commit()
		return redirect(url_for('show_teachers'))			
		#return "INSERT INTO User (userName, password, name, role, status) VALUES ('"+ name +"','"+ passw +"','"+ name +"',2,1 )"

		
		#return 'function called %s' % name
	else:
      		name = request.args.get('name')
      		passw = request.args.get('pwd')
                return 'function called %s' % passw 
		


@app.route('/show_teachers')
def show_teachers():

	ses = check_session()
        if ses != '1':
             return redirect(url_for('index'))

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from User where role = 2 and status =1")
	data  = cursor.fetchall()
	classd = get_class()
	
	if data is None:
	     return "Username or Password is wrong"
	else:
	      return render_template('show_teachers.html',data =data,classd=classd) 


@app.route('/delete_teachers/<ids>')
def delete_teachers(ids):
	emp_id = ids

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("update User set status =0 where userId='"+emp_id+"'")
	conn.commit()
	data  = cursor.fetchone() 

	return redirect(url_for('show_teachers'))


@app.route('/edit_teachers/<ids>')
def edit_teachers(ids):

	ses = check_session()
        if ses != '1':
             return redirect(url_for('index'))
	
	emp_id = ids
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from User where userId='"+emp_id+"'")
	conn.commit()
	data  = cursor.fetchone()

	return render_template('edit_teachers.html',data =data)


@app.route('/update_teachers',methods = ['POST', 'GET'])
def update_teachers():
	name = request.form['name']
        passw = request.form['pwd']
	emp_id = request.form['id']
	conn = mysql.connect()
	#cursor = mysql.connect().cursor()
	cursor = conn.cursor()
	cursor.execute("Update User  set userName='"+name+"', password='"+passw+"', name='"+name+"' where userId='"+emp_id+"'  ")	
	conn.commit()
	
	return redirect(url_for('show_teachers'))

@app.route('/add_student')
def add_student():
	  ses = check_session()
          if ses != '1':
             return redirect(url_for('index'))
 	
	  #conn = mysql.connect()
	  #cursor = conn.cursor()
	  #cursor.execute("SELECT userId,name from User where role = 2 and status =1")
	  #data  = cursor.fetchall()
	  data = get_class()
	  return render_template('add_student.html',data=data) 


@app.route('/save_student',methods = ['POST', 'GET'])
def save_student():
	if request.method == 'POST':
		name = request.form['name']
                passw = request.form['pwd']
		sclass = request.form['class']
		#return 'function called %s' % teachers
		conn = mysql.connect()
		#cursor = mysql.connect().cursor()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO User (userName, password, name, role, status,class_id) VALUES ('"+ name +"','"+ passw +"','"+ name +"',3,1,'"+sclass+"' )")
		conn.commit()
		return '1'
	else:
      		name = request.args.get('name')
      		passw = request.args.get('pwd')
                return 'function called %s' % passw 

 

@app.route('/show_student')
def show_student():
	 ses = check_session()
         if ses != '1':
             return redirect(url_for('index'))
	 
	 conn = mysql.connect()
	 cursor = conn.cursor()
	 cursor.execute("SELECT * from User where role = 3 and status =1")
	 data1  = cursor.fetchall()
	 data = get_class()
	 #data1="unother data passing"
	 return render_template('show_student.html',data=data,data1=data1) 

@app.route('/edit_student/<ids>')
def edit_student(ids):

	ses = check_session()
        if ses != '1':
             return redirect(url_for('index'))
	
	emp_id = ids
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from User where userId='"+emp_id+"'")
	conn.commit()
	data  = cursor.fetchone()

	return render_template('edit_student.html',data =data)
	

@app.route('/update_student',methods = ['POST', 'GET'])
def update_student():
	name   = request.form['name']
        passw  = request.form['pwd']
	sclass = request.form['class'] 
	emp_id = request.form['id']
	conn = mysql.connect()
	#cursor = mysql.connect().cursor()
	cursor = conn.cursor()
	cursor.execute("Update User  set userName='"+name+"', password='"+passw+"', name='"+name+"', class_id ='"+sclass+"'     where userId='"+emp_id+"'  ")	
	conn.commit()
	
	return redirect(url_for('show_student'))


@app.route('/get_class_details/<ids>')
def get_class_details(ids):
	class_id = ids	
	
	ses = check_session()
        if ses != '1':
             return redirect(url_for('index'))
	
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from User where role = 3 and status =1 and  class_id='"+class_id+"'")
	stdudent  = cursor.fetchall()
	cursor.execute("SELECT * from User where role = 2 and status =1 and  class_id='"+class_id+"'")
	teachers  = cursor.fetchall()
	cursor.execute("SELECT * from class where id ='"+class_id+"'")
	classd  = cursor.fetchone()
	return render_template('class_details.html',stdudent=stdudent,teachers=teachers,classd=classd)
	
@app.route('/add_class_teacher')
def add_class_teacher():
	ses = check_session()
        if ses != '1':
             return redirect(url_for('index'))
	data = get_class()
	teacher = get_all_teacher() 
	return render_template('add_school_teacher.html',data=data,teacher=teacher)
	#return 'function called'	

@app.route('/get_all_teacher')
def get_all_teacher():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from User where role = 2 and status =1 ")
	teachers  = cursor.fetchall()
	return teachers

@app.route('/save_class_teacher',methods = ['POST', 'GET'])
def save_class_teacher():
	class1   = request.form['class']
        teacher  = request.form['teacher']
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("update class set teacher_id='"+teacher+"' where id='"+class1+"'")	
	conn.commit()
	return "1"
	
@app.route('/view_class_teacher')
def show_class_teacher():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("select c.classname , u.name from class c JOIN User u ON c.teacher_id=u.userId  ")
        teachers  = cursor.fetchall()
	return render_template('show_class_teachers.html',data=teachers)  
 

@app.route('/get_student_details/<ids>')
def get_student_details(ids):
	class_id = ids	
	#return '**** %s' % class_id	
	ses = check_session()
        if ses != '1':
        	return redirect(url_for('index'))
	
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from User where role = 3 and status =1 and  class_id='"+class_id+"'")
	stdudent  = cursor.fetchall()
	cursor.execute("SELECT * from class where id ='"+class_id+"'")
	classd  = cursor.fetchone()
	return render_template('student_details.html',stdudent=stdudent,classd=classd)

@app.route('/make_attendance')
def make_attendance():
	classd = get_class()
	return render_template('make_attendace.html',data=classd) 

@app.route('/mark_attendance/<classno>/<role>')
def mark_attendance(classno,role):
	#return 'classno %s' % classno 
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("INSERT INTO attendance(class, role) VALUES ('"+ classno +"','"+ role+"')")#
	conn.commit()
	return "attedance mark";

@app.route('/view_attendance')
def view_attendance():
	classd = get_class()
	return render_template('view_attendace.html',data=classd) 	

@app.route('/get_class_attendance_details/<ids>')
def get_class_attendance_details(ids):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("select u.name,a.class,date(a.reg_date) from attendance a join User u on a.role=u.userId where a.class='"+ids+"'")
	stdudent  = cursor.fetchall()
	return render_template('viewclass_attendance.html',data=stdudent)	

@app.route('/downlaod_excel/<ids>')
def downlaod_excel(ids):
	return 'class %s' %ids
	
if __name__ == '__main__':
   app.run(debug = True)
