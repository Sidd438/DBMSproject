-- 1 
select * from flights where source = 'Delhi' and destination = 'Mumbai' and cast(start_time as date)=curdate();

-- 2
select * from flights where cast(start_time as date)="2019-12-25";

-- 3
select * from seats where not exists (select * from bookings where bookings.seat_id = seats.seat_id and not bookings.status='cancelled') and flight_id=1;

-- 4
select seat_id, price from seats;

-- 5


-- 6
select * from seats where exists (select * from bookings where bookings.seat_id = seats.seat_id and not bookings.status='Cancelled' and bookings.user_id="a@gmail.com");

-- 7
update bookings set status='Cancelled' where booking_id=1;

-- 8
insert into passengers (email, password, name, date_of_birth) values ("c@gmail.com", "c", "c", "1999-12-12");

-- 9
select count(*) from seats where flight_id=1 and where seat_type="Business" and not exists (select * from bookings where bookings.seat_id = seats.seat_id and not bookings.status='Cancelled');

-- 10
update bookings set status='Confirmed' where booking_id=1;

-- 11
select sum(price) from seats where seat_id in (select seat_id from bookings where user_id="a@gmail.com" and (status="Confirmed" or status="Completed"));