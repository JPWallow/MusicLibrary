from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Song:
    db = "music_library_schema"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.composer = data['composer']
        self.arranger = data['arranger']
        self.type = data['type']
        self.number = data['number']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @staticmethod
    def validate_song(song):
        is_valid = True 

        if int(song['number']) < 1:
            flash("Number of copies must be greater than 0.", "create")
            is_valid = False
        if len(song['name']) < 2:
            flash("Must include song title.", "create")
            is_valid = False
        if len(song['composer']) < 2:
            flash("Must include composer.", "create")
            is_valid = False
        if len(song['arranger']) < 2:
            flash("Must include arranger.", "create")
            is_valid = False
        if len(song['type']) < 2:
            flash("Must include type of ensemble.", "create")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM songs;"
        results = connectToMySQL('music_library_schema').query_db(query)
        songs = []
        for song in results:
            songs.append( cls(song) )
        return songs
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM songs WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO songs (name, composer, arranger, type, number, description, user_id) VALUES (%(name)s, %(composer)s, %(arranger)s, %(type)s, %(number)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE songs SET name = %(name)s, composer = %(composer)s, arranger = %(arranger)s, type = %(type)s, number = %(number)s, description = %(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM songs WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)        
    
    @classmethod
    def join_get_all( cls ):
        query = "SELECT * FROM songs JOIN users on songs.user_id = users.id;"
        results = connectToMySQL('music_library_schema').query_db(query)
        songs = []
        for song in results:
            songs.append( cls(song))
        return songs

