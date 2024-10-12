import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# function to get the database connection and interact with the rows
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# retrieves the post id
def get_post(post_id):
    conn = get_db_connection()
    # stores the selected post in the post variable
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    # if the post cannot be found, 404 error is shown
    if post is None:
        abort(404)
    return post

# initialize the site connection
@app.route('/')
def index():
    # run the db connection function 
    conn = get_db_connection()
    # fetch all the rows from the query result and return the list of posts
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return render_template('index.html', posts=posts)

# allow get and post requests. GET retrieves data from the server, POST posts data to a specific route
@app.route('/create/', methods=('GET', 'POST'))
def create():
    # extract title and content from form in create page
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        

        # flash error messages if title and content not inputted
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        elif not description:
            flash('Description is required!')
        # if title and content are inputted, database is connected and insert SQL commands are run
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, description, content) VALUES (?, ?, ?)',
                         (title, description, content))
            # commit and close database
            conn.commit()
            conn.close()
            # redirect user to index page where their new post will be displayed
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/about/', methods=('GET', 'POST'))
def about():
    return render_template('about.html')

# int: is a converter that accepts positive integers, id is the URL variable that will determine the post you want to edit
@app.route('/<int:id>/edit/', methods=('POST', 'GET'))
def edit(id):
    # fetches post with the associated id from the url
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        elif not description:
            flash('Description is required!')

        else:
            # connects to database and updates the post with the new title and/or content
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, description = ?, content = ?'
                         ' WHERE id = ?',
                         (title, description, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('{} was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/<int:id>/blogpost/', methods=('POST', 'GET'))
def post(id):

    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
    

    return render_template('blogpost.html', post=post)



        