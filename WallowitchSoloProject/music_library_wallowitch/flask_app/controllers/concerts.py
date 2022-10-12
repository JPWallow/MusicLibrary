from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.song import Song
from flask_app.models.user import User
from flask_app.models.concert import Concert
from flask_app.config.mysqlconnection import connectToMySQL

@app.route('/concerts/new')
def new_concert():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    songs = Song.join_get_all()
    return render_template("new_concert.html", user=User.search_user(user_data), songs=songs)

@app.route('/concerts')
def past_concerts():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    concerts = Concert.join_get_all()
    return render_template("concerts.html", user=User.search_user(data), concerts=concerts)

@app.route('/concerts/community')
def community():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id': session['user_id']
    }
    concerts = Concert.join_get_all()
    return render_template("community.html", user=User.search_user(data), concerts=concerts)

@app.route('/concerts/create', methods=['POST'])
def create_concert():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Concert.validate_concert(request.form):
        return redirect('/concerts/new')
    concert_data = {
            "ensemble": request.form["ensemble"],
            "date": request.form["date"],
            "song_one": request.form["song_one"],
            "song_two": request.form["song_two"],
            "song_three": request.form["song_three"],
            "song_four": request.form["song_four"],
            "description": request.form["description"],
            "user_id": session["user_id"],
        }
    Concert.save(concert_data)
    return redirect("/concerts") 

@app.route('/concerts/<int:id>')
def show_concert(id):
    if 'user_id' not in session:
        return redirect('/logout')
    concert_data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_concert.html",concert=Concert.get_one(concert_data),user=User.search_user(user_data))

@app.route('/concerts/edit/<int:id>')
def edit_concert(id):
    if 'user_id' not in session:
        return redirect('/logout')
    concert_data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    songs = Song.join_get_all()
    return render_template("edit_concert.html",concert=Concert.get_one(concert_data),user=User.search_user(user_data), songs=songs)

@app.route('/concerts/update', methods=['POST'])
def update_concert():
    if 'user_id' not in session:
        return redirect('/logout')
    concert_data = {
            "ensemble": request.form["ensemble"],
            "date": request.form["date"],
            "song_one": request.form["song_one"],
            "song_two": request.form["song_two"],
            "song_three": request.form["song_three"],
            "song_four": request.form["song_four"],
            "description": request.form["description"],
            "id": request.form["id"],
        }
    if not Concert.validate_concert(request.form):
        id = request.form['id']
        return redirect(f"/concerts/edit/{id}")
    Concert.update_concert(concert_data)
    return redirect("/concerts") 

@app.route('/concerts/delete/<int:id>')
def delete_concert(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Concert.delete_concert(data)
    return redirect('/concerts')
