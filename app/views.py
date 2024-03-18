from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PasswordUpdateForm
from app.models import User, ServerResourceUsage
from flask_login import current_user, login_user, logout_user, login_required
from app.graph_generation import generate_graphs


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        # Use the model's set_password method to update the password
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated.')
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Profile', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    # Call the function to generate graphs before rendering the template
    generate_graphs()
    # Retrieve the latest resource usage data from the database
    latest_data = ServerResourceUsage.query.order_by(ServerResourceUsage.timestamp.desc()).first()
    return render_template('dashboard.html', latest_data=latest_data)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied: Admins only.')
        return redirect(url_for('index'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


@app.route('/grant_admin/<int:user_id>', methods=['POST'])
@login_required
def grant_admin(user_id):
    if not current_user.is_admin:
        flash('Access denied: Admins only.')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
        flash(f'{user.username} has been granted admin status.')
    else:
        flash('User not found.')

    return redirect(url_for('admin_dashboard'))


