# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, url_for, redirect, send_from_directory, jsonify, current_app, Markup, make_response, send_file
from database import *
import random
from flask import session as login_session
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
 
   
#start_date = datetime("8-3-2019-18:00:00")
#end_date = datetime("8-3-2019-20:00:00")


@app.route('/')
def home():
	team = None
	if 'id' in login_session and login_session["group"]=="student":
		team = get_team_name(login_session["team"])
	return render_template('home.html', team = team, start=True, teams = sorted(get_teams(),key=lambda x:-x.points))

    

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'id' in login_session:
		return redirect(url_for("viewQuestions"))
	if request.method == 'GET':
		return render_template('login.html')
	else:
		if(request.form["user name"]=="admin"):
			if request.form['password']=="adminmeet":
				user = get_admin_user()
				login_session["id"] = user.id
				login_session["group"] = user.group
				return dashboard()
			else:
				flash("invalid username")
				return render_template("login.html")
		team = get_team_name(request.form['team name'])
		if team==None:
			flash("invalid login")
			return render_template("login.html")
		if team.verify_password(request.form['password']):
			user = get_user_team_name(team.name,request.form["user name"]) 
			if user == None:
				create_user(request.form["user name"],team.name)
				user = get_user_team_name(team.name,request.form["user name"]) 


			login_session["id"] = user.id
			login_session["team"] = team.name
			login_session["group"] = user.group
			flash("Welcome "+user.name)
			return home()
		else:
			flash("invalid login")
			return render_template("login.html")




@app.route('/logout')
def logout():
	login_session.clear()
	return home()


#there will be a bonus question only accessible by manually editing the route--

def checkLoggedIn():
	if 'id' not in login_session:
		flash("You must login to view that page.")
		return home()

def checkAdmin():
	if 'id' not in login_session:
		flash("You must login to view that page.")
		return home()
	if login_session['group'] != "admin":
		flash("You must be an admin to view that page.")
		return home()

@app.route("/viewQuestions")
def viewQuestions():
	checkLoggedIn()
	print(login_session)
	
	if login_session["group"]=="admin":
		team = None
	else:
		team = get_team_name(login_session["team"])
	return render_template("questions.html", questions = get_questions(), team = team)

@app.route("/viewQuestion/<int:id>")
def viewQuestion(id):
	checkLoggedIn()
	if login_session["group"]=="admin":
		team = None
	else:
		team = get_team_name(login_session["team"])
	return render_template("question.html", question = get_question_id(id), team = team)

@app.route("/answerQuestion/<int:id>",methods=['POST'])
def answerQuestion(id):
	checkLoggedIn()
	question = get_question_id(id)
	team = get_team_name(login_session["team"])
	if(id not in team.questions_status or not team.questions_status[id]["correct"]):
		status = {"correct":(request.form["answer"]==question.answer),"last_submit":request.form["answer"],"last_code":request.form["code"]}
		update_question(team.id,id,status)
		if status["correct"]:
			flash("Correct!")
			team.points += question.points
		else:
			flash("Incorrect.")
	else:
		flash("You've already answered this question correctly.")
	return redirect(request.referrer)

@app.route("/teamInfo")
def teamInfo():
	checkLoggedIn()
	return home()

@app.route("/dashboard")
def dashboard():
	checkAdmin()
	return render_template("dashboard.html", teams = get_teams(), questions = get_questions())

@app.route("/makeTeam",methods=['POST'])
def makeTeam():
	checkAdmin()
	if(get_team_name(request.form['team name'])==None):
			create_team(request.form['team name'],request.form['password'])
	return redirect(request.referrer)

@app.route("/removeTeam",methods=['POST'])
def removeTeam():
	checkAdmin()
	if(get_team_name(request.form['team name'])!=None):
			remove_team(request.form['team name'])
	return redirect(request.referrer)

@app.route("/makeQuestion",methods=['POST'])
def makeQuestion():
	checkAdmin()
	return redirect(request.referrer)

@app.route("/editQuestion",methods=['POST'])
def editQuestion():
	checkAdmin()
	return redirect(request.referrer)

@app.route("/removeQuestion",methods=['POST'])
def removeQuestion():
	checkAdmin()
	return redirect(request.referrer)

if __name__ == '__main__':
	app.run(debug=True,host= '0.0.0.0')
