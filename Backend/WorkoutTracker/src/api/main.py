from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import jwt

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

## Flask App

app = Flask(__name__)


# Here you can globally configure all the ways you want to allow JWTs to
# be sent to your web application. By default, this will be only headers.
app.config["JWT_TOKEN_LOCATION"] = ["headers", "json"]  # "cookies", "query_string"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

# Change this in your code!
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

jwt = JWTManager(app)


@app.route("/")
def root():
    return jsonify(msg="Application Workout Tracker API is running."), 200


@app.route("/protected", methods=["POST", "GET"])
@jwt_required()
def protected_endpoint():
    return jsonify(logged_in_as=get_jwt_identity()), 200


## Configurations

DB_CONFIG = {
    "dbname": "workout_tracker",
    "user": "wt_admin",
    "password": "admin",
    "host": "localhost",
    "port": "5432",
}

# conn = psycopg2.connect(**DB_CONFIG)
# cursor = conn.cursor()

## USERS


@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data or not "username" in data or not "password" in data:
        return "Both username and password are required.", 400
    uname = data["username"]
    hashed_pwd = generate_password_hash(data["password"])
    # try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM workout_tracker.users WHERE users.user_name = (%s)", (uname,)
    )
    if cur.fetchone():
        return jsonify(msg="Username already taken."), 403  # or 409?
    cur.execute(
        "INSERT INTO workout_tracker.users (user_name, password_hash) VALUES (%s, %s)",
        (uname, hashed_pwd),
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(msg=f"{uname} created successfully."), 201
    # except:
    # return jsonify(msg="An expected error occurred"), 500


@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if (not data) or (not "username" in data) or (not "password" in data):
        return jsonify("Both username and password are required."), 400
    # try:
    uname = data["username"]
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM workout_tracker.users WHERE users.user_name = (%s)", (uname,)
    )
    the_user = cur.fetchone()
    if check_password_hash(the_user[2], data["password"]):
        access_token = create_access_token(identity=uname)
        return jsonify(msg="Login successful", access_token=access_token), 200
    else:
        return jsonify(msg="Login unsuccessful, wrong username or password."), 401
    # except:
    # return jsonify(msg="An expected error occurred"), 500


@app.route("/delete-account", methods=["DELETE"])
def delete_user():
    if False:
        return jsonify(msg="Not implemented yet"), 501
    data = request.get_json()
    if not data or not "username" in data or not "password" in data:
        return "Both username and password are required.", 400
    uname = data["username"]
    # try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM workout_tracker.users WHERE users.user_name = (%s)", (uname,)
    )
    the_user = cur.fetchone()
    if not the_user:
        return jsonify(msg="User not found"), 404
    if check_password_hash(the_user[2], data["password"]):
        cur.execute("DELETE FROM workout_tracker.users WHERE id = (%s)", (the_user[0],))
        # cur.execute("DELETE FROM workout_tracker.exercises WHERE id = (%s)", (the_user[0],))
        # cur.execute("DELETE FROM workout_tracker.workouts_exercises WHERE id = (%s)", (the_user[0],))
        cur.execute(
            "DELETE FROM workout_tracker.workouts WHERE user_id = (%s)", (the_user[0],)
        )
        cur.execute(
            "DELETE FROM workout_tracker.schedules WHERE user_id = (%s)", (the_user[0],)
        )
        ####################################################################################################
        ####################################################################################################
        ####################################################################################################
        # ON DELETE CASCADE?
        # AUTO RELOAD OF FLASK?
        ####################################################################################################
        ####################################################################################################
        ####################################################################################################
        conn.commit()
        cur.close()
        conn.close()
        return (
            jsonify(
                msg="User was deleted. (Related data might still remain in the systems.)"
            ),
            200,
        )
    else:
        return jsonify(msg="Wrong username or password."), 200
    if not __DEBUG:
        return jsonify(msg="An expected error occurred"), 500


@app.route("/change-password", methods=["POST"])
def chpwd_user():
    if True:
        return jsonify(msg="Not implemented yet"), 501


## Workouts
## Should only access personal and public ones!

# Create


# @protect() # this is so messy! {}
@app.route("/workout/new", methods=["POST"])
@jwt_required()
def create_workout():
    if False:
        return jsonify(msg="Not implemented yet"), 501
    data = request.get_json()
    print(data)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    uname = get_jwt_identity()
    cur.execute(
        "SELECT * FROM workout_tracker.users WHERE users.user_name = (%s)", (uname,)
    )
    the_user = cur.fetchone()
    cur.execute("SELECT * FROM workout_tracker.workouts WHERE name = %s", (data['name'],))
    if cur.fetchone():
        return jsonify(msg="Already exists"), 403
    cur.execute(
        "INSERT INTO workout_tracker.workouts (name, description, is_public, user_id) VALUES (%s, %s, False, %s)", (data['name'], data['description'], the_user[0])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(msg="Created a dummy workout successfully"), 200

# READ


@app.route("/workout/list", methods=["GET"])
@jwt_required(optional=True)
def list_workouts():
    uname = get_jwt_identity()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    if uname:
        cur.execute(
            "SELECT * FROM workout_tracker.users WHERE users.user_name = (%s)", (uname,)
        )
        the_user = cur.fetchone()
        cur.execute(
            "SELECT * FROM workout_tracker.workouts WHERE user_id = (%s) or is_public = True",
            (the_user[0],),
        )
        workouts = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(workouts=workouts), 200
    else:
        cur.execute("SELECT * FROM workout_tracker.workouts WHERE is_public = True")
        workouts = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(workouts=workouts), 200


@app.route("/workout/search/q=<query>", methods=["GET"])
@jwt_required(optional=True)
def search_workout(query):
    uname = get_jwt_identity()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    if uname:
        cur.execute(
            "SELECT * FROM workout_tracker.users WHERE users.user_name = (%s)", (uname,)
        )
        the_user = cur.fetchone()
        cur.execute(
            "SELECT id, name, description FROM workout_tracker.workouts WHERE (user_id = %s OR is_public = True ) AND (name ILIKE %s OR description ILIKE %s)",
            (the_user[0], f"%{query}%", f"%{query}%"),
        )
        workouts = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(workouts=workouts), 200
    else:
        cur.execute(
            "SELECT id, name, description FROM workout_tracker.workouts WHERE name ILIKE %s AND is_public = True",
            (f"%{query}%",),
        )
        # cur.execute("""
        # SELECT * FROM workout_tracker.workouts
        # WHERE (is_public = TRUE) AND name ILIKE %s
        # """, (f"%{query}%",))
        workouts = cur.fetchall()
        if not workouts or len(workouts) == 0:
            return jsonify(msg="Not found"), 404
        print(workouts)
        cur.close()
        conn.close()
        return jsonify(workouts=workouts), 200


@app.route("/workout/show/<workout_id>", methods=["GET"])
@jwt_required(optional=True)
def show_workout(workout_id):
    uname = get_jwt_identity()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM workout_tracker.workouts WHERE id = %s", (workout_id,)
        )
        the_workout = cur.fetchone()
        if uname:
            cur.execute(
                "SELECT * FROM workout_tracker.users WHERE user_name = %s", (uname,)
            )
            the_user = cur.fetchone()
            if the_workout[4]==the_user[0]:
                cur.close()
                conn.close()
                return jsonify(workout=the_workout), 200
        elif the_workout[3] == True:
            cur.close()
            conn.close()
            return jsonify(workout=the_workout), 200
        else:
            cur.close()
            conn.close()
            return jsonify(msg="Unauthorized"), 401
    except:
        cur.close()
        conn.close()
        return jsonify(msg="An unexpected issue occurred"), 500


# Update

# Delete

@app.route("/workout/delete/<workout_id>", methods=["POST"])
@jwt_required()
def delete_workout(workout_id):
    uname = get_jwt_identity()
    # data = request.get_json()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM workout_tracker.users WHERE users.user_name = (%s)", (uname,)
    )
    the_user = cur.fetchone()
    cur.execute(
        "SELECT * FROM workout_tracker.workouts WHERE id = (%s)", (workout_id,) # data['workout_id']
    )
    the_workout = cur.fetchone()
    if not the_workout:
        return jsonify(msg="Not found"), 404
    if the_user[0] == the_workout[4]:
            cur.execute(
                "DELETE FROM workout_tracker.workouts WHERE id = (%s)", (workout_id,)
            )
    else:
        cur.close()
        conn.close()
        return jsonify(msg="Not allowed"), 403
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(msg="Removed succesfully"), 200

## Exercises
## Should only access personal and public ones!

# Create

# Read


@app.route("/exercise/list", methods=["GET"])
def list_exercises():
    if True:
        return jsonify(msg="Not implemented yet"), 501

@app.route("/exercise/search/q=<query>", methods=["GET"])
def search_exercise():
    if True:
        return jsonify(msg="Not implemented yet"), 501



@app.route("/exercise/show/<id>", methods=["GET"])
def show_exercise(id):
    if True:
        return jsonify(msg="Not implemented yet"), 501



# Update

# Delete

## Schedules CRUD

# Everything is personal


## Application


def main():
    if __name__ == "__main__":
        print("Hi")
        app.run(debug=True)


app.run(debug=True)

print("Bye")
