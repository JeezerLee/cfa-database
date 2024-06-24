from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from datetime import datetime
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '53jas01ksdlqwepo14ndamcnxzlapmn1234'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'usadapekora'
app.config['MYSQL_DB'] = 'cfa_database'

Bootstrap(app)
# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `database`')
        data = cursor.fetchall()
        if request.method == 'POST' and 'search_id' in request.form:
            return redirect(url_for('search', studentid=request.form['search_id']))
        elif request.method == 'POST' and 'student_id' in request.form:
            studentid = request.form['student_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT MAX(access_id) AS count FROM access_logs')
            access_count = cursor.fetchall()
            if access_count[0]['count'] is None:
                count = 0
            else:
                count = access_count[0]['count'] + 1
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute('INSERT INTO access_logs VALUES (%s, %s, %s, %s)', (count, studentid, session['username'], dt_string))
            mysql.connection.commit()
        if(session['role'] == 'admin'):
            return render_template('admin_mode.html', username=session['username'], database = data)
        else:
            return render_template('home.html', username=session['username'], database = data)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['role'] = account['role']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('role', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        passwordval = request.form['passwordval']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        elif password != passwordval:
            msg = 'Passwords do not match!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (%s, %s, "user")', (username, password,))
            mysql.connection.commit()
            msg = 'New account created!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/search/<studentid>')
def search(studentid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM `database` WHERE student_id = %s', (studentid,))
    search_result = cursor.fetchall()
    if request.method == 'POST' and 'search_id' in request.form:
        return redirect(url_for('search', studentid=request.form['search_id']))
    return render_template('home.html', database = search_result)

@app.route('/remarks/<studentid>', methods=['GET', 'POST'])
def remarks(studentid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM remarks WHERE student_id = %s', (studentid,))
    remarks = cursor.fetchall()
    return render_template('remarks.html', remarks = remarks, studentid = studentid)

@app.route('/new_remark/<studentid>', methods=['GET', 'POST'])
def new_remark(studentid):
    if request.method == 'POST' and 'remark' in request.form:
        remark = request.form['remark']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT MAX(remark_id) AS count FROM remarks')
        remark_count = cursor.fetchall()
        count = remark_count[0]['count'] + 1
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute('INSERT INTO remarks VALUES (%s, %s, %s, %s, %s)', (count, studentid, remark, dt_string, session['username']))
        mysql.connection.commit()
        return redirect(url_for('remarks', studentid=studentid))
    return render_template('new_remark.html', studentid = studentid, adviser = session['username'])

@app.route('/accesslogs', methods=['GET', 'POST'])
def accesslogs():
    if session['role'] == 'admin':
        if request.method == 'POST' and 'search_id' in request.form:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM access_logs WHERE student_accessed = %s', (request.form['search_id'],))
            logs = cursor.fetchall()
            return render_template('accesslogs.html', database = logs)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM access_logs')
            logs = cursor.fetchall()
            return render_template('accesslogs.html', database = logs)
    else:
        return redirect(url_for('home'))

@app.route('/new_record', methods=['GET', 'POST'])
def new_record():
    if session['role'] == 'admin':
        if request.method == 'POST' and 'studentid' in request.form and 'studentname' in request.form and 'link' in request.form:
            studentid = request.form['studentid']
            studentname = request.form['studentname']
            link = request.form['link']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO `database` VALUES (%s, %s, %s)', (studentid, studentname, link))
            mysql.connection.commit()
            msg = f'The student record for {studentid} has been created.'
            return render_template('new_record.html', msg=msg)
        return render_template('new_record.html')
    else:
        return redirect(url_for('home'))

# select a record to edit or delete
@app.route('/select_record', methods=['GET', 'POST'])
def select_record():
    if session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `database`')
        search_result = cursor.fetchall()
        if request.method == 'POST' and 'search_id' in request.form:
            return redirect(url_for('search_select_record', studentid=request.form['search_id']))
        return render_template('select_record.html', database = search_result)
    else:
        return redirect(url_for('home'))

# search a record to edit or delete
@app.route('/select_record/<studentid>')
def search_select_record(studentid):
    if session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `database` WHERE student_id = %s', (studentid,))
        search_result = cursor.fetchall()
        return render_template('select_record.html', database = search_result, search=1)
    else:
        return redirect(url_for('home'))

# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['GET', 'POST'])
def edit_or_delete():
    if session['role'] == 'admin':
        id = request.form['id']
        choice = request.form['choice']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `database` WHERE student_id = %s', (id,))
        record = cursor.fetchone()
        return render_template('edit_or_delete.html', record=record, choice=choice)
    else:
        return redirect(url_for('home'))

# result of delete - this function deletes the record
@app.route('/delete_result', methods=['GET', 'POST'])
def delete_result():
    if session['role'] == 'admin':
        id = request.form['studentid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM `database` WHERE student_id = %s', (id,))
        mysql.connection.commit()
        message = f"The records of student {id} has been deleted from the database."
        return render_template('result.html', message=message)
    else:
        return redirect(url_for('home'))

@app.route('/edit_result', methods=['POST'])
def edit_result():
    if session['role'] == 'admin':
        id = request.form['studentid']
        name = request.form['studentname']
        link = request.form['link']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE `database` SET student_name = %s, link_to_records = %s WHERE student_id = %s", (name, link, id,))
        mysql.connection.commit()
        message = f"The data for student {id} has been updated."
        return render_template('result.html', message=message)
    else:
        return redirect(url_for('home'))

# select a user to edit or delete
@app.route('/select_user', methods=['GET', 'POST'])
def select_user():
    if session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts')
        search_result = cursor.fetchall()
        if request.method == 'POST' and 'search_id' in request.form:
            return redirect(url_for('search_select_user', username=request.form['search_id']))
        return render_template('select_user.html', database = search_result)
    else:
        return redirect(url_for('home'))

# search a user to edit or delete
@app.route('/select_user/<username>')
def search_select_user(username):
    if session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        search_result = cursor.fetchall()
        return render_template('select_user.html', database = search_result, search=1)

# edit or delete - come here from form in /select_record
@app.route('/edit_delete_user', methods=['GET', 'POST'])
def edit_delete_user():
    if session['role'] == 'admin':
        id = request.form['id']
        choice = request.form['choice']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (id,))
        record = cursor.fetchone()
        return render_template('edit_delete_user.html', record=record, choice=choice)
    else:
        return redirect(url_for('home'))

# result of delete - this function deletes the user
@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if session['role'] == 'admin':
        id = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM accounts WHERE username = %s', (id,))
        mysql.connection.commit()
        message = f"The account {id} has been deleted."
        return render_template('result_user.html', message=message)
    else:
        return redirect(url_for('home'))

@app.route('/edit_user', methods=['POST'])
def edit_user():
    if session['role'] == 'admin':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET username = %s, password = %s WHERE username = %s", (username, password, username,))
        mysql.connection.commit()
        message = f"The account information of {username} has been updated."
        return render_template('result_user.html', message=message)

if __name__ == "__main__":
    app.run()