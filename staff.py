#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, abort
import pymysql.cursors
from werkzeug.utils import environ_property
import mysql.connector
from random import randint
from datetime import date

#Initialize the app from Flask
app = Flask(__name__)
app.secret_key = 'any random string'

#Configure MySQL
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='root',
					   port = 3306,
                       db='university',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)



# function to get flight number from string
def get_flight(data, row):
    s = ""
    l = []
    idx = 0
    while idx < len(data):
        if data[idx] == "[" or data[idx] == "]":
            idx += 12
            continue
        if data[idx]== "}":
            s += data[idx]
            idx += 2
            l.append(s)
            s = ""
        else:
            s += data[idx]
            idx += 1

    data = l[row].strip("{}").split(",")[0]
    data = data.split(":")[1].split("'")[1]
    return int(data)  


@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cursor = conn.cursor()
        # Search for flights
        if 'flights' in request.form:
            departure = request.form['departure']
            arrival = request.form['arrival']
            outbound = request.form['outbound']
            trip_type = request.form['trip_type']
            try: return_ = request.form['return']
            except: return_ = False
            
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
            
            # one-way
            if trip_type == "one-way":
                
                query = "select distinct * from (select airline_name, flight_number, departure_date, departure_time, departure_airport_code, arrival_airport_code, airplane_ID, arrival_date, arrival_time, base_price, flight_status, city as departure_city from flight join airport on departure_airport_code = airport_code) as F natural join (select flight_number, city as arrival_city from flight join airport on arrival_airport_code = airport_code) as S where (departure_city = '%s' or departure_airport_code = '%s') and (arrival_city = '%s' or arrival_airport_code = '%s') and departure_date = '%s'" % (d_city, d_code, a_city, a_code, outbound)

                cursor.execute(query)
                data = cursor.fetchall()
                cursor.close()
                if data:
                    return render_template('flight_result.html', data=data, usr = "Public User", triptype = trip_type)
                else:
                    error = 'No information available'
                    return render_template('index.html', error=error)
            # round-trip
            else:

                data = "select distinct * from (select airline_name, flight_number, departure_date, departure_time, departure_airport_code, arrival_airport_code, airplane_ID, arrival_date, arrival_time, base_price, flight_status, city as departure_city from flight join airport on departure_airport_code = airport_code) as F natural join (select flight_number, city as arrival_city from flight join airport on arrival_airport_code = airport_code) as S where (departure_city = '%s' or departure_airport_code = '%s') and (arrival_city = '%s' or arrival_airport_code = '%s') and departure_date = '%s'" % (d_city, d_code, a_city, a_code, outbound)

                coming = "select distinct * from (select airline_name, flight_number, departure_date, departure_time, departure_airport_code, arrival_airport_code, airplane_ID, arrival_date, arrival_time, base_price, flight_status, city as departure_city from flight join airport on departure_airport_code = airport_code) as F natural join (select flight_number, city as arrival_city from flight join airport on arrival_airport_code = airport_code) as S where (departure_city = '%s' or departure_airport_code = '%s') and (arrival_city = '%s' or arrival_airport_code = '%s') and departure_date = '%s'" % (a_city, a_code, d_city, d_code, return_)

                cursor.execute(data)
                data = cursor.fetchall()
                cursor.execute(coming)
                coming = cursor.fetchall()
                cursor.close()

                if len(data) > 0 and len(coming) > 0:
                    return render_template('flight_result.html', data=data, coming=coming, usr = "Public User", triptype = trip_type)
                else:
                    error = 'No available information'
                    return render_template('index.html', error=error)

        else: # check status
            airline = request.form['airline']
            flight_num = request.form['flight_num']
            departure_date = request.form['departure_date']
            arrival_date = request.form['arrival_date']

            query = "SELECT airline_name, flight_number, departure_date, arrival_date, flight_status FROM flight WHERE airline_name='%s' AND flight_number='%s' AND departure_date ='%s' AND arrival_date = '%s'" % (airline, flight_num, departure_date, arrival_date)

            cursor.execute(query)
            data = cursor.fetchone()
            cursor.close()

            return render_template('status_result.html', data=data)
            
    else:
        return render_template('index.html')


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
                session['email'] = row['customer_email']
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


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        cursor = conn.cursor()
        row_num = int(request.form['row_num'])-1
        data = request.form['myField']
        try:
            data2 = request.form['myField2']
            row_num2 = int(request.form['row_num2'])-1
            flight_num2 = get_flight(data2, row_num2)
            flight_num = get_flight(data, row_num)
            check = True
            return render_template('purchase.html', flight = flight_num, flight2 = flight_num2, check = check)
        except:
            check = False
            flight_num = get_flight(data, row_num)
            return render_template('purchase.html', flight = flight_num, check = check)
    else:
        return render_template('purchase.html')



@app.route('/purchase_result', methods=['GET', 'POST'])
def purchase_result():
    if request.method == 'POST':
        cursor = conn.cursor()
        username = session['username']
        flight = request.form['flight']
        try:
            flight2 = request.form['flight2']
            check = request.form['check']
        except:
            pass

        card_num = request.form['card_num']
        card_type = request.form["card_type"]
        name = request.form['name']
        exp = request.form['exp']
        ticket_id = randint(10000000, 99999999)
        today = date.today()
        time = today.strftime("%H:%M:%S")

        query1 = "select flight_number, airline_name, departure_date, departure_time, base_price from flight where flight_number = '%s'" % (flight)
        cursor.execute(query1)
        r1 = cursor.fetchall()
        try:
            query2 = "select flight_number, airline_name, departure_date, departure_time, base_price from flight where flight_number = '%s'" % (flight2)
            cursor.execute(query2)
            r2 = cursor.fetchall()
        except:
            pass

        email = "select customer_email from customer where customer_name = '%s'" % (username)
        cursor.execute(email)
        email = cursor.fetchone()
        email = email['customer_email']

        if check == "False":
            if r1:
                for i in range(len(r1)):
                    see = "select * from ticket where customer_email = '%s' and flight_number = '%s'" % (email, flight)
                    cursor.execute(see)
                    if cursor.fetchone() is None:
                        query2 = "INSERT INTO ticket values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (ticket_id, email, r1[i]["flight_number"], r1[i]["airline_name"], r1[i]["departure_date"], r1[i]["departure_time"], r1[i]["base_price"], card_type, card_num, name, exp, today, str(time))
                        cursor.execute(query2)
                        conn.commit()
                        cursor.close()
                        return render_template('purchase_result.html', data = r1, usr=username, check = check)
                    else:
                        error = "You already bought the ticket for the following flight"
                        return render_template('purchase.html', error=error)
            else:
                error1 = "No flights found"
                return render_template('purchase.html', error=error1)
        else:
            if r1 and r2:
                for i in range(len(r1)):
                    see = "select * from ticket where customer_email = '%s' and flight_number = '%s'" % (email, flight)
                    cursor.execute(see)
                    if cursor.fetchone() is None:
                        query2 = "INSERT INTO ticket values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (ticket_id, email, r1[i]["flight_number"], r1[i]["airline_name"], r1[i]["departure_date"], r1[i]["departure_time"], r1[i]["base_price"], card_type, card_num, name, exp, today, str(time))
                        cursor.execute(query2)
                        conn.commit()
                    else:
                        error = "You already bought the ticket for the following flight"
                        return render_template('purchase.html', error=error)
                for i in range(len(r2)):
                    see = "select * from ticket where customer_email = '%s' and flight_number = '%s'" % (email, flight2)
                    cursor.execute(see)
                    if cursor.fetchone() is None:
                        ticket_id2 = randint(10000000, 99999999)
                        query3 = "INSERT INTO ticket values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (ticket_id2, email, r2[i]["flight_number"], r2[i]["airline_name"], r2[i]["departure_date"], r2[i]["departure_time"], r2[i]["base_price"], card_type, card_num, name, exp, today, str(time))
                        cursor.execute(query3)
                        conn.commit()
                        cursor.close()
                    else:
                        error = "You already bought the ticket for the following flight"
                        return render_template('purchase.html', error=error)
                return render_template('purchase_result.html', data = r1, data2 = r2, usr=username, check = check)
            else:
                error1 = "No flights found"
                return render_template('purchase.html', error=error1)
    else:
        return render_template('purchase_result.html')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
#~~~~~~~~~~~~~~~~~~~~~~~~~TAMAR~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/addflight', methods=['GET','POST'])
def addflight():

    if request.method == 'POST':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        
        #session is for staff
        else:
        
            airline = session['airline']

            flight_number = request.form['flight_number']
            departure_date = request.form['departure_date']
            departure_time = request.form['departure_time']
            departure_airport_code = request.form['departure_airport_code']
            arrival_airport_code = request.form['arrival_airport_code']
            airplane_ID = request.form['airplane_ID']
            arrival_date = request.form['arrival_date']
            arrival_time = request.form['arrival_time']
            base_price = request.form['base_price']
            status = request.form['status']



            reg_flights = "SELECT * FROM flight WHERE airline_name = %s"
            cursor = conn.cursor()
            cursor.execute(reg_flights, (airline))
            all_flights = cursor.fetchall()


            #checking if flight already registered 
            flight_check = "SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_date = %s AND departure_time =%s"
            cursor.execute(flight_check, (airline, flight_number,departure_date, departure_time))
            data1 = cursor.fetchone()

            if(data1):
                error = f"Flight{flight_number} already registered for {airline} on this date {departure_date} and time {departure_time}"
                return render_template('addflight.html', flights=all_flights, error=error, airline=airline)
            
            # #If a fligt is not registered they can add a new one
            flight_new = "INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
            cursor.execute(flight_new, (airline, flight_number, departure_date, departure_time, departure_airport_code, arrival_airport_code, airplane_ID, arrival_date, arrival_time, base_price, status))
            conn.commit()

            return render_template('addflight.html', flights=all_flights, airline=airline)
	
    else:
        return render_template('addflight.html')

#### view_customer
@app.route('/requestcust', methods=['GET','POST'])
def requestcust():
     if request.method == 'POST':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        
        #session is for staff
        else:
            airline = session['airline']
            flight_number =request.form['flight_number']
            cust_flights = '''SELECT 
                                    c.* 
                            FROM 
                                ticket t
                            left join
                                customer c
                            on 
                                t.customer_email=c.customer_email
                            WHERE 
                                t.airline_name = %s 
                                AND t.flight_number= %s'''
            cursor = conn.cursor()
            cursor.execute(cust_flights, (airline,flight_number))
            all_flights = cursor.fetchall()

            if (not all_flights):
                error = "No customers found"
                return render_template('requestcust.html', error = error)
            else:
                return render_template('viewcust.html',all_flights=all_flights)
     else:
         return render_template('requestcust.html')  

### Staff search for flight ###

@app.route('/staffsearch', methods=['GET','POST'])
def staffsearch():
     if request.method == 'POST':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        
        #session is for staff
        else:
        
            #defining the search input for 
            airline = session['airline']
            departure_date1 = request.form['departure_date1']
            departure_date2 = request.form['departure_date2']
            departure_airport_code = request.form['departure_airport_code']
            arrival_airport_code = request.form['arrival_airport_code']
            cursor = conn.cursor()

            test = '''SELECT * FROM flight WHERE (airline_name = %s) AND (departure_date between %s and %s)
            AND departure_airport_code=%s AND arrival_airport_code=%s'''
            cursor.execute(test, (airline,departure_date1,departure_date2,departure_airport_code,arrival_airport_code))
            updated_flight = cursor.fetchall()

            #search start date and end date
            #JFK to DXB 

            if (not test):
                error = "No flights found"
                return render_template('staffsearch.html', error = error)
            
            else:
                print("\n",updated_flight,"\n")
                # return updated_flight
                return render_template('staffresult.html',updated_flight=updated_flight)
                # return str(updated_flight)
                #flask template to render a list 
     
     else:
         return render_template('staffsearch.html')           

@app.route('/trackmyspending', methods=['GET','POST'])
def trackmyspending():
     if request.method == 'POST':
        if session['type'] == 'staff':
            abort(401)
        else:
            # username=session['username']
            cursor = conn.cursor()
            date1=request.form['date1']
            date2=request.form['date2']
            cursor = conn.cursor()
            email= session['email']

            requested_date='''SELECT SUM(ticket_sold_price) as Spent FROM Ticket WHERE customer_email = %s 
            AND ticket_purchase_date between %s and  %s
            GROUP BY YEAR(ticket_purchase_date), MONTH(ticket_purchase_date)'''
            cursor.execute(requested_date,(email,date1,date2))
            result= cursor.fetchall()

            if (not result):
                error = "No flight found"
                return render_template('trackmyspending.html', error = error)
            
            else:
                return str(result)

     
     else:
         return render_template('trackmyspending.html')
        
@app.route('/flightstatus',methods=['GET','POST'])
def flightstatus():
    if request.method == 'POST':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        
        #session is for staff
        else:
            airline = session['airline']

            flight_number = request.form['flight_number']
            departure_date = request.form['departure_date']
            departure_time = request.form['departure_time']
            status = request.form['flight_status']
            
            cursor = conn.cursor()

            test = "SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_date=%s AND departure_time=%s"
            cursor.execute(test, (airline, flight_number,departure_date,departure_time))
            updated_flight = cursor.fetchone()

            #check if empty query
            if (not updated_flight):
                error = "No flight found"
                return render_template('flightstatus.html', error = error)

            #else the flight exists and we ned to update it
            status_new = "UPDATE flight SET flight_status = %s WHERE flight_number = %s AND departure_date=%s"
            cursor.execute(status_new, (status, flight_number, departure_date))
            conn.commit()
            cursor.close()
            return render_template('flightstatus.html', flights=updated_flight)


    else:
        return render_template('flightstatus.html')
    
### staff adding an airplane ###

@app.route('/addplane', methods=['GET','POST'])
def addplane():
    if request.method == 'POST':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        
        #session is for staff
        else:
        
            airline = session['airline']
            airplane_ID=request.form['airplane_ID']
            num_seats=request.form['num_seats']

            cursor = conn.cursor()

            test = "SELECT * FROM airplane WHERE airline_name = %s AND airplane_ID=%s AND num_seats=%s"
            cursor.execute(test, (airline, airplane_ID,num_seats))
            plane = cursor.fetchone()

            # is query empty?
            if (plane):
                error = "Airplane already exists"
                return render_template('addflight.html', error = error)

            #else the plane doesnt exist and the staff memeber can add it 
            status_new = "INSERT INTO airplane VALUES(%s, %s, %s)"
            cursor.execute(status_new, (airplane_ID, airline, num_seats))
            conn.commit()
            cursor.close()
            return render_template('addplane.html', flights=plane)
    
    else:
        return render_template('addplane.html')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/addairport', methods=['GET','POST'])
def addairport():
    if request.method == 'POST':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        #session is for staff
        else:
            airport_code = request.form['airport_code']
            airport_name = request.form['airport_name']
            city = request.form['city']
            addAirportQ = "SELECT * FROM airport WHERE airport_code= '%s'"%(airport_code)
            cursor = conn.cursor()
            cursor.execute(addAirportQ)
            all_airport = cursor.fetchall()

            airport_check = "SELECT * FROM airport WHERE airport_code = '%s' AND airport_name = '%s' AND city = '%s'" %(airport_code, airport_name, city)

           
            cursor.execute(airport_check)
            data1 = cursor.fetchone()

            if(data1):
                error = f"Airport {airport_name} already added for {city}"
                return render_template('addairport.html', airport=all_airport, error=error)

            airport_new = "INSERT INTO airport VALUES( '%s', '%s', '%s')" %( airport_code, airport_name, city)
            cursor.execute(airport_new)
            conn.commit()

            return render_template('addairport.html', airport=all_airport)
	
    else:
        return render_template('addairport.html')


@app.route('/ratings')
def ratings():
    if request.method == 'GET':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        cursor = conn.cursor()
        # cursor.execute('SELECT flight_number, customer_experience_rating FROM customer_experience')
        cursor.execute('SELECT flight_number, AVG(customer_experience_rating) as avg_rate from customer_experience GROUP by flight_number')
        ratingData = cursor.fetchall()

        cursor.execute('SELECT flight_number as fn, customer_experience_comment as comment from customer_experience')
        commentData = cursor.fetchall()
        return render_template("ratings.html", ratingData = ratingData, commentData= commentData)
    return render_template("ratings.html")

@app.route('/freqCust')
def freqCust():
    if request.method == 'GET':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        cursor = conn.cursor()
        cursor.execute('SELECT customer_email, COUNT(ticket_ID) as totalTick  FROM ticket WHERE ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()GROUP BY customer_email')
        dataFreq = cursor.fetchall()

        cursor.execute('SELECT customer_email as ce, flight_number as fn FROM ticket WHERE ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()')
        dataFreqFlightVal = cursor.fetchall()


        return render_template("freqCust.html", dataFreq = dataFreq, dataFreqFlightVal =dataFreqFlightVal)
    return render_template("freqCust.html")

@app.route('/viewReport')
def freqCut():
    if request.method == 'GET':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(ticket_ID) as tickSum FROM `ticket`WHERE ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()")
        viewReportQ = cursor.fetchall()

        cursor.execute("SELECT COUNT(ticket_ID) as tickSum FROM `ticket`WHERE ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()")
        viewReportMQ = cursor.fetchall()

        
        cursor.execute("SELECT COUNT(ticket_ID) as tickSum, MONTH(ticket_purchase_date) as monthVal FROM `ticket`WHERE ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW() Group BY ticket_purchase_date")
        months = cursor.fetchall()
    
        return render_template("viewRep.html", viewReportQ = viewReportQ,viewReportMQ= viewReportMQ, months= months)
    return render_template("viewRep.html")

@app.route('/totalEarned')
def totalEarn():
    if request.method == 'GET':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
            
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(ticket_sold_price) as sumVal FROM `ticket`WHERE ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW() ")
        totalSaleMQ = cursor.fetchall()

        cursor.execute("SELECT SUM(ticket_sold_price) as sumVal FROM `ticket`WHERE ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL  1 YEAR) AND NOW()")
        totalSaleYQ = cursor.fetchall()
        return render_template("totalSale.html", totalSaleMQ = totalSaleMQ,totalSaleYQ= totalSaleYQ)
    return render_template("totalSale.html")

@app.route('/topDest')
def topDest():
    if request.method == 'GET':
        #end session if user is customer
        if session['type'] == 'customer':
            abort(401)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(A.city), A.city as cityDestVal FROM flight as F INNER JOIN ticket as T ON F.flight_number = T.flight_number INNER JOIN airport as A ON F.arrival_airport_code = A.airport_code WHERE T.ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()GROUP BY (A.city) ')
        topDestDataM = cursor.fetchall()

        cursor.execute('SELECT COUNT(A.city), A.city as cityDestVal FROM flight as F INNER JOIN ticket as T ON F.flight_number = T.flight_number INNER JOIN airport as A ON F.arrival_airport_code = A.airport_code WHERE T.ticket_purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()GROUP BY (A.city) ')
        topDestDataY = cursor.fetchall()
        return render_template("topDest.html", topDestDataM = topDestDataM, topDestDataY = topDestDataY)
    return render_template("topDest.html")

        


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('type', None)
    session.pop('airline', None)
    session.pop('email', None)
    message = "Successfully logged out!"
    return render_template('index.html', message = message)
    

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)