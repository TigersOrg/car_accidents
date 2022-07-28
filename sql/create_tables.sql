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

-- Create table cars
CREATE TABLE IF NOT EXISTS cars (
    id serial PRIMARY KEY,
    mark varchar(100) NOT NULL,
    model varchar(100) NOT NULL,
    car_num varchar(100) NOT NULL,
    created TIMESTAMP without time zone DEFAULT now(),
    updated TIMESTAMP without time zone DEFAULT now()
);

-- Create table user_car
CREATE TABLE IF NOT EXISTS user_car (
  user_id INT,
  car_id INT,
  PRIMARY KEY (user_id, car_id),
  CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id),
  CONSTRAINT fk_car FOREIGN KEY(car_id) REFERENCES cars(id)
);
