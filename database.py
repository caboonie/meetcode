# -*- coding: utf-8 -*-
from models import *
import datetime
import random
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.mutable import Mutable
from werkzeug.security import generate_password_hash

engine = create_engine('sqlite:///codejam.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def create_team(team_name,password):
        newTeam = Team(name=team_name, points = 0, questions_status = {})
        newTeam.hash_password(password)
        session.add(newTeam)
        session.commit()

def remove_team(team_name):
    team = session.query(Team).filter_by(name=team_name).first();
    session.delete(team)
    session.commit()

def get_team_name(team_name):
    return session.query(Team).filter_by(name=team_name).first();

def get_teams():
    return session.query(Team).all();


#assume they have been verified with the team password
def create_user(user_name,team_name,group="student"):
    user = User(name = user_name,team_id=get_team_name(team_name).id,group=group)
    session.add(user)
    session.commit()

def create_admin():
    user = User(name = "admin",team_id="admins",group="admin")
    session.add(user)
    session.commit()

def get_user_team_name(team_name,user_name):
    for user in session.query(Team).filter_by(name=team_name).first().users:
        if user.name==user_name:
            return user
    return None

def get_admin_user():
    return session.query(User).filter_by(name="admin").first()

def create_question(name,question,answer,hint,points):
    question = Question(name = name,question=question,answer=answer,hint=hint,points=points)
    session.add(question)
    session.commit()

def get_question_id(id):
    return session.query(Question).filter_by(id=id).first();

def get_question_name(name):
    return session.query(Question).filter_by(name=name).first();

def get_questions():
    return session.query(Question).all()

def update_question(team_id,question_id,status):
    team = session.query(Team).filter_by(id=team_id).first()
    questions_status = dict(team.questions_status)
    questions_status[question_id] = status
    team.questions_status = questions_status
    #session.add(team)
    session.commit()


#create_admin()
#create_team("test","test")
#create_user("admin","doesn't matter")
#create_question("Lost in the Crypts","rw fqjc hnja fjb rjbj nbcjkurbqnm?","1990","mmm Caesar salad, my favorite Shift",2)
#create_question("Prime Time","If you take the time (hour and minute) on a digital clock to make a number, such as 3:14 -> 314, in a single day, how many primes would appear? Note, for times such as half-past noon, the clock shows 12:30, which would be 1230 as a number.","232","Every number happens twice in 24 hours.",10)
#create_question("Yaaaaaaas","How many times does the letter a appear in this: Y"+3*"aaaaaaaaaaaAAAAAAAAAAAAaaaAAaaAAAldkjfsAAAAAAAAAAAAaaaaaooooaaaaAAAAAAAAAAAAAAAAAAAaaaaaa",100,2)
#create_question("Fiba-what now?","MEET students have invented a new fibonacci sequence where you take the sum of the last three numbers in the sequence to get the next, and they call it the Fibano-she-didn't sequence. What are the last three digits of the 2019th Fibano-she-didn't number?",100,5)
#create_question("Ohmygodtherearesomanystairs","How many stairs are there?",213,50)
#logic puzzle mystery with IASA food
#

#print("team: ",[user.name for user in get_team_name("test").users])