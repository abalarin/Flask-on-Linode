from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from flask_app import app, db
from flask_app.models import User, Post
from flask_app.forms import PostForm

@app.route("/")
def index():
    db.create_all()
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("index.html")


# @app.route("/register", methods=['GET', 'POST'])
# def register():

#     if request.method == 'GET':
#         return render_template('register.html')

#     else:
#         # Create user object to insert into SQL
#         passwd1 = request.form.get('password1')
#         passwd2 = request.form.get('password2')

#         if passwd1 != passwd2 or passwd1 == None:
#             flash('Password Error!', 'danger')
#             return render_template('register.html')

#         hashed_pass = sha256_crypt.encrypt(str(passwd1))

#         new_user = User(
#             username=request.form.get('username'),
#             email=request.form.get('username'),
#             password=hashed_pass)

#         if user_exsists(new_user.username, new_user.email):
#             flash('User already exsists!', 'danger')
#             return render_template('register.html')
#         else:
#             # Insert new user into SQL
#             db.session.add(new_user)
#             db.session.commit()

#             login_user(new_user)

#             flash('Account created!', 'success')
#             return redirect(url_for('index'))


@app.route('/personal-login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(username=username).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)
            flash('Logged in!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Incorrect Login!', 'danger')
            return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))


# Check if username or email are already taken
def user_exsists(username, email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
