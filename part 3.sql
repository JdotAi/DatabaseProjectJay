### Problem 4
### a
select  * from flight where departure_date > CURRENT_DATE;

### b
select * from flight where flight_status ='delayed';

### c
select customer_name from customer where customer_email in (select customer_email from ticket);

### d
Select * from airplane where airline_name= 'China Eastern';
