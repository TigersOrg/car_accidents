-- Set params
-- set session my.number_of_users = '100';
-- set session my.number_of_cars = '100';


-- Create table users
CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    first_name varchar(100) NOT NULL,
    last_name varchar(100) NOT NULL,
    phone varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    car_num varchar(50) NOT NULL,
    country varchar(200) NOT NULL,
    city varchar(200) NOT NULL,
    a_role varchar(200) NOT NULL,
    created TIMESTAMP without time zone DEFAULT now() NOT NULL,
    updated TIMESTAMP without time zone DEFAULT now()
);

-- INSERT INTO users (first_name, last_name, phone, email, password, car_num, country, city, a_role, created, updated)
--     VALUES ( 'Ailn', 'Rathmouth', '051-444-61-974', 'mailn0@bravesites.com', 'password', 'AE56789KL', 'Ukraine',
--             'Dnipro', 'user', TO_TIMESTAMP('2022-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
--             TO_TIMESTAMP('2022-06-06 00:00:00', 'YYYY-MM-DD HH24:MI:SS'));

-- Create table cars
CREATE TABLE IF NOT EXISTS cars (
    id serial PRIMARY KEY,
    mark varchar(100) NOT NULL,
    model varchar(100) NOT NULL,
    car_num varchar(100) NOT NULL,
    created TIMESTAMP without time zone DEFAULT now(),
    updated TIMESTAMP without time zone DEFAULT now()
);

-- INSERT INTO cars (mark, model, car_num, created, updated)
--     VALUES ( 'Kia', 'Sportage', 'AE56789KL', TO_TIMESTAMP('2022-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
--             TO_TIMESTAMP('2022-06-05 00:00:00', 'YYYY-MM-DD HH24:MI:SS'));

-- Create table owner_car
CREATE TABLE IF NOT EXISTS owner_car (
  user_id INT,
  car_id INT,
  PRIMARY KEY (user_id, car_id),
  CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id),
  CONSTRAINT fk_car FOREIGN KEY(car_id) REFERENCES cars(id)
);


-- INSERT INTO owner_car (user_id, car_id)
--     VALUES (1, 1);
