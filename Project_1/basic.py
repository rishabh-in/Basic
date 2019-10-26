import os
from form import AddForm,DelForm,AddCourse
from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)

app.config["SECRET_KEY"]="mykey"

##############################################
########SQL_DATABASE#########
##############################################

basedir=os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
Migrate(app,db)

################################################
######## MODEL ############
################################################

class Student(db.Model):

    __tablename__= "student"

    id=db.Column(db.Integer,primary_key=True)

    name=db.Column(db.Text)

    ####One to One relation---->One Student One Course
    course=db.relationship("Course", backref="student", uselist=False)

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        if self.course:
            return f"Student Name: {self.name}  Course Name:{self.course.course_name}"
        else:
            return "Student Name: {}".format(self.name)

class Course(db.Model):

    __tablename__="Course"

    id=db.Column(db.Integer,primary_key=True)

    course_name=db.Column(db.Text)

    student_id=db.Column(db.Integer,db.ForeignKey("student.id"))

    def __init__(self,course_name,student_id):
        self.course_name=course_name
        self.student_id=student_id

    def __repr__(self):
        return f"Course Name: {self.course_name}"


###############################################
######## ADD VIEWS ###########
###############################################


@app.route("/")
def index():

    return render_template("home.html")

@app.route("/add",methods=["GET","POST"])
def add():

    form=AddForm()

    if form.validate_on_submit():
        name=form.name.data                   ## Getting name from the form.
        new_name = Student(name)            ## new_name is the object of the class.
        db.session.add(new_name)              ## We are adding new_name
        db.session.commit()

        return redirect(url_for("list"))

    return render_template("add.html",form=form)

@app.route("/list")
def list():

    students=Student.query.all()

    return render_template("pup_list.html",students=students)

@app.route("/del",methods=["GET","POST"])
def delete():

    form=DelForm()

    if form.validate_on_submit():

        id=form.id.data

        to_del=Student.query.get(id)
        db.session.delete(to_del)
        db.session.commit()

        return redirect(url_for("list"))

    return render_template("delete.html",form=form)

@app.route("/course",methods=["GET","POST"])
def course():

    form=AddCourse()

    if form.validate_on_submit():

        course_name=form.name.data
        stud_id=form.stud_id.data

        course = Course(course_name,stud_id)

        db.session.add(course)
        db.session.commit()

        return redirect(url_for("list"))

    return render_template("course.html",form=form)


