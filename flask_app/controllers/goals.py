from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, position, goal


@app.route('/delete/goal/<int:id>')
def delete_goal(id):
    data = {
        'id': id
    }
    goal.Goal.delete_goal(data)
    return redirect(request.referrer)


@app.route('/edit/goal/<int:id>')
def edit_goal(id):
    one_goal = goal.Goal.get_one_goal({"id": id})
    return render_template("edit_goal.html", one_goal=one_goal)


@app.route('/update/goal', methods=["POST"])
def update_goals():
    if not goal.Goal.validate_goal(request.form):
        return redirect(request.referrer)
    else:
        goal.Goal.update_goal(request.form)
    return redirect('/dashboard')
