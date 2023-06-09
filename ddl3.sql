--
-- Create model Hostel
--
CREATE TABLE `hostels` (`hostel_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `capacity` integer NOT NULL);
--
-- Create model Room
--
CREATE TABLE `rooms` (`room_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `no_of_occ` integer NOT NULL, `hostel_id` integer NOT NULL);
--
-- Create model Student
--
CREATE TABLE `students` (`student_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `first_name` varchar(100) NOT NULL, `last_name` varchar(100) NOT NULL, `dob` date NOT NULL, `year_of_study` integer NOT NULL, `gender` varchar(100) NOT NULL, `hostel_id` integer NOT NULL, `room_id` integer NOT NULL);
--
-- Create model Warden
--
CREATE TABLE `atha_warden` (`warden_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `first_name` varchar(100) NOT NULL, `last_name` varchar(100) NOT NULL, `hostel_id` integer NOT NULL UNIQUE);
--
-- Create model StudentPhone
--
CREATE TABLE `student_phones` (`phone` varchar(100) NOT NULL, `student_id` integer NOT NULL PRIMARY KEY);
--
-- Create model WardenPhone
--
CREATE TABLE `warden_phones` (`phone` varchar(100) NOT NULL, `warden_id` integer NOT NULL PRIMARY KEY);
ALTER TABLE `rooms` ADD CONSTRAINT `rooms_hostel_id_6aa882ad_fk_hostels_hostel_id` FOREIGN KEY (`hostel_id`) REFERENCES `hostels` (`hostel_id`);
ALTER TABLE `students` ADD CONSTRAINT `students_hostel_id_35c16da6_fk_hostels_hostel_id` FOREIGN KEY (`hostel_id`) REFERENCES `hostels` (`hostel_id`);
ALTER TABLE `students` ADD CONSTRAINT `students_room_id_f7d03e22_fk_rooms_room_id` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`);
ALTER TABLE `atha_warden` ADD CONSTRAINT `atha_warden_hostel_id_83678989_fk_hostels_hostel_id` FOREIGN KEY (`hostel_id`) REFERENCES `hostels` (`hostel_id`);
ALTER TABLE `student_phones` ADD CONSTRAINT `student_phones_student_id_6f52c72b_fk_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);
ALTER TABLE `warden_phones` ADD CONSTRAINT `warden_phones_warden_id_eee87149_fk_atha_warden_warden_id` FOREIGN KEY (`warden_id`) REFERENCES `atha_warden` (`warden_id`);
