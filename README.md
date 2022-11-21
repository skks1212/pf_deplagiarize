# What does this do?

This is a plagiarism checker for pupilfirst's WD201 course.

# How do I run this?

Create a `.env` file in the root directory of this project. The file should contain the following:

```
SESSION_KEY=[your pupilfirst.school session key]
NAME=[your name]
```

How do you get the session key?
Login to LMS, and copy the value of the `_pupilfirst_session` cookie.

Install all dependencies, then run the `main.py` file and you should be good to go!

Note: This is not a very efficient way to do this, but it works. I'll probably make this better in the future.
