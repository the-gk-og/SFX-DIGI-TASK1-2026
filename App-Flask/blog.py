import sqlite3
import os
import functools
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

blog = Blueprint('blog', __name__, url_prefix='/blog')

DB_PATH = os.path.join(os.path.dirname(__file__), 'blog.db')

BLOG_USERNAME = os.getenv('BLOG_USERNAME', 'admin')
BLOG_PASSWORD = os.getenv('BLOG_PASSWORD', 'admin')


# ── DB ───────────────────────────────────────────────────────────────────────

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            body    TEXT NOT NULL,
            created TEXT NOT NULL
        )
    ''')
    db.commit()
    db.close()


# ── Auth ─────────────────────────────────────────────────────────────────────

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('blog_logged_in'):
            return redirect(url_for('blog.login'))
        return f(*args, **kwargs)
    return decorated


# ── Public ───────────────────────────────────────────────────────────────────

@blog.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    db.close()
    return render_template('blog/index.html', posts=posts)


@blog.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    p = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    db.close()
    if not p:
        return redirect(url_for('blog.index'))
    return render_template('blog/post.html', post=p)


# ── Admin ────────────────────────────────────────────────────────────────────

@blog.route('/admin/login', methods=['GET', 'POST'])
def login():
    if session.get('blog_logged_in'):
        return redirect(url_for('blog.admin'))
    error = None
    if request.method == 'POST':
        if (request.form.get('username') == BLOG_USERNAME and
                request.form.get('password') == BLOG_PASSWORD):
            session['blog_logged_in'] = True
            return redirect(url_for('blog.admin'))
        error = 'Invalid credentials.'
    return render_template('blog/login.html', error=error)


@blog.route('/admin/logout')
def logout():
    session.pop('blog_logged_in', None)
    return redirect(url_for('blog.index'))


@blog.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    db = get_db()
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':
            title = request.form.get('title', '').strip()
            body  = request.form.get('body', '').strip()
            if title and body:
                db.execute(
                    'INSERT INTO posts (title, body, created) VALUES (?, ?, ?)',
                    (title, body, datetime.now().strftime('%d %b %Y'))
                )
                db.commit()
                flash('Post published!', 'success')
            else:
                flash('Title and body are required.', 'error')

        elif action == 'delete':
            post_id = request.form.get('post_id')
            if post_id:
                db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
                db.commit()
                flash('Post deleted.', 'success')

        db.close()
        return redirect(url_for('blog.admin'))

    posts = db.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    db.close()
    return render_template('blog/admin.html', posts=posts)