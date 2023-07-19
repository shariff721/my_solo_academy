from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, position


@app.route('/positions')
def positions_dashboard():
    if "user_id" not in session:
        flash(" You must be logged in", "login")
        return redirect('/')
    else:
        all_positions = position.Position.get_all_positions()
    return render_template("positions_dashboard.html", all_positions=all_positions)


@app.route('/new/position', methods=["POST"])
def new_position():
    if not position.Position.validate_position(request.form):
        flash(" Positoin has to be atleat 3 characters", "position")
        return redirect(request.referrer)
    else:
        position.Position.save_position(request.form)
    return redirect('/positions')


@app.route('/one/position/<int:id>')
def show_one_position(id):
    if "user_id" not in session:
        flash(" You must be logged in", "login")
        return redirect('/')
    else:
        data = {
            'id': id
        }
        return render_template("one_position.html", one_position=position.Position.get_position_with_users(data))


@app.route('/delete/position/<int:id>')
def delete_position(id):
    data = {
        "id": id
    }
    position.Position.delete_position(data)
    return redirect('/positions')


@app.route('/edit/position/<int:id>')
def edit_position(id):
    if "user_id" not in session:
        flash(" You must be logged in", "login")
        return redirect('/')
    else:
        data = {
            "id": id
        }
        one_position = position.Position.get_one_position(data)
        return render_template("edit_position.html", one_position=one_position)


@app.route('/position/update', methods=["POST"])
def update_position_info():
    if not position.Position.validate_position(request.form):
        flash(" Positoin has to be atleat 3 characters", "position")
        return redirect(request.referrer)
    else:
        position.Position.update_position(request.form)
        return redirect('/positions')
