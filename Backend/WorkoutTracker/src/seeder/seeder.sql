CREATE SCHEMA IF NOT EXISTS workout_tracker;

CREATE TABLE IF NOT EXISTS  workout_tracker.users(
       id SERIAL PRIMARY KEY,
       user_name VARCHAR(255) UNIQUE,
       password_hash VARCHAR(255) -- possible to hash with plugins
       -- email varchar(255)
       ON DELETE CASCADE
);
-- ALTER TABLE workout_tracker.users RENAME COLUMN passowrd_hash TO password_hash;
-- https://www.dbvis.com/thetable/postgres-on-delete-cascade-a-guide/

CREATE TABLE IF NOT EXISTS workout_tracker.exercises (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL,
	exercise_group VARCHAR(255),
	muscle_group VARCHAR(255)[],
	equipment VARCHAR(255)[],
	intensity INTEGER,
	difficulty INTEGER,
	description VARCHAR(255) -- also url
);

CREATE TABLE IF NOT EXISTS workout_tracker.workouts(
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) UNIQUE,
	description VARCHAR(255),
	is_public BOOLEAN,
	user_id INTEGER REFERENCES workout_tracker.users(id)
);

-- user_id only if not public? or always okay?

CREATE TABLE IF NOT EXISTS workout_tracker.workouts_exercises(
	id SERIAL UNIQUE,-- PRIMARY KEY UNIQUE,
	workout_id INTEGER REFERENCES workout_tracker.workouts(id),
	exercise_id INTEGER REFERENCES workout_tracker.exercises(id),
	weight INTEGER,
	sets INTEGER,
	reps INTEGER,
	rest INTEGER,
	ord INTEGER NOT NULL,
	PRIMARY KEY (workout_id, exercise_id, ord)
);
-- Because there is lots of exercises in a workout that might change.
-- select * from /// which workout_id = ///; -- then sort them based on order (ord)



CREATE TABLE IF NOT EXISTS workout_tracker.schedules(
	id SERIAL PRIMARY KEY UNIQUE,
	user_id INTEGER REFERENCES workout_tracker.users(id),
	workout_id INTEGER REFERENCES workout_tracker.workouts(id),
	schedule_date DATE,
	schedule_time TIME,
	status BOOLEAN,
	repeat INTERVAL,
	deadline DATE
);

---
INSERT INTO workout_tracker.exercises (name, muscle_group, equipment)
VALUES
	('Push Up', '{"pecs","triceps"}', '{}'),
	('Pull Up', '{"lats","biceps"}', '{"bar"}'),
	('Squats', '{"quads","glutes"}', '{}'),
	('Barbell Squats', '{"quads","glutes"}', '{"barbell"}'),
	('Goblin Squats', '{"quads","glutes"}', '{"dumbbell"}'),
	('Barbell Shrug', '{"traps"}', '{"barbell"}'),
	('Dumbbell Shrug', '{"traps"}', '{"dumbbell"}'),
	('Bicep Curls', '{"biceps"}', '{"dumbbell"}'),
	('Hammer Curls', '{"biceps"}', '{"dumbbell"}'),
	('Overhead Tricep Extension', '{"triceps"}', '{"dumbbell"}'),
	('Dumbbell Bench Press', '{"pecs","triceps"}', '{"dumbbell"}'),
	('Dumbbell Chest Fly', '{"pecs"}', '{"dumbbell"}'),
	('Dumbbell Forward Lunges', '{"quads","glutes"}', '{"dumbbell"}'),
	('Leg Press Machine', '{"quads"}', '{"machine"}'), -- name might be wrong
	('Machine Leg Extension', '{"quads"}', '{"machine"}')
ON CONFLICT (name) DO NOTHING;

---
INSERT INTO workout_tracker.workouts (name, description, is_public)
VALUES
	('Arms Day 001', 'Very basic public arms-day exercise for testing purposes', TRUE),
	('Legs Day 001', 'Very basic public legs-day exercise for testing purposes', TRUE)
ON CONFLICT (name) DO NOTHING;

---
-- WITH arms_day_id AS (SELECT id FROM workout_tracker.workouts WHERE name = 'Arms Day 001'),
-- arms_exercises AS (SELECT id FROM workout_tracker.exercises WHERE name in ('Bicep Curls', 'Hammer Curls', 'Ovearhead Tricep Extension')) -- this shit would've been way easier in python
-- 	INSERT INTO workout_tracker.workouts_exercises
-- 	(workout_id, exercise_id, weight, sets, reps, rest, ord)
-- 	VALUES
-- 		(arms_day_id, (SELECT id FROM arms_exercises WHERE name = 'Bicep Curls'), 10, 2, 8, 30, 1),
-- 		(arms_day_id, (SELECT id FROM arms_exercises WHERE name = 'Hammer Curls'), 10, 2, 8, 30, 2),
-- 		(arms_day_id, (SELECT id FROM arms_exercises WHERE name = 'Overhead Tricep Extension'), 12, 2, 8, 30, 3)
-- 	ON CONFLICT (name) DO NOTHING;;

INSERT INTO workout_tracker.workouts_exercises
       (workout_id, exercise_id, weight, sets, reps, rest, ord)
VALUES
	((SELECT id FROM workout_tracker.workouts WHERE name = 'Arms Day 001'),
		(SELECT id FROM workout_tracker.exercises WHERE name = 'Bicep Curls'),
		10, 2, 8, 30, 1),
	((SELECT id FROM workout_tracker.workouts WHERE name = 'Arms Day 001'),
		(SELECT id FROM workout_tracker.exercises WHERE name = 'Hammer Curls'), 10, 2, 8, 30, 2),
	((SELECT id FROM workout_tracker.workouts WHERE name = 'Arms Day 001'),
		(SELECT id FROM workout_tracker.exercises WHERE name = 'Overhead Tricep Extension'),
		12, 2, 8, 30, 3)
--ON CONFLICT (ord) DO NOTHING;
;

------- BUGS. Now I can fill a workout with CRAP!

INSERT INTO workout_tracker.workouts_exercises
       (workout_id, exercise_id, weight, sets, reps, rest, ord)
VALUES
	((SELECT id FROM workout_tracker.workouts WHERE name = 'Legs Day 001'),
		(SELECT id FROM workout_tracker.exercises WHERE name = 'Squats'),
		10, 2, 8, 30, 1),
	((SELECT id FROM workout_tracker.workouts WHERE name = 'Legs Day 001'),
		(SELECT id FROM workout_tracker.exercises WHERE name = 'Leg Press Machine'),
		10, 2, 8, 30, 2),
	((SELECT id FROM workout_tracker.workouts WHERE name = 'Legs Day 001'),
		(SELECT id FROM workout_tracker.exercises WHERE name = 'Goblin Squats'),
		10, 2, 8, 30, 3),
	((SELECT id FROM workout_tracker.workouts WHERE name = 'Legs Day 001'),
		(SELECT id FROM workout_tracker.exercises WHERE name = 'Machine Leg Extension'),
		12, 2, 8, 30, 4);

