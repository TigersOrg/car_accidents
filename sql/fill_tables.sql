-- Set params
set session my.number_of_users = '5';
set session my.number_of_cars = '7';
set session my.created_date = '2022-06-01 00:00:00';
set session my.updated_date = '2022-06-06 00:00:00';


INSERT INTO users
SELECT id, concat('User ', id),
concat('LastName ', id),
concat('067-444-61-97', id),
concat('mail', id, '@gmail.com'),
MD5(concat('password', id)),
concat('AE567', id, 'KN'),
'Ukraine',
'Dnipro',
'user',
TO_TIMESTAMP(created_date, 'YYYY-MM-DD HH24:MI:SS'),
TO_TIMESTAMP(updated_date, 'YYYY-MM-DD HH24:MI:SS')
FROM generate_series(2, current_setting('my.number_of_users')::int) as id,
current_setting('my.created_date') as created_date,
current_setting('my.updated_date') as updated_date;


INSERT INTO cars
SELECT id,
concat('Mark ', id),
concat('Model ', id),
concat('AE567', id, 'KN'),
TO_TIMESTAMP(created_date, 'YYYY-MM-DD HH24:MI:SS'),
TO_TIMESTAMP(updated_date, 'YYYY-MM-DD HH24:MI:SS')
FROM generate_series(2, current_setting('my.number_of_cars')::int) as id,
current_setting('my.created_date') as created_date,
current_setting('my.updated_date') as updated_date;


INSERT INTO owner_car (user_id, car_id)
VALUES
(2, 2),
(2, 3),
(3, 3),
(4, 4),
(4, 4);
