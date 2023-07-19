from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, position, goal
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    all_positions = position.Position.get_all_positions()
    return render_template("index.html", all_positions=all_positions)


@app.route('/register/user', methods=["POST"])
def add_entry():
    if not user.User.validate_user(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash,
            "date_of_birth": request.form["date_of_birth"],
            "position_id": request.form["position_id"]
        }
    user_id = user.User.save(data)
    session['user_id'] = user_id
    return redirect("/dashboard")


@app.route('/login', methods=["POST"])
def login():
    data = {"email": request.form["email"]}
    user_in_db = user.User.get_one_by_email(data)

    if not user_in_db:
        flash(" Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash(" Invalid Email/password", "login")
        return redirect('/')
    # ---> The lines below puts our logged in user(object of our class user) in session
    session['user_id'] = user_in_db.id
    session['name'] = user_in_db.first_name
    return redirect('/dashboard')


@app.route('/dashboard')
def user_dashboard():
    # This is to prevent non logged in users from acess to our app
    if "user_id" not in session:
        flash(" You must be logged in", "login")
        return redirect('/')
    logged_in_user = user.User.get_one_by_id({"id": int(session['user_id'])})
    all_players = user.User.get_all()
    all_goals = goal.Goal.get_goals_with_user()
    return render_template("dashboard.html", one_user=logged_in_user, all_players=all_players, all_goals=all_goals)


@app.route('/show/player/<int:id>')
def show_player(id):
    if "user_id" not in session:
        flash(" You must be logged in", "login")
        return redirect('/')
    else:
        data = {
            'id': id
        }
        one_user_with_goal = user.User.user_with_goals(data)
        return render_template("show_player.html", one_user_with_goal=one_user_with_goal)
        # one_user = user.User.get_one_by_id(data)
        # one_goal = goal.Goal.get_one_goal_with_owner(data)
        # return render_template("show_player.html", one_user=one_user, one_goal=one_goal)


@app.route('/edit/user/<int:id>')
def edit_user(id):
    if "user_id" not in session:
        flash(" You must be logged in", "login")
        return redirect('/')
    else:
        data = {
            "id": id
        }
        one_player = user.User.get_one_by_id(data)
        all_positions = position.Position.get_all_positions()
        return render_template("edit_player.html", one_player=one_player, all_positions=all_positions)


@app.route('/user/update', methods=["POST"])
def update_user_info():
    if not user.User.validate_user(request.form):
        return redirect(request.referrer)
    else:
        user.User.update_user(request.form)
    return redirect('/dashboard')


@app.route('/delete/player/<int:id>')
def delete_player_info(id):
    data = {
        "id": id
    }
    user.User.delete_user(data)
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    # session.pop('email', None) ---> Another way to clear user data from session
    return redirect('/')


@app.route('/save/goal', methods=["POST"])
def create_goal():
    if not goal.Goal.validate_goal(request.form):
        return redirect(request.referrer)
    else:
        data = {
            "player_goals": request.form["player_goals"],
            "user_id": session['user_id']
        }
        goal.Goal.save_goal(data)
        return redirect('/dashboard')
