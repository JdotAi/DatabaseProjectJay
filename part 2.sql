### Problem 3
### a. One Airline name "China Eastern". 
INSERT INTO airline values ('China Eastern');
INSERT INTO airline values ('Ryanair');
INSERT INTO airline values ('American Airline');
INSERT INTO airline values ('Delta');
INSERT INTO airline values ('Asiana');

### b. At least Two airports named "JFK" in NYC and "PVG" in Shanghai.
INSERT INTO airport values ('JFK', 'John F. Kennedy International Airport', 'NYC');
INSERT INTO airport values ('PVG', 'Shanghai Pudong International Airport', 'Shanghai');
INSERT INTO airport values ('AUH', 'Abu Dhabi International Airport', 'Abu Dhabi');
INSERT INTO airport values ('DXB', 'Dubai International Airport', 'Dubai');
INSERT INTO airport values ('ICN', 'Incheon International Airport', 'Incheon');

### c. Insert at least three customers with appropriate names and other attributes. 
INSERT INTO customer values ('sl5583@nyu.edu', 'Sangjin Lee', 'abc1', '70 Washington Square S, New York, NY 10012', '6467890976', '2341564', '20301230', 'Republic of Korea', '19970306');
INSERT INTO customer values ('tah428@nyu.edu', 'Tamer Al-Haddadin', 'def1', '6 MetroTech Center, Brooklyn, NY 11201', '6467890333', '4567881', '20250915', 'Jordan', '19990506');    
INSERT INTO customer values ('jp5207@nyu.edu', 'Jay Patel', 'ghi1', '6 MetroTech Center, Brooklyn, NY 11201', '6460998343', '8898767', '20220615', 'US', '19991112');    


### d. Insert at least three airplanes. 
INSERT INTO airplane values ('EY875', 'Delta', 290);
INSERT INTO airplane values ('AH889', 'Ryanair', 295);
INSERT INTO airplane values ('YG312', 'China Eastern', 310);
INSERT INTO airplane values ('GL777', 'China Eastern', 305);
INSERT INTO airplane values ('AA333', 'Asiana', 320);


### e. Insert At least One airline Staff working for China Eastern.
INSERT INTO staff values ('ah3456', 'China Eastern', 'tag888', 'Chris', 'Watkins', '19890309');
INSERT INTO staff values ('jk7878', 'Delta', 'jokez12', 'Leroy', 'Debeer', '19910823');


### f. Insert several flights with on-time, and delayed statuses.
INSERT INTO flight values ('China Eastern', '123123', '2021-11-11', '15:50:00', 'JFK', 'PVG', 'YG312', '2021-11-12', '10:05:00', 950, 'on-time');
INSERT INTO flight values ('China Eastern', '890890', '2021-12-02', '11:10:00', 'PVG', 'JFK', 'GL777', '2021-12-02', '23:30:00', 880, 'delayed');
INSERT INTO flight values ('Asiana', '760769', '2022-01-02', '21:10:00', 'ICN', 'DXB', 'AA333', '2022-01-03', '21:45:00', 900, 'delayed');
INSERT INTO flight values ('Delta', '234234', '2021-12-28', '02:10:00', 'JFK', 'AUH', 'EY875', '2021-12-28', '10:45:00', 880, 'on-time');


### g. Insert some tickets for corresponding flights and insert some purchase records (customers bought some tickets).
INSERT INTO ticket values ('12345678', 'sl5583@nyu.edu', '123123', 'China Eastern', '2021-11-11', '15:50:00', 950, 'credit', 3645272837456378, 'SANGJIN LEE', '2025-07-20', '2021-10-15', '10:10:00');
INSERT INTO ticket values ('90123456', 'tah428@nyu.edu', '890890', 'China Eastern', '2021-12-02', '11:10:00', 880, 'debit', 8475890034567723, 'TAMER HADDADIN', '2026-08-20', '2021-11-10', '09:10:00');
