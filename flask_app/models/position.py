from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Position:
    DB = "Riff_Soccer_Academy"

    def __init__(self, data):
        self.id = data['id']
        self.position_name = data['position_name']

        self.user = []

    @classmethod
    def save_position(cls, data):
        query = """
            INSERT INTO positions
            (position_name) VALUES (%(position_name)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_positions(cls):
        query = """
            SELECT * FROM positions;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        all_positions = []
        for one_position in results:
            all_positions.append(cls(one_position))
        return all_positions

    @classmethod
    def get_one_position(cls, data):
        query = """
            SELECT * FROM positions
            WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_position_with_users(cls, data):
        query = """
            SELECT * FROM positions 
            JOIN users ON users.position_id = positions.id
            WHERE positions.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        one_position = cls(results[0])

        for user_data in results:
            user_data = {
                'id': user_data['users.id'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'date_of_birth': user_data['date_of_birth'],
                'position_id': user_data['position_id'],
                'password': user_data['password'],
            }
            one_user = user.User(user_data)
            one_position.user.append(one_user)
        return one_position

    # @classmethod
    # def get_position_with_owner(cls, data):

    @classmethod
    def update_position(cls, data):
        query = """
            UPDATE positions
            SET position_name = %(position_name)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_position(cls, data):
        query = """
            DELETE FROM positions WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_position(position):
        is_valid = True

        if len(position['position_name']) < 3:
            flash("Position must not be blank.")
            is_valid = False

        return is_valid
