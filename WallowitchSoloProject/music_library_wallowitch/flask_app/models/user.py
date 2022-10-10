from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re


NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "music_library_schema"
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True 
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) > 0:
            flash("This email is already in use!", "register")
            is_valid = False
        if len(user['username']) < 3:
            flash("Username must be at least 3 characters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must be the same!", "register")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s,  %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def search_user(cls,data):
        query = "SELECT * FROM users WHERE (id) = %(id)s;"
        results = connectToMySQL("music_library_schema").query_db(query, data)
        return cls(results[0])

    @classmethod
    def search_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('music_library_schema').query_db(query)
        songs = []
        for user in results:
            users.append( cls(user) )
        return users

