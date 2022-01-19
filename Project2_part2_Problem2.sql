### Problem 2
### Creating tables

create table airline
	(airline_name varchar(30), 
	 primary key (airline_name)
	);
    
create table airport
	(airport_code varchar(5), 
     airport_name varchar(50),
     city varchar(10),
	 primary key (airport_code)
	);    

create table airplane
	(airplane_ID varchar(10),
     airline_name varchar(30),
     num_seats numeric(3,0),
	 primary key (airplane_ID, airline_name),
     foreign key (airline_name) references airline(airline_name)
	);
    
create table customer
	(customer_email varchar(20),
    customer_name varchar(20),
    customer_password varchar(20),
    customer_address varchar(50),
    customer_phone_number numeric(10,0),
    customer_passport_number numeric(10,0),
    passport_experation numeric(8,0),
    passport_country varchar(30),
    customer_doB numeric(8,0),
    primary key (customer_email)
    );

create table flight
	(airline_name varchar(20),
     flight_number numeric(6,0),
     departure_date date,
     departure_time time,
     departure_airport_code varchar(5),
     arrival_airport_code varchar(5),
     airplane_ID varchar(10),
     arrival_date date,
     arrival_time time,
	 base_price numeric(8,0),
     flight_status varchar(15),
	 primary key (airline_name, flight_number, departure_date, departure_time),
     foreign key (airline_name) references airline(airline_name),
     foreign key (departure_airport_code) references airport(airport_code),
     foreign key (arrival_airport_code) references airport(airport_code),
     foreign key (airplane_ID) references airplane(airplane_ID)
	);

create table ticket
	(ticket_ID numeric(8,0),
    customer_email varchar(20),
    flight_number numeric(6,0),
    airline_name varchar(20),
    departure_date date,
    departure_time time,
    ticket_sold_price numeric(4,0),
    card_type varchar(20),
    card_numer numeric(16,0),
    name_on_card varchar(20),
    expiration_date date,
    ticket_purchase_date date,
    ticket_purchase_time time,
    primary key (ticket_ID),
    foreign key (customer_email) references customer(customer_email),
    foreign key (airline_name, flight_number, departure_date, departure_time) references flight(airline_name, flight_number, departure_date, departure_time)
    );

create table customer_experience
	(customer_email varchar(20),
    airline_name varchar(20),
    flight_number numeric(6,0),
    departure_date date,
	departure_time time,
	customer_experience_comment varchar(100),
    customer_experience_rating numeric(5,0),
    primary key (customer_email, airline_name,flight_number,departure_date,departure_time),
    foreign key (customer_email) references customer(customer_email),
	foreign key (airline_name, flight_number, departure_date, departure_time) references flight(airline_name, flight_number, departure_date, departure_time)
);

create table staff
	(username varchar(20),
    airline_name varchar(20),
    staff_password varchar(20),
    staff_F_name varchar(20),
    staff_L_name varchar(20),
    staff_dofB numeric(8,0),
    primary key (username),
    foreign key(airline_name) references airline(airline_name)
    );
    
    create table staff_phone
	(username varchar(20),
    phone_number numeric(10,0),
    primary key (username, phone_number),
    foreign key (username) references staff(username)
);


