from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from secrets import SECRET_PASSWORD
from forms import UserForm, RegisterForm, FeedbackForm

app = Flask(__name__)

password = SECRET_PASSWORD


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///password_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def home_page():
    return redirect('/register')


@app.route('/secret', methods = ['GET', 'POST'])
def show_secret():
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/')
    form = FeedbackForm()
    all_feedback = Feedback.query.all()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=session['user_id'])
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback Accepted!')
        return redirect('/secret')
    return render_template('secret.html', form=form, feedback=all_feedback)

@app.route('/secret/<int:id>', methods=['POST'])
def delete_feedback(id):
    #Delete Tweet
    if 'user_id' not in session:
    	flash("Please login first")
    	return redirect('/login') 
    feedback = Feedback.query.get_or_404(id)
    if feedback.username == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback was deleted!")
        return redirect('/secret')
    flash("You don't have permission for that")
    return redirect('/secret')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form=RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.username
        flash('Welcome! Account Successfully Created!')
        return redirect('/secret')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form=UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!")
    return redirect('/')


