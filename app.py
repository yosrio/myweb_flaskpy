from flask import Flask, render_template, json, request, flash 
from flask import redirect, session, abort
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showLogin')
def showLogin():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
	if request.form['inputPassword'] == 'yosrio10' and request.form['inputName'] == 'yosrio':
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return successLogin()

@app.route('/successLogin')
def successLogin():
	if session.get('logged_in'):
		return render_template('login.html')
	else:
    	return render_template('index.html')

@app.route('/signUp', methods=['POST','GET'])
def signUp():
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	if _name and _email and _password:
		conn = mysql.connect()
		cursor = conn.cursor()
		_hashed_password = generate_password_hash(_password)
		cursor.callproc('sp_createUser',(_name,_email,_hashed_password))

		data = cursor.fetchall()
		 
		if len(data) is 0:
		    conn.commit()
		    return json.dumps({'message':'User created successfully !'})
		else:
		    return json.dumps({'error':str(data[0])})
	else:
		return json.dumps({'html':'<span>Enter the required fields!</span>'})

if __name__ == "__main__":
    app.run(port = 5502)
