from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.song import Song
from flask_app.models.user import User
from flask_app.models.concert import Concert
from flask_app.config.mysqlconnection import connectToMySQL

@app.route('/songs/new')
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template("new_song.html", user=User.search_user(user_data))


@app.route('/songs/create', methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Song.validate_song(request.form):
        return redirect('/songs/new')
    song_data = {
            "name": request.form["name"],
            "composer": request.form["composer"],
            "arranger": request.form["arranger"],
            "type": request.form["type"],
            "number": int(request.form["number"]),
            "description": request.form["description"],
            "user_id": session["user_id"],
        }
    Song.save(song_data)
    return redirect("/dashboard") 

@app.route('/songs/<int:id>')
def show_song(id):
    if 'user_id' not in session:
        return redirect('/logout')
    song_data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_song.html",song=Song.get_one(song_data),user=User.search_user(user_data))

@app.route('/songs/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    song_data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_song.html",song=Song.get_one(song_data),user=User.search_user(user_data))

@app.route('/songs/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    song_data = {
            "name": request.form["name"],
            "composer": request.form["composer"],
            "arranger": request.form["arranger"],
            "type": request.form["type"],
            "number": int(request.form["number"]),
            "description": request.form["description"],
            "id": request.form["id"],
        }
    print("song_data", song_data)
    if not Song.validate_song(request.form):
        id = request.form['id']
        return redirect(f"/songs/edit/{id}")
    Song.update(song_data)
    return redirect("/dashboard") 

@app.route('/songs/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Song.delete(data)
    return redirect('/dashboard')
