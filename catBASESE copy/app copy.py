import os
from flask import Flask
import hashlib
from flask import request
from flask import render_template
from werkzeug import secure_filename
from flask import session
from flask import redirect, url_for, send_from_directory 
import mysql.connector



UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['png,jpg,gif'])



app = Flask(__name__)
app.secret_key = '1234'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/updateForm/<id>')
def updateForm(id):


	cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
	cur = cnx.cursor()
	idx = (id,)
	cur.execute("select * from users where id=%s",idx)
	data = cur.fetchone()
	return render_template("update.html",theData = data)


@app.route('/show/<id>')
def show(id):
	if session['loggedin']==1:

		cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
		cur = cnx.cursor()
		idx = (id,)
		cur.execute("select * from users where id=%s",idx)
		data = cur.fetchone()
		return render_template("show.html",theData = data)
	else:
		return render_template('loginForm.html')

# @app.route('/show/<id>')
# def show(id):
#	if request.method=='GET':
#		sessions['loggedin']=;
#		cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
#		cur = cnx.cursor()
#		idx = (id,)
#		cur.execute("select * from users where id=%s",idx)
#		data = cur.fetchone()
#		return render_template("show.html",theData = data)
#	else:
#		return render_template('loginForm.html')

@app.route('/updateAction/<id>',methods=['GET','POST'])
def updateAction(id):

	username = request.form["username"]
	password = request.form["password"]
	info = request.form['info']


	md5 = hashlib.md5()
	md5.update(password)
	password = md5.hexdigest()


	cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
	cur = cnx.cursor()
	cur.execute("update users set username=%s, password=%s, info=%s where id=%s",(username,password,info,id))
	cnx.commit()
	return redirect('/protected')




@app.route('/delete/<id>')
def delete(id):

	cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
	cur = cnx.cursor()
	uId = (id,)
	statement = "delete from users where id =%s"
	cur.execute(statement,uId)
	cnx.commit()
	return redirect("/protected")



@app.route('/')
def start():
	return render_template('index.html')

@app.route('/loginForm')
def loginForm():
	return render_template('loginForm.html')

@app.route('/addForm')
def addForm():
	return render_template('addForm.html')

@app.route('/protected')
def protected():
	
	if session['loggedin']==1:
		cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
		cur = cnx.cursor()
		cur.execute("select * from users")
		users = cur.fetchall()
		return render_template('protected.html',data=users)
	else:
		return render_template('loginForm.html')

@app.route('/logout')
def logout():
	session.pop('loggedin',None)
	return render_template('loginForm.html')


@app.route('/loginAction',methods=['GET','POST'])
def loginAction():
	if request.method=='POST':
		username = request.form["username"]
		password = request.form["password"]
		
		md5 = hashlib.md5()
		md5.update(password)
		password = md5.hexdigest()

		cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
		cur = cnx.cursor()
		cur.execute("select * from users where username=%s and password=%s",(username,password))
		user = cur.fetchone()


		if user:
			data = {'username':username,'password':password }
			session['loggedin']=1 
			return redirect("/protected")
		else:
			session['loggedin']=0
			return redirect("/loginForm")

		cnx.close()

	else:
		return request.method


# @app.route('/<id>/<num>')
# def index(id,num):
#	return 'Hello '+id

# @app.route('/uploads/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		return'POST'
	else:
		return request.method

@app.route('/addAction',methods=['GET','POST'])
def addaction():
	if request.method == 'POST':

		cnx = mysql.connector.connect(user='root',password='root',host='127.0.0.1',port='8889',database='day3')
		cur = cnx.cursor()
		password = request.form["password"]
		info = request.form['info']
		md5 = hashlib.md5()
		md5.update(password)
		password = md5.hexdigest()
		cur.execute("insert into users (username, password,info) values (%s,%s,%s)",(request.form['username'],password,info))
		cnx.commit()

		return redirect('/protected')
		


		# hashed = hashlib.md5()
		# hashed.update(request.form['password'])
		# file = request.files['userfile']
		# filename = secure_filename(file.filename)
		# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		# return 'Name: ' + request.form['username'] + '<br>'+'Password:' + "<p style='color:red'>" + hashed.hexdigest() +"</p>"+'<br>' + '<img src="'+url_for('send_file', filename=filename)+'"/>'



	else:
		return request.method




@app.route('/form')
def form():
	name='joe'
	return render_template('form.html',name = name)

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string




if __name__ == '__main__':
	app.run(debug=True)