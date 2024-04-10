from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PasswordUpdateForm
from app.models import User, ServerResourceUsage
from flask_login import current_user, login_user, logout_user, login_required
from scripts.graph_generation import generate_graphs


# Creates the function index point the user to the index page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')


# Creates the function register to allow users to register a new account and points the user to the register page
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


# Creates the function login to allow users to register a new account and points the user to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)


# Creates the function dashboard point the user to the dashboard page
@app.route('/dashboard')
@login_required
def dashboard():
    # Call the function to generate graphs before rendering the template
    generate_graphs()
    # Retrieve the latest resource usage data from the database
    latest_data = ServerResourceUsage.query.order_by(ServerResourceUsage.timestamp.desc()).first()
    return render_template('dashboard.html', latest_data=latest_data)


# Creates the function admin_dashboard point an Admin user to the admin dashboard page
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied: Admins only.')
        return redirect(url_for('index'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


# Creates the function grant_admin to allow admin users to assign other users admin status
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


# Creates the function delete_account to allow admin users to delete other users accounts
@app.route('/delete_account/<int:user_id>', methods=['POST'])
@login_required
def delete_account(user_id):
    if not current_user.is_admin:
        flash('Access denied: Admins only.')
        return redirect(url_for('index'))

    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f'Account {user_to_delete.username} has been deleted.')
    else:
        flash('User not found.')

    return redirect(url_for('admin_dashboard'))


# Creates the function profile that points the user to their profile page that shows all their details
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        # Use the model's set_password method to update the password
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated.')
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Profile', form=form)


# Creates the function delete_own_account, which allows users to delete their own account
@app.route('/delete_own_account', methods=['POST'])
@login_required
def delete_own_account():
    user_id = current_user.id
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        logout_user()  # Log the user out after deleting the account
        flash('Your account has been successfully deleted.')
        return redirect(url_for('index'))
    else:
        flash('Account not found.')
        return redirect(url_for('profile'))


# Creates the function logout to allow users to logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



