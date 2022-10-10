from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Concert:
    db = "music_library_schema"
    def __init__(self,data):
        self.id = data['id']
        self.date = data['date']
        self.song_one = data['song_one']
        self.song_two = data['song_two']
        self.song_three = data['song_three']
        self.song_four = data['song_four']
        self.description = data['description']
        self.ensemble = data['ensemble']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @staticmethod
    def validate_concert(concert):
        is_valid = True 
        if len(concert['ensemble']) < 2:
            flash("Must include the name of the ensemble.", "create")
            is_valid = False
        if len(concert['date'])<8:
            flash("Must include a date", "create")
            is_valid = False
        if len(concert['song_one']) < 2:
            flash("Must include at least one song.", "create")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM concerts;"
        results = connectToMySQL('music_library_schema').query_db(query)
        concerts = []
        for concert in results:
            concerts.append( cls(concert) )
        return concert
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM concerts WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO concerts (date, song_one, song_two, song_three, song_four, description, ensemble, user_id) VALUES (%(date)s, %(song_one)s, %(song_two)s, %(song_three)s, %(song_four)s, %(description)s, %(ensemble)s , %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update_concert(cls, data):
        query = "UPDATE concerts SET date = %(date)s, song_one = %(song_one)s, song_two = %(song_two)s, song_three = %(song_three)s, song_four = %(song_four)s, description = %(description)s, ensemble = %(ensemble)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_concert(cls,data):
        query  = "DELETE FROM concerts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)        
    
    @classmethod
    def join_get_all( cls ):
        query = "SELECT * FROM concerts JOIN users on concerts.user_id = users.id;"
        results = connectToMySQL('music_library_schema').query_db(query)
        concerts = []
        for concert in results:
            concerts.append( cls(concert))
        return concerts

