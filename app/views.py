"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os.path
import hashlib
import uuid
import time
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, json
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignUpForm
from models import UserProfile
from werkzeug.utils import secure_filename


def upload(file,userid):
    file_folder = app.config['UPLOAD_FOLDER']
    filename = secure_filename(file.filename)
    file.save(os.path.join(file_folder, filename))
    ext = os.path.splitext(file_folder+filename)[1]
    os.rename(file_folder+"/"+filename, file_folder+"/"+userid+ext)

def search(userid):
    rootdir = app.config['UPLOAD_FOLDER']
    for subdir, dirs, files in os.walk(rootdir):
        for name in files:
            if str(userid) in name:
                 return name
    return None
   
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html',active='home')
    
@app.route('/profile', methods=["GET","POST"])
def profile():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            """Get data from form"""
            uid = int(uuid.uuid4().int & (1<<16)-1)
            fname = form.firstname.data
            lname = form.lastname.data
            uname = form.username.data
            age = form.age.data
            bio = form.biography.data
            gender = form.gender.data
            file = form.profilePic.data 
            
            """Save data to database"""
            user = UserProfile(id=uid,first_name=fname,last_name=lname,username=uname,age=age,gender=gender,bio=bio)
            db.session.add(user)
            db.session.commit()
                
            """upload profile picture"""
            upload(file,str(uid))
           
            flash("Profile created")
            return redirect(url_for("userprofile",userid=uid,active='profiles'))
        else:
            flash_errors(form)
            return redirect(url_for("profile",active='profile'))
        
    return render_template("profile.html", form=form, active='profile')
    
@app.route("/profiles", methods=["GET","POST"])
def profiles():
    users = UserProfile.query.all()
    if request.method == "GET":
        for u in users:
            u.image = search(u.id)
            u.idstring = str(u.id)
        return render_template("profiles.html",users=users, active='profiles')
    elif request.method == "POST":
        out = []
        if  "application/json" in request.headers['CONTENT-TYPE']:
            for u in users:
                user = {"userid":u.id,"username":u.username}
                out.append(user)
            return json.jsonify(out)
    

@app.route("/profile/<userid>", methods=["GET","POST"])
def userprofile(userid):
    
    user = UserProfile.query.get(userid)
    img = search(userid)
    if request.method == "GET":
        return render_template("user.html",user=user,img=img, active='profiles')
        
    elif request.method == "POST":
        if  "application/json" in request.headers['CONTENT-TYPE']:
            return json.jsonify(userid=user.id, username=user.username, image=img, gender=user.gender, age= user.age, profile_created_on=user.created_on)
        
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("home"))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
