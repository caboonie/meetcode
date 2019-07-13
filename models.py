from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, DateTime, Boolean,PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class Team(Base):
	#Users of the 'Student' group are part of a Team.  Each team will have points and a dictionary mapping questions to last submitted answer and penalties
	__tablename__ = 'teams'
	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	points = Column(Integer) #starts as 0
	questions_status = Column(PickleType) #dictionary mapping question ids to status dictionary: correct: True/False, last_submit: String, last_code: String
	password_hash = Column(String(255))
	def hash_password(self, password):
			self.password_hash = pwd_context.encrypt(password)
	def verify_password(self, password):
			return pwd_context.verify(password, self.password_hash)

class User(Base):
	#Everyone in the system is a type of user, Authorization of Student Users, Administrators will be specified in the 'group' field
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	group = Column(String(255))
	team_id = Column(Integer, ForeignKey(Team.id)) #values here must exist in the team column
	team = relationship("Team", back_populates = "users")

Team.users = relationship("User", order_by = User.id, back_populates = "team")

class Question(Base):
        __tablename__ = 'questions'
        id = Column(Integer, primary_key=True)
        name = Column(String(255))
        question = Column(String(255))
        hint = Column(String(255))
        points = Column(Integer)
        answer = Column(String(255))
