# import sqlite3

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy as sqla
from functools import wraps
import base64, json, hmac, hashlib  # For manual JWT
from os import environ
from time import time

## Configurations


if "SECRET_KEY" in environ:
    SECRET_KEY = environ["SECRET_KEY"]
else:
    SECRET_KEY = "my_dummy_secret_key"

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(__file__).parent}/database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


@app.route("/")
def root():
    return "This is the root, welcome.", 200  # OK


db = sqla(app)


@app.route("/sdb", methods=["GET"])
def sdb():
    """
    Set-up DataBase
    """
    db.create_all()
    return jsonify({"message": "Created all tables for the database."}), 200


## Custom JWT implementation


def create_jwt(
    payload: json,
    secret: str = SECRET_KEY,
    header: json = {"alg": "HS256", "typ": "JWT"},
):
    """
    Creates a JSON Web Token
    """
    if header["alg"] != "HS256":
        return "Not Implemented", 501
    header_s = (
        base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip("=")
    )  # What a mess!
    payload_s = (
        base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip("=")
    )
    signature = hmac.new(
        secret.encode(), f"{header_s}.{payload_s}".encode(), hashlib.sha256
    ).digest()
    signature_s = base64.urlsafe_b64encode(signature).decode().strip("=")
    return f"{header_s}.{payload_s}.{signature_s}"


def verify_jwt(jwt, secret=SECRET_KEY):
    try:
        h, p, s = jwt.split(".")
        header = base64.urlsafe_b64decode(h + "==").decode()
        payload = base64.urlsafe_b64decode(p + "==").decode()
        s_c = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
        s_s = base64.urlsafe_b64encode(s_c).decode().strip("=")
        # print("\x1b[33m=====Verify JWT Begins\x1b[0m")
        if s_s != s:
            print(
                "\x1b[31m======================\n"
                + "Bad signature!\n"
                + "======================\x1b[0m"
            )
            return False
        else:
            pj = json.loads(payload)
            # ttt = int(pj
            if float(pj["exp"]) > time():
                # print("\x1b[33m=====OKAY\x1b[0m")
                return payload
            else:
                print(
                    "\x1b[31m======================\n"
                    + "The token has expired!\n"
                    + "======================\x1b[0m"
                )
                return False
    except:
        print("\x1b[33m Unexpected error\x1b[0m")
        return False


## Users


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # The Todo is the name of the class, not the table!
    todos = db.relationship("Todo", backref="user", lazy=True)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not "username" in data or not "password" in data:
        return "Both username and password are required.", 400  # Bad request
    # if db.User.query.filter_by(username=data["username"]).first():
    # return jsonify({"error": "Username already exists"}), 400
    hpass = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hpass)
    try:
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "User registered successfully.",
                    "usename": data["username"],
                }
            ),
            201,  # Created
        )
    except Exception as e:
        return (
            jsonify({"error": "An error occured.", "usename": data["username"]}),
            500,  # An unexpected error.
        )
    return jsonify(data)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not "username" in data or not "password" in data:
        return "Both username and password are required.", 400

    u = data["username"]
    try:
        user = db.session.execute(db.select(User).filter_by(username=u)).scalar_one()
        #
        # THIS HERE IS AN EXAMPLE OF BAD PRACTICE:
        # Why? Because they will know /the username/ is wrong, lowering the security.
        # except:
        #     return jsonify({'message':'User not found.'}), 404
        #
        p = data["password"]
        if check_password_hash(user.password, p):
            token = create_jwt(
                payload={"sub": str(user.id), "exp": str(time() + 3600)}
            )
            return jsonify({"token": token}), 200
        else:
            return jsonify({"message": "Wrong username or password."}), 401
    except:
        return jsonify({"message": "Something failed and IDK why."}), 500


## Add update/delete User here

## Security


def protect_endpoint():
    def decor(func):
        # print("\x1b[32m Decor begins\x1b[0m")
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (
                # I'm not yet comfortable with that /Bearer/ format.
                verify_jwt(request.headers["Authorization"]) # ( ___ .split(" ")[1])
                and len(
                    list(
                        db.session.execute(
                            db.select(User).filter_by(
                                username=request.get_json()["username"]
                            )
                        ).scalars()
                    )
                )
                != 0
                and db.session.execute(
                    db.select(User).filter_by(username=request.get_json()["username"])
                )
                .scalar_one()
                .id
                == int(json.loads(verify_jwt(request.headers["Authorization"]))["sub"]) # OR ((( ___ .split(" ")[1]))["sub"])
            ) or request.headers[
                "Authorization"
            ] == "admin":  # INSECURE AND FOR DEBUGGIN ONLY, REMOVE AFTER PRODUCTION.
                print("\x1b[32m Valid\x1b[0m")
                # print(type(a))
                # print(a)

                result = func(*args, **kwargs)
                return result
            else:
                return jsonify({"message": "Unauthorized!"}), 401

        return wrapper

    return decor


## TODO


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=False)


## TODO CRUD


@app.route("/todos", methods=["POST"])  # Use /Authorization/ header to recognize user.
@protect_endpoint()
def new_todo():
    ## **THIS MIGHT BE INSECURE**, but I have no idea right now.
    print("\x1b[32m POST TODO\x1b[0m")
    user_id = (
        db.session.execute(
            db.select(User).filter_by(username=request.get_json()["username"])
        )
        .scalar_one()
        .id
    )
    data = request.get_json()
    # What if the data fields do not exist?!
    try:
        todo = data["todo"]
    except KeyError:
        return jsonify({"message": "No TODO was provided."}), 500
    try:
        title = todo["title"]
    except KeyError:
        return jsonify({"message": "No title was provided."}), 500
    try:
        description = todo["description"]
    except KeyError:
        description = ""
    try:
        status = todo["status"]
    except KeyError:
        status = False

    try:
        new_todo = Todo(
            user_id=user_id,
            title=title,
            description=description,
            status=status,
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({"message": "OK"}), 200
    except:
        return jsonify({"message": "WTF, An unexpected error occured."}), 500


@app.route("/todos", methods=["GET"])
@protect_endpoint()
def open_todo():
    print("\x1b[32m GET TODO\x1b[0m")
    data = request.get_json()
    # I don't care if you add user_id in your request data, I expect a username.
    user_id = (
        db.session.execute(db.select(User).filter_by(username=data["username"]))
        .scalar_one()
        .id
    )
    if "id" in data:
        item = db.get_or_404(Todo, data["id"])
        if item.user_id == user_id:
            task_j = {
                "id": item.id,
                "title": item.title,
                "status": item.status,
                "description": item.description,
            }
            return jsonify(task_j), 200
        else:
            return jsonify({"message": "Unauthorized!"}), 401
    else:
        tasks = db.session.execute(db.select(Todo).filter_by(user_id=user_id)).scalars()
        # return jsonify(tasks), 200
        # IDK how to return proper results right now.
        tasks_j = []
        for item in tasks:
            tasks_j += [
                {
                    "id": item.id,
                    "title": item.title,
                    "status": item.status,
                    "description": item.description,
                }
            ]
        return jsonify(tasks_j)
        # return jsonify({"message": "OK"}), 200
    return jsonify({"message": "WTF, An unexpected error occured."}), 500


# The main source suggested /todos/<id> route for the next two operations.
# I don't like that inconsistent BS so I'm using my own format.

# {"username": ,
# "id": , # this is task's ID
# "title": , # OR
# "description": , OR
# "status": ,
# }


@app.route("/todos", methods=["PUT"])
@protect_endpoint()
def edit_todo():
    print("\x1b[32m PUT TODO\x1b[0m")
    data = request.get_json()
    # I don't care if you add user_id in your request data, I expect a username.
    # And indeed I am copy pasting my own code. I do not know enought to abstract
    # the whole thing cleanly.
    user_id = (
        db.session.execute(db.select(User).filter_by(username=data["username"]))
        .scalar_one()
        .id
    )
    if "id" in data:
        item = db.get_or_404(Todo, data["id"])
        if item.user_id != user_id:
            return jsonify({"message": "Unauthorized"}), 401
        item_j = {}
        try:
            item.title = data["title"]
            item_j["title"] = data["title"]
        except:
            pass
        try:
            item.description = data["description"]
            item_j["description"] = data["description"]
        except:
            pass
        try:
            item.status = data["status"]
            item_j["status"] = data["status"]
        except:
            pass
        db.session.commit()
        return jsonify({"message": "OK, todo updated.", "todo": item_j}), 200
    else:
        return jsonify({"message": "An ID is necessary!"}), 400
    return jsonify({"message": "WTF, An unexpected error occured."}), 500


@app.route("/todos", methods=["DELETE"])
@protect_endpoint()
def delete_todo():
    print("\x1b[32m DELETE TODO\x1b[0m")
    # db.session.delete(obj)
    # db.session.commit()
    data = request.get_json()
    user_id = (
        db.session.execute(db.select(User).filter_by(username=data["username"]))
        .scalar_one()
        .id
    )
    if "id" in data:
        item = db.get_or_404(Todo, data["id"])
        if item.user_id != user_id:
            return jsonify({"message": "Unauthorized"}), 401
        myid = item.id
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": f"todo with id {myid} removed"}), 200
    else:
        return jsonify({"message": "An ID is necessary!"}), 400
    return jsonify({"message": "WTF, An unexpected error occured."}), 500


@app.route("/something")
def something():
    return jsonify({"message": "Not Implemented"}), 501  # Not Implemented


def main():
    if __name__ == "__main__":
        app.run(debug=False)
    else:
        print("\033[31m__name__ is \033[33m" + __name__ + "\033[0m")
        app.run(debug=True)


# if __name__ == "__main__":
#    app.run(debug=True)

with app.app_context():
    db.create_all()
    user = User.query.filter_by(username="todolistapi").first()
    print(user)
    my_jwt = create_jwt({"message": "hi"})
    print(jsonify(verify_jwt(my_jwt)))
