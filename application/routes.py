from application import app, db
from flask import render_template, request, Response, json, jsonify, redirect, flash, url_for, session
from .models import User, Course, Enrollment
from .forms import LoginForm, RegisterForm
from .course_list import course_list
#from flask_restplus import Resource

courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, 
                  {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, 
                  {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, 
                  {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, 
                  {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]
#print(courseData)
##################################################################################################
'''
@api.route('/api', '/api/')
class GetAndPost(Resource):
    
    def get(self):
        return jsonify(user.objects.all())

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    
    def get(self, idx):
        return jsonify(user.objects(user_id=idx))
'''
    



################################################################################################################

#decorators
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Spring 2019"
    
    classes = Course.objects.order_by("-courseID")
    
    return render_template("courses.html", courseData=classes, courses=True, term=term)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit() == True:
        email = form.email.data
        password = form.password.data
        #check the email supply if it matches what's in the database
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            #enable session immediately after logging
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html",title="Login", form=form, login=True)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session['user_id'] = False
    session.pop('username', None)
    
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id +=1
        
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        user = User(user_id=user_id, first_name=first_name, last_name=last_name,
                    email=email)
        user.set_password(password)
        user.save()
        flash("You are successfully registered! ", "success")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form, register=True)



@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')
    
    if courseID:
        if Enrollment.objects(user_id=user_id,courseID=courseID):
            flash(f"Oops! you are already registered in this course {courseTitle}", "danger")
            return redirect(url_for("courses"))
        
        else:
            Enrollment(user_id=user_id,courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success") 
            
    classes = course_list(user_id)
    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, title = "enrollment", classes = classes) 







#@app.route('/api/')
#@app.route('/api/<idx>')
#def api(idx=None):
#    if idx==None:
#        jdata = courseData
#   else:
#        jdata = courseData[int(idx)]
    
#   return Response(json.dumps(jdata), mimetype="application/json")

@app.route("/user")
def user():
    #User(user_id=1, first_name="Debby", last_name="Opawale", email="Debbybola5@gmail.com", password="abc1234").save()
    #User(user_id=2, first_name="Sam", last_name="Opa", email="bsamuel243@gmail.com", password="password123").save()
    users = User.objects.all()
    return render_template('user.html', users=users)