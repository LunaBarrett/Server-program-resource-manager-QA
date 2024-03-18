from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, ServerResourceUsage
from flask_login import current_user, login_user, logout_user, login_required
import matplotlib.pyplot as plt
import os
from datetime import datetime


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


def generate_graphs():
    # Query the last N resource usage records from the database
    data_points = ServerResourceUsage.query.order_by(ServerResourceUsage.timestamp.desc()).limit(100).all()

    # Extract the data for each resource
    timestamps = [data.timestamp for data in data_points]
    cpu_usages = [data.cpu_usage for data in data_points]
    memory_usages = [data.memory_usage for data in data_points]
    disk_usages = [data.disk_usage for data in data_points]
    # ... other resources

    # Generate and save the Memory usage graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, memory_usages, label='Memory(RAM) Usage')
    plt.xlabel('Time')
    plt.ylabel('Memory Usage (%)')
    plt.title('Memory(RAM) Usage Over Time')
    plt.legend()
    plt.savefig(os.path.join(app.static_folder, 'images', 'memory_usage.png'))
    plt.close()

    # Generate and save the Disk usage graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, disk_usages, label='Disk Usage')
    plt.xlabel('Time')
    plt.ylabel('Disk Usage (%)')
    plt.title('Disk Usage Over Time')
    plt.legend()
    plt.savefig(os.path.join(app.static_folder, 'images', 'disk_usage.png'))
    plt.close()

    # Generate and save the CPU usage graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_usages, label='CPU Usage')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.legend()
    plt.savefig(os.path.join(app.static_folder, 'images', 'cpu_usage.png'))
    plt.close()

    # Generate and save graphs for other resources similarly...

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


