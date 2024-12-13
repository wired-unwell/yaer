# A to-do List API

A small app to learn API handling and creation in addiiton to SQLite3 in python, I guess.

The first goal is to implement [this todo-list-api](https://roadmap.sh/projects/todo-list-api).
I then **_might_** make this API work with something else as well, like my [TaskTracker](./../TaskTracker/ "tooltip").

Also, the code is [**blacked**](https://github.com/psf/black)!

# Some AI Transparency

So, I've tried my best to avoid AI generated code in this small project. 
However, my code will be definitely influenced by the snippets I've read from GPT-4o.
There were some parts that are ~~almost~~ the exact same thing,
even though I tried my best to change them. See `create_jwt` as an example.

Moreover, 
I heavily used it to learn the next steps and the methodology of implementing my code,
as well as extensive use for tracking project progress.

This is very important to keep track of.

# Progress Overview

- [x] Hand-made JWT Create/Validate
- [x] Database: SQLite3
- User Class/Table
  - [x] `POST /register`
  - [x] `POST /login`
  - Login is very insecure at the moment.
- [x] Basic authentication function to protect endpoints
- [ ] Proper:
  - [ ] tokenization (expiration, randomness, etc)
  - [ ] data validation (sign data by user)
- Todo Class/Table -- basic `CRUD` done!
  - [x] `POST /todos`
  - [x] `GET /todos`
	- [ ] Pagination and filtering
  - [x] `PUT /todos`
  - [x] `DELETE /todos`
- [x] Basic security and errors 
- [ ] Check security measures and errors 
