--
-- Create model Passenger
--
CREATE TABLE `passengers` (`password` varchar(100) NOT NULL, `email` varchar(254) NOT NULL PRIMARY KEY, `date_of_birth` date NULL, `name` varchar(100) NOT NULL);
CREATE TABLE `passengers_groups` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `passenger_id` varchar(254) NOT NULL, `group_id` integer NOT NULL);
CREATE TABLE `passengers_user_permissions` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `passenger_id` varchar(254) NOT NULL, `permission_id` integer NOT NULL);
--
-- Create model Booking
--
CREATE TABLE `bookings` (`booking_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `status` varchar(20) NOT NULL, `created_at` datetime(6) NOT NULL);
--
-- Create model Flight
--
CREATE TABLE `flights` (`flight_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `start_time` datetime(6) NOT NULL, `end_time` datetime(6) NOT NULL, `source` varchar(100) NOT NULL, `destination` varchar(100) NOT NULL);
--
-- Create model Cancellation
--
CREATE TABLE `cancellations` (`booking_id` integer NOT NULL PRIMARY KEY, `created_at` datetime(6) NOT NULL, `reason` longtext NOT NULL);
--
-- Create model SMS
--
CREATE TABLE `sms` (`sms_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `body` longtext NOT NULL, `created_at` datetime(6) NOT NULL, `recepient_id` varchar(254) NOT NULL);
--
-- Create model Seat
--
CREATE TABLE `seats` (`seat_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `seat_type` varchar(100) NOT NULL, `flight_id` integer NOT NULL);
--
-- Create model Email
--
CREATE TABLE `emails` (`em_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `subject` varchar(100) NOT NULL, `body` longtext NOT NULL, `created_at` datetime(6) NOT NULL, `recepient_id` varchar(254) NOT NULL);
--
-- Add field seat to booking
--
ALTER TABLE `bookings` ADD COLUMN `seat_id` integer NOT NULL , ADD CONSTRAINT `bookings_seat_id_05dfaa38_fk_seats_seat_id` FOREIGN KEY (`seat_id`) REFERENCES `seats`(`seat_id`);
--
-- Add field user to booking
--
ALTER TABLE `bookings` ADD COLUMN `user_id` varchar(254) NOT NULL , ADD CONSTRAINT `bookings_user_id_6e734b08_fk_passengers_email` FOREIGN KEY (`user_id`) REFERENCES `passengers`(`email`);
ALTER TABLE `passengers_groups` ADD CONSTRAINT `passengers_groups_passenger_id_group_id_a079617a_uniq` UNIQUE (`passenger_id`, `group_id`);
ALTER TABLE `passengers_groups` ADD CONSTRAINT `passengers_groups_passenger_id_b4628fce_fk_passengers_email` FOREIGN KEY (`passenger_id`) REFERENCES `passengers` (`email`);
ALTER TABLE `passengers_groups` ADD CONSTRAINT `passengers_groups_group_id_b8a400c5_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `passengers_user_permissions` ADD CONSTRAINT `passengers_user_permissi_passenger_id_permission__25761e5b_uniq` UNIQUE (`passenger_id`, `permission_id`);
ALTER TABLE `passengers_user_permissions` ADD CONSTRAINT `passengers_user_perm_passenger_id_626f4e15_fk_passenger` FOREIGN KEY (`passenger_id`) REFERENCES `passengers` (`email`);
ALTER TABLE `passengers_user_permissions` ADD CONSTRAINT `passengers_user_perm_permission_id_8d4b1bf7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `cancellations` ADD CONSTRAINT `cancellations_booking_id_a4cfa381_fk_bookings_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`);
ALTER TABLE `sms` ADD CONSTRAINT `sms_recepient_id_65c69568_fk_passengers_email` FOREIGN KEY (`recepient_id`) REFERENCES `passengers` (`email`);
ALTER TABLE `seats` ADD CONSTRAINT `seats_flight_id_e61b3bde_fk_flights_flight_id` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`);
ALTER TABLE `emails` ADD CONSTRAINT `emails_recepient_id_88069420_fk_passengers_email` FOREIGN KEY (`recepient_id`) REFERENCES `passengers` (`email`);
