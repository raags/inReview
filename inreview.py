#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
inReview
~~~~~~

An application to rate and review companies with 
data from Linkedin.

:copyright: (c) 2012 by Raghu Udiyar.
:license: BSD, see LICENSE for more details.
"""
	
# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, jsonify
 
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///inreview.db'
DEBUG = True
SECRET_KEY = 'adevelopment key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)


# models 
users_table = db.Table('users_table', db.Model.metadata,
		    db.Column('company_id', db.Integer, db.ForeignKey('company.company_id'), primary_key=True),
			db.Column('user_id', db.String, db.ForeignKey('user.user_id'), primary_key=True)
		)

class Company(db.Model):
	company_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	reviews = db.relationship('Review', backref='company', lazy='dynamic')
#	user_id = db.column(db.String(80), db.ForeignKey('User.user_id'))
#	users = db.relationship('User', backref='companies', lazy='dynamic')
	users = db.relationship('User', secondary=users_table, lazy='dynamic', backref=db.backref('companies', lazy='dynamic'))
	
	def __init__(self, company_id, name):
		self.company_id = company_id
		self.name = name

	def __repr__(self):
		return '<Company %r>' % self.name
		
class User(db.Model):
	user_id = db.Column(db.String(80), primary_key=True)
#	company_id = db.Column(db.Integer, db.ForeignKey('Company.company_id'))
		
	def __init__(self, user_id):
		self.user_id = user_id

	def __repr__(self):
		return '<User %r>' % self.user_id
		
class Review(db.Model):
	title = db.Column(db.String(150))
	review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	company_id = db.Column(db.Integer, db.ForeignKey('company.company_id') )
	rate_career = db.Column(db.Integer)
	rate_comp = db.Column(db.Integer)
	rate_worklife = db.Column(db.Integer)
	rate_manage = db.Column(db.Integer)
	rate_culture = db.Column(db.Integer)
	recommend_radio = db.Column(db.Boolean)
	pros = db.Column(db.String(80))
	cons = db.Column(db.String(80))
	
	def __init__(self, title, company_id, rate_career, rate_comp, rate_worklife, rate_manage, rate_culture, recommend_radio, pros, cons):
		self.title = title
		self.company_id = company_id
		self.rate_career = rate_career
		self.rate_comp = rate_comp
		self.rate_worklife = rate_worklife
		self.rate_manage = rate_manage
		self.rate_culture = rate_culture
		self.recommend_radio = recommend_radio
		self.pros = pros
		self.cons = cons

	def __repr__(self):
		return '<Review %r>' % self.review_id


# helper functions

# views

@app.route("/")
def main():
    return render_template("layout.html")

@app.route("/review")
def get_review():
	return render_template("review.html", has_reviewed = False)
	
@app.route("/right")
def get_review():
	return render_template("right.html")
	
@app.route("/has_reviewed", methods=['GET'])
def has_reviewed(comp_id="", user_id=""):
	if comp_id or user_id:
		company_id = comp_id
		user_id = user_id
	else:
		company_id = request.args.get('cid', '')
		user_id = request.args.get('uid', '')
		
	company = Company.query.get(company_id)
	if not company:
		response = {'response': False}
	else:
		user = company.users.filter(User.user_id==user_id).all()
		if not user:
			response = {'response':False}
		else:
			response = {'response':True}
		
	return jsonify(response)
	
@app.route("/submit", methods=['POST'])
def submit_review():
	
	company = Company.query.get(request.form['company-id'])
	if not company:
		company = Company(request.form['company-id'], request.form['company-name'])
	
	user =  User.query.get(request.form['user-id'])
	if not user:
		user = User(request.form['user-id'])
	
	# Add check to determine if user is already present	
	company.users.append(user)
	
	if request.form['recommend-radio'] == "yes":
		recommend = True
	else:
		recommend = False
		
	review = Review(request.form['title'], request.form['company-id'], request.form['rate-career'], request.form['rate-comp'], request.form['rate-worklife'], 
					request.form['rate-manage'], request.form['rate-culture'], recommend, request.form['pros'], 
					request.form['cons'])
	
	company.reviews.append(review)
	
	db.session.add(company)
	db.session.commit()
	
	return show_review(reviewed=True, comp_id=request.form['company-id'])
	
@app.route("/show", methods=['GET'])
def show_review(reviewed=False, comp_id=""):
	
	if comp_id:
		company_id = comp_id
	else:
		company_id = request.args.get('id', '')
	
	reviews = Review.query.filter_by(company_id=company_id).all()
	company = reviews[0].company
	return render_template('show_review.html', reviews=reviews, company=company, has_reviewed=reviewed)
	
# For testing
@app.route("/Test")
def add_review():

	return render_template('Test.html')
	

if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)









# vim: ts=4 sw=4 et
