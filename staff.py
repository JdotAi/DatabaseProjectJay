#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, abort
import pymysql.cursors
import mysql.connector

#Initialize the app from Flask
app = Flask(__name__)
app.secret_key = 'any random string'

#Configure MySQL
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='root',
					   port = 8889,
                       db='university',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/input_staff')
# def input_staff():
# 	return render_template('test.html')

# @app.route('/staffAuth', methods=['GET', 'POST'])
# def staffAuth():
#     username = request.form['username']
#     cursor = conn.cursor()
#     query = 'SELECT * FROM university.staff WHERE username = %s'
#     cursor.execute(query, (username))
#     data1 = cursor.fetchall() 
#     cursor.close()
#     print(data1)
#     if data1:
#         return render_template('staff_table.html', posts=data1)
#     else:
#         return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']

        if user_type == 'customer':
            cursor = conn.cursor()
            query = "SELECT * FROM customer WHERE customer_name='%s' AND customer_password='%s'" % (username, password)
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            if row:
                session['loggedin'] = True
                session['username'] = username
                session['type'] = 'customer'
                return redirect(url_for('home'))
            else:
                error = 'Invalid username and/or password'
                return render_template('login.html', error=error)

        else: #user_type == 'staff:'
            cursor = conn.cursor()
            query = "SELECT * FROM staff WHERE username='%s' AND staff_password='%s'" % (username, password)
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            if row:
                session['loggedin'] = True
                session['username'] = username
                session['type'] = 'staff'
                session['airline'] = row['airline_name']
                return redirect(url_for('home'))
            else:
                error = 'Invalid username and/or password'
                return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = conn.cursor()
        if 'customer' in request.form:
            query = "SELECT * FROM customer WHERE customer_name='%s' AND customer_password='%s'" % (username, password)
            cursor.execute(query)

            if cursor.fetchone() is None:
                email = request.form['email']
                address = request.form['address']
                phone = request.form['phone']
                passport = request.form['passport']
                passport_ex = request.form['passport_ex']
                passport_country = request.form['passport_country']
                dob = request.form['DoB']
                query2 = "INSERT INTO customer (customer_email, customer_name, customer_password, customer_address, customer_phone_number, customer_passport_number, customer_experation, passport_country, customer_doB) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"  % (email, username, password, address, phone, passport, passport_ex, passport_country, dob)
                cursor.execute(query2)
                conn.commit()
                return render_template('login.html')
            else:
                error = "User already exists"
                return render_template('register.html', error=error, usr=username)

        else:
            query = "SELECT * FROM staff WHERE username = '%s' AND staff_password='%s'" % (username, password)
            cursor.execute(query)

            if cursor.fetchone() is None:
                airline = request.form['airline_name']
                f = request.form['f_name']
                l = request.form['l_name']
                dob = request.form['DoB']
                query2 = "INSERT INTO staff (username, airline_name, staff_password, staff_F_name, staff_L_name, staff_dofB) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (username, airline, password, f, l, dob)
                cursor.execute(query2)
                conn.commit()
                return render_template('login.html')
            else:
                error = "User already exists"
                return render_template('register.html', error=error, usr=username)
    else:
        return render_template('register.html')


@app.route('/rate', methods=['GET', 'POST'])
def rate():
    username = session['username']
    usertype = session['type']
    cursor = conn.cursor()
    if request.method == 'POST':
        if usertype == 'customer':
            query = "select customer_email, airline_name, flight_number, departure_date, departure_time from customer natural join ticket where customer_name = '%s' and departure_date < CURRENT_DATE()" % (username)
            cursor.execute(query)
            row = cursor.fetchall()
            if row is None:
                error = "No previous flights found"
                return render_template('rate.html', error = error, usr=username)
            else:
                try:
                    idx = int(request.form['row_num']) - 1
                    comment = request.form['comment']
                    rating = request.form['rating']
                    query2 = "INSERT INTO customer_experience (customer_email, airline_name, flight_number, departure_date, departure_time, customer_experience_comment, customer_experience_rating) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"  % (row[idx]['customer_email'], row[idx]['airline_name'], row[idx]['flight_number'], row[idx]['departure_date'], row[idx]['departure_time'], comment, rating)
                    cursor.execute(query2)
                    conn.commit()
                    return render_template('rate.html', data = row, usr=username)
                except:
                    error = "You already submitted your comment for flight '{}' for '{}'".format(row[0]['flight_number'], row[0]['departure_date'])
                    return render_template('rate.html', data=row, error = error, usr=username)
        else: #user_type == 'staff:'
            error = "Sorry. Staff members are banned from this action."
            return render_template('rate.html', error = error, usr=username)
    else:
        query = "select customer_email, airline_name, flight_number, departure_date, departure_time from customer natural join ticket where customer_name = '%s' and departure_date < CURRENT_DATE()" % (username)
        cursor.execute(query)
        row = cursor.fetchall()
        return render_template('rate.html', data=row, usr=username)



@app.route('/home')
def home():

    username = session['username']
    usertype = session['type']

    cursor = conn.cursor()

    if 'username' in session:
        if usertype == 'customer':
            try:
                return render_template('home.html', usertype=usertype, usr=username)
            except:
                return render_template('login.html')
        else:
            # Staff
            try:
                airline = session['airline']
                return render_template('home.html', usertype=usertype, airline=airline)
            except:
                return render_template('login.html')


    else:
        return redirect(url_for('login'))


@app.route('/view_flights')
def view_flights():

    username = session['username']
    usertype = session['type']

    cursor = conn.cursor()

    if 'username' in session:
        if usertype == 'customer':
            query = "select flight_number, airline_name, departure_airport_code, departure_date, departure_time, arrival_airport_code, arrival_date, arrival_time from flight natural join ticket natural join customer where customer_name = '%s' and departure_date > CURRENT_DATE()" % (username)
            cursor.execute(query)
            data1 = cursor.fetchall() 
            cursor.close()
            if data1:
                return render_template('view_flights.html', posts=data1, usertype=usertype, usr=username)
            else:
                error = "You have not purchased any flights"
                return render_template('home.html', error=error) # FIX: when theres no purchased flights
        else:
            # Staff
            airline = session['airline']
            # date = request.form['preffered_date']
            query = "SELECT * FROM flight WHERE airline_name = '%s'" % (airline)
            cursor.execute(query)
            data1 = cursor.fetchall() 
            cursor.close()
            if data1:
                return render_template('view_flights.html', posts=data1, usertype=usertype, usr=username)
                # if date:
                #     return render_template('home.html', posts=data1, usertype=usertype, date = date)
            else:
                return render_template('index.html')
    else:
        return redirect(url_for('login'))
# @app.route('/staff_table', methods = ['GET', 'POST'])
# def staff_table():
#     # if request.method == 'POST':
#     #     username = session['username']
#     #     usertype = session['type']
#     #     flightNum = request.form['flight_number']

#     #     return render_template(
#     if request.method == 'GET':





@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if request.method == 'POST':
        username = session['username']
        usertype = session['type']
        departure = request.form['departure']
        arrival = request.form['arrival']
        outbound = request.form['outbound']
        cursor = conn.cursor()

        if 'one-way' in request.form:
            oneway = request.form['one-way']

            if len(departure) == 3:
                d_city = ""
                d_code = departure
            
            else:
                d_city = departure
                d_code = ""
            
            if len(arrival) == 3:
                a_city = ""
                a_code = arrival
            
            else:
                a_city = arrival
                a_code = ""
            
            query = "select distinct * from (select airline_name, flight_number, departure_date, departure_time, departure_airport_code, arrival_airport_code, airplane_ID, arrival_date, arrival_time, base_price, flight_status, city as departure_city from flight join airport on departure_airport_code = airport_code) as F natural join (select flight_number, city as arrival_city from flight join airport on arrival_airport_code = airport_code) as S where (departure_city = '%s' or departure_airport_code = '%s') and (arrival_city = '%s' or arrival_airport_code = '%s') and departure_date = '%s'" % (d_city, d_code, a_city, a_code, outbound)

            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            if data:
                print("\n",data,"\n")
                return render_template('search_flights_result.html', data=data, usr = username, triptype = oneway)
            else:
                error = 'No flights for given configuration'
                return render_template('search_flights.html', error=error)

        else: # round-trip
            return_ = request.form['return']

            if len(departure) == 3:
                d_city = ""
                d_code = departure
            
            else:
                d_city = departure
                d_code = ""
            
            if len(arrival) == 3:
                a_city = ""
                a_code = arrival
            
            else:
                a_city = arrival
                a_code = ""

            data = "select distinct * from (select airline_name, flight_number, departure_date, departure_time, departure_airport_code, arrival_airport_code, airplane_ID, arrival_date, arrival_time, base_price, flight_status, city as departure_city from flight join airport on departure_airport_code = airport_code) as F natural join (select flight_number, city as arrival_city from flight join airport on arrival_airport_code = airport_code) as S where (departure_city = '%s' or departure_airport_code = '%s') and (arrival_city = '%s' or arrival_airport_code = '%s') and departure_date = '%s'" % (d_city, d_code, a_city, a_code, outbound)

            coming = "select distinct * from (select airline_name, flight_number, departure_date, departure_time, departure_airport_code, arrival_airport_code, airplane_ID, arrival_date, arrival_time, base_price, flight_status, city as departure_city from flight join airport on departure_airport_code = airport_code) as F natural join (select flight_number, city as arrival_city from flight join airport on arrival_airport_code = airport_code) as S where (departure_city = '%s' or departure_airport_code = '%s') and (arrival_city = '%s' or arrival_airport_code = '%s') and departure_date = '%s'" % (a_city, a_code, d_city, d_code, return_)

            cursor.execute(data)
            data = cursor.fetchall()
            print("DATA >>>", data, "\n")
            cursor.execute(coming)
            coming = cursor.fetchall()
            print("COMING >>>", coming, "\n")
            cursor.close()

            if len(data) > 0 and len(coming) > 0:
                print("REQUEST.FORM >>>", request.form, "\n")
                return render_template('search_flights_result.html', data=data, coming=coming, usr = username, triptype = return_)
            else:
                error = 'No round-trip flights available'
                return render_template('search_flights.html', error=error)
    else:
        return render_template('search_flights.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('type', None)
    session.pop('airline', None)
    message = "Successfully logged out!"
    return render_template('index.html', message = message)
    

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)