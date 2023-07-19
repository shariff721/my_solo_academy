from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import user, position, goal

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "Riff_Soccer_Academy"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.date_of_birth = data['date_of_birth']
        self.position_id = data['position_id']

        self.goals = []

    @classmethod
    def user_with_goals(cls, data):
        query = """
            SELECT * FROM users 
            JOIN goals on users.id = goals.user_id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        one_user = cls(results[0])

        for user_dict in results:
            user_dict = {
                "id": user_dict["goals.id"],
                "player_goals": user_dict["player_goals"],
                "user_id": user_dict["user_id"]
            }
            one_goal = goal.Goal(user_dict)
            one_user.goals.append(one_goal)
        return one_user

    @classmethod
    def save(cls, data):
        query = """ INSERT INTO users (first_name, last_name, email, password, date_of_birth, position_id)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(date_of_birth)s, %(position_id)s)"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def update_user(cls, data):
        query = """
            UPDATE users
            SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, date_of_birth = %(date_of_birth)s, position_id = %(position_id)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM users;"""
        results = connectToMySQL(cls.DB).query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def get_one_by_email(cls, data):
        query = """ SELECT * FROM users WHERE email = %(email)s """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def delete_user(cls, data):
        query = """
            DELETE FROM users WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_one_by_id(cls, data):
        query = """
            SELECT * FROM users WHERE id = %(id)s
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    def get_position_name(self):
        query = " SELECT position_name FROM positions WHERE id = %(position_id)s;"
        data = {"position_id": self.position_id}
        result = connectToMySQL(self.DB).query_db(query, data)
        return result[0]['position_name']

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.DB).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken", "register")
            is_valid = False

        if len(user['first_name']) < 3:
            flash("Name must be atleat 3 characters.", "register")
            is_valid = False

        if len(user['last_name']) < 3:
            flash("Name must be atleast 3 characters.", "register")
            is_valid = False

        if len(user['password']) < 1:
            flash("Invalid password!!!", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords Don't match", "register")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!!!", "register")
            is_valid = False
        return is_valid
