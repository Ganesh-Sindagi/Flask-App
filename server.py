from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import pprint

from appdef import app, conn

# Authenticates the login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        #grabs the information from the forms
        email = request.form['user']
        password = request.form['passn']
        #cursor used to send queries
        cursor = conn.cursor()
        #Query the database
        query = 'SELECT user_id, password, username FROM user WHERE email = %s'
        cursor.execute(query, (email))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if(data):
            #creates a session for the the user
            #session is a built in
            print(data) 
            session['username'] = data['username']
            session['user_id'] = data['user_id']
            return redirect(url_for('studentdetails')) 
        else:
            #returns an error message to the html page
            error = 'Invalid login or username'
            return render_template('login.html', error=error)


@app.route('/studentdetails', methods=['GET', 'POST'])
def studentdetails():
    if request.method == 'GET':
        return render_template('studentdetails.html', user_name = session['username'], user_id = session['user_id'])
    elif request.method == 'POST':
        name = request.form['name']
        usn = request.form['usn']
        phone_no = request.form['phoneno']
        email_id = request.form['emailid']
        address = request.form['address']
        user_id = request.form['user_id']
        pp = pprint.PrettyPrinter()
        pp.pprint(request.form)
        cursor = conn.cursor()
        query = "INSERT INTO studentdetails (std_id, name, usn, phone_no, email_id, address) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, [user_id, name, usn, phone_no, email_id, address])
        conn.commit()
        return render_template('department.html', user_id = session['user_id'])


@app.route('/department', methods=['GET', 'POST'])
def department():
    if request.method == 'GET':
        return render_template('department.html')
        