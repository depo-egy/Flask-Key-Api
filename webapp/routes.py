'''

Here we have the routes

'''

import os
import secrets
#from PIL import Image
import cv2
import numpy as np
import time

from flask import render_template, url_for, flash, redirect, request
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm , Take_VideoForm , Search_UserForm
from webapp.databases import User
from flask_login import login_user, current_user, logout_user, login_required

user1 = ''

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    db.create_all()
    def Key_api_generator():
        key_api = secrets.token_hex(16).encode('utf-8')
        return key_api
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password , key_api = Key_api_generator())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in! An Account KEY  is sent to your email', 'success')
        path = 'webapp/trained_img/'+user.username
        os.mkdir(path)
        user1 = user.username

        return redirect(url_for('login') )
    return render_template('register.html', title='Register', form=form )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/take_video/<user1>" , methods=['GET', 'POST'] )
@login_required
def take_video(user1):
    form = Take_VideoForm()
    if form.validate_on_submit():
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(user1+'.avi',fourcc, 20.0, (640,480))
        t0 = time.clock()
        while(cap.isOpened()):
            ret, frame = cap.read()

            if ret==True:
                out.write(frame)
                #cv2.imshow('frame',frame)
                if cv2.waitKey(1)& int(time.clock() - t0) == 10:# & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        #video parse
        vidcap = cv2.VideoCapture(user1+'.avi')
        success,image = vidcap.read()
        count = 0
        success = True
        os.chdir('webapp/trained_img/'+user1)
        while success:
            cv2.imwrite("%d.jpg" % count, image)     # save frame as JPEG file
            success,image = vidcap.read()
            print('Read a new frame:' , success)
            count += 1
        #initialize stage
        os.chdir(app.root_path)
        from webapp.main import  Initialize
        dir_pre = os.path.join('webapp/pre_img/',user1)
        #os.chdir('webapp/trained_img')
        initialize = Initialize()
        if len(os.listdir(dir_pre))!=0:
            from webapp.main import  Train
            train = Train()
    return render_template('take_video.html' ,title = 'Taking video' ,form = form , cap = cv2.VideoCapture(0))

@app.route("/search_user" , methods=['GET', 'POST'] )
#@login_required
def search_user():

    form = Search_UserForm()
    if form.validate_on_submit():
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        cv2.imwrite('test'+'.png', image)
        del(camera)
    #test img
    from webapp.main_test import Test
    try:
        os.chdir('webapp')
    except:
        pass
    try:
        test = Test()
    except:
        pass
    return render_template('search_user.html' , form=form)


@app.route("/account", methods=['GET', 'POST'])
#@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
