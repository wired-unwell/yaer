# A to-do List API

A small app to learn API handling and creation in addiiton to SQLite3 in python, I guess.

The first goal is to implement [this todo-list-api](https://roadmap.sh/projects/todo-list-api).
I then **_might_** make this API work with something else as well, like my [TaskTracker](./../TaskTracker/ "tooltip").

Also, the code is [**blacked**](https://github.com/psf/black)!

# Notices

## Security

THIS API IS **NOT SECURE**! I KNOW THERE WILL BE A FEW VULNERABILITIES.
They would be fixed if I used proper third party libraries for
everything, but I decided to learn the basic concepts of those
by implementing them myself. Indeed, I'm mostly talking about
JWT and endpoint protection.

Also, at `protect_endpoint` (around `line 200`) there is a very important back-door-ish thing
that is a security nightmare and can easily bypass the whole JWT.
I used that because I don't like logging in during tests.

It is best practice to hash passwords client-side to further reduce any risk of snooping. (Implement later)

## License

This is a part of my learning project, released under GPL-3.0.
See [LICENSE](./../../LICENSE) in the root of the repository.

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
- Todo Class/Table -- basic `CRUD` done!
  - [x] `POST /todos`
  - [x] `GET /todos`
  - [x] `PUT /todos`
  - [x] `DELETE /todos`
- [x] Basic security and errors 
- [ ] Security Measures and 
- [ ] Error handling
- [x] Tokenization (expiration, randomness, etc)
- [ ] Data Validation (=input is OK?)
- [ ] Pagination and (Bonus)
- [ ] Filtering (Bonus)
- [ ] Unit tests (Bonus)
- [ ] Rate limiting requests/user (Self Bonus)
- [ ] Sign data by user. (Self bonus)
