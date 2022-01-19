INSERT INTO airline values ('Emirates');

INSERT INTO airport values ('JFK', 'John F. Kennedy International Airport', 'NYC');
INSERT INTO airport values ('BOS', 'Boston Logan International Airport', 'Boston');
INSERT INTO airport values ('PVG', 'Shanghai Pudong International Airport', 'Shanghai');
INSERT INTO airport values ('BEI', 'Beijing Capital International Airport', 'Beijing');
INSERT INTO airport values ('SHEN', 'Shenzhen Baoan International Airport', 'Shenzen');
INSERT INTO airport values ('SFO', 'San Francisco International Airport', 'SF');
INSERT INTO airport values ('LAX', 'Los Angeles International Airport', 'LA');
INSERT INTO airport values ('HKA', 'Hong Kong International Airport', 'Hong Kong');


INSERT INTO customer values ('testcustomer@nyu.edu', 'Test Customer 1', '1234', '1555 Jay St, Brooklyn, New York', '1234321421', '54321', '20251224', 'USA', '19991219');
INSERT INTO customer values ('user1@nyu.edu', 'User 1', '1234', '5405 Jay Street, Brooklyn, New York', '1234322422', '54322', '20251225', 'USA', '19991119');
INSERT INTO customer values ('user12@nyu.edu', 'User 2', '1234', '1702 Jay Street, Brooklyn, New York', '1234323423', '54323', '20251024', 'USA', '19991019');
INSERT INTO customer values ('user3@nyu.edu', 'User 3', '1234', '1890 Jay Street, Brooklyn, New York', '1234324424', '54324', '20250924', 'USA', '19990919');


INSERT INTO airplane values ('1', 'Delta', 4);
INSERT INTO airplane values ('2', 'Delta', 4);
INSERT INTO airplane values ('3', 'Delta', 50);


INSERT INTO staff values ('admin', 'Delta', 'abcd', 'Roe', 'Jones', '19780525');


INSERT INTO flight values ('Emirates', '102', '2021-11-12', '13:25:25', 'SFO', 'LAX', '3', '2021-11-12', '16:50:25', 300, 'on-time');
INSERT INTO flight values ('Emirates', '104', '2021-12-09', '13:25:25', 'PVG', 'BEI', '3', '2021-12-09', '16:50:25', 300, 'on-time');
INSERT INTO flight values ('Emirates', '106', '2021-10-12', '13:25:25', 'SFO', 'LAX', '3', '2021-10-12', '16:50:25', 350, 'delayed');
INSERT INTO flight values ('Emirates', '206', '2022-01-09', '13:25:25', 'SFO', 'LAX', '2', '2022-01-09', '16:50:25', 400, 'on-time');
INSERT INTO flight values ('Emirates', '207', '2022-02-12', '13:25:25', 'LAX', 'SFO', '2', '2022-02-12', '16:50:25', 300, 'on-time');
INSERT INTO flight values ('Emirates', '134', '2022-08-12', '13:25:25', 'JFK', 'BOS', '3', '2022-08-12', '16:50:25', 300, 'delayed');
INSERT INTO flight values ('Emirates', '296', '2022-01-01', '13:25:25', 'PVG', 'SFO', '1', '2022-01-01', '16:50:25', 3000, 'delayed');
INSERT INTO flight values ('Emirates', '715', '2021-11-28', '10:25:25', 'PVG', 'BEI', '1', '2021-11-28', '13:50:25', 500, 'delayed');
INSERT INTO flight values ('Emirates', '839', '2021-02-12', '13:25:25', 'SHEN', 'BEI', '3', '2021-02-12', '16:50:25', 800, 'on-time');

INSERT INTO ticket values ('1','testcustomer@nyu.edu', '102', 'Emirates', '2021-11-12', '13:25:25', '300', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01','2021-10-14', '11:55:55');
INSERT INTO ticket values ('2','user1@nyu.edu', '102', 'Emirates', '2021-11-12', '13:25:25', '300', 'credit', '1111-2222-3333-5555', 'User 1', '2023-03-01','2021-10-13', '11:55:55');
INSERT INTO ticket values ('3','user2@nyu.edu', '102', 'Emirates', '2021-11-12', '13:25:25', '300', 'credit', '1111-2222-3333-5555', 'User 2', '2023-03-01','2021-11-14', '11:55:55');
INSERT INTO ticket values ('4','user1@nyu.edu', '104', 'Emirates', '2021-12-09', '13:25:25', '300', 'credit', '1111-2222-3333-5555', 'User 1', '2023-03-01','2021-10-21', '11:55:55');
INSERT INTO ticket values ('5','testcustomer@nyu.edu', '104', 'Emirates', '2021-12-09', '13:25:25', '300', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2021-11-28','2021-10-13', '11:55:55');
INSERT INTO ticket values ('6','testcustomer@nyu.edu', '106', 'Emirates', '2021-10-12', '13:25:25', '350', 'credit', '1111-2222-3333-5555', 'Test Customer 1', '2021-10-05','2021-10-13', '11:55:55');
INSERT INTO ticket values ('7','user3@nyu.edu', '106', 'Emirates', '2021-10-12', '13:25:25', '350', 'credit', '1111-2222-3333-5555', 'User 3', '2023-03-01','2021-09-03', '11:55:55');
INSERT INTO ticket values ('8','user3@nyu.edu', '839', 'Emirates', '2021-02-12', '13:25:25', '300', 'credit', '1111-2222-3333-5555', 'User 3', '2023-03-01','2021-02-13', '11:55:55');
INSERT INTO ticket values ('9','user3@nyu.edu', '102', 'Emirates', '2021-11-12', '13:25:25', '300', 'credit', '1111-2222-3333-5555', 'User 3', '2023-03-01','2021-03-09', '11:55:55');
INSERT INTO ticket values ('11','user3@nyu.edu', '134', 'Emirates', '2021-08-12', '13:25:25', '300', 'credit', '1111-2222-3333-5555', 'User 3', '2023-03-01','2021-02-23', '11:55:55');
INSERT INTO ticket values ('12','testcustomer@nyu.edu', '715', 'Emirates', '2021-11-28', '10:25:25', '500', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01','2021-10-05', '11:55:55');
INSERT INTO ticket values ('14','user3@nyu.edu', '206', 'Emirates', '2022-01-09', '13:25:25', '400', 'credit', '1111-2222-3333-5555', 'User 3', '2023-03-01','2021-12-05', '11:55:55');
INSERT INTO ticket values ('15','user1@nyu.edu', '206', 'Emirates', '2022-01-09', '13:25:25', '400', 'credit', '1111-2222-3333-5555', 'User 1', '2023-03-01','2021-12-06', '11:55:55');
INSERT INTO ticket values ('16','user2@nyu.edu', '206', 'Emirates', '2022-01-09', '13:25:25', '400', 'credit', '1111-2222-3333-5555', 'User 2', '2023-03-01','2021-11-19', '11:55:55');
INSERT INTO ticket values ('17','user1@nyu.edu', '207', 'Emirates', '2022-02-12', '13:25:25', '300', 'credit', '1111-2222-3333-5555', 'User 1', '2023-03-01','2021-10-14', '11:55:55');
INSERT INTO ticket values ('18','testcustomer@nyu.edu', '207', 'Emirates', '2022-02-12', '13:25:25', '300', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01','2021-11-25', '11:55:55');
INSERT INTO ticket values ('19','user1@nyu.edu', '296', 'Emirates', '2022-01-01', '13:25:25', '3000', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01','2021-12-04', '11:55:55');
INSERT INTO ticket values ('20','testcustomer@nyu.edu', '296', 'Emirates', '2022-01-01', '13:25:25', '3000', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01','2021-09-12', '11:55:55');

INSERT INTO customer_experience values('testcustomer@nyu.edu', 'Emirates', 102,'2021-11-12', '13:25:25', 'Very Comfortable','4');
INSERT INTO customer_experience values('user1@nyu.edu', 'Emirates', 102,'2021-11-12', '13:25:25', 'Relaxing, check-in and onboarding very professional','5');
INSERT INTO customer_experience values('user2@nyu.edu', 'Emirates', 102,'2021-11-12', '13:25:25', 'Satisfied and will use the same flight again','3');
INSERT INTO customer_experience values('testcustomer@nyu.edu', 'Emirates', 104,'2021-12-09', '13:25:25', 'Customer Care services are not good','1');
INSERT INTO customer_experience values('user1@nyu.edu', 'Emirates', 104,'2021-12-09', '13:25:25', 'Comfortable journey and Professional','5');

