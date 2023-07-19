from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, position


class Goal:
    DB = "Riff_Soccer_Academy"

    def __init__(self, data):
        self.id = data['id']
        self.player_goals = data['player_goals']
        self.user_id = data['user_id']

        self.owner = None

    @classmethod
    def get_all_goals(cls):
        query = "SELECT * FROM goals;"
        results = connectToMySQL(cls.DB).query_db(query)

        all_goals = []
        for one_goal in results:
            all_goals.append(cls(one_goal))
        return all_goals

    @classmethod
    def get_goals_with_user(cls):
        query = """
            SELECT * FROM goals
            JOIN users on goals.user_id = users.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        all_goals = []

        for row in results:
            one_goal = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'date_of_birth': row['date_of_birth'],
                'position_id': row['position_id']
            }

            one_goal.owner = user.User(user_data)
            all_goals.append(one_goal)
        return all_goals

    @classmethod
    def get_one_goal_with_owner(cls, data):
        query = """
            SELECT * FROM goals
            JOIN users on goals.user_id = users.id
            WHERE goals.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        one_goal = cls(results[0])

        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'date_of_birth': results[0]['date_of_birth'],
            'position_id': results[0]['position_id']
        }
        one_user = user.User(user_data)
        one_goal.owner = one_user

        return one_goal

    @classmethod
    def get_one_goal(cls, data):
        query = """
                SELECT * FROM goals WHERE id = %(id)s;
            """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def save_goal(cls, data):
        query = """
            INSERT INTO goals
            (player_goals,user_id)
            VALUES (%(player_goals)s,%(user_id)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def update_goal(cls, data):
        query = """
                UPDATE goals
                SET player_goals = %(player_goals)s
                WHERE id = %(id)s;
            """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_goal(cls, data):
        query = """
                DELETE FROM goals WHERE id = %(id)s;
            """
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_goal(goal):
        is_valid = True
        if len(goal['player_goals']) < 10:
            flash("Goals / Objectives must atleast be 10 characters long !!!", "goals")
            is_valid = False
        return is_valid
