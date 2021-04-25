from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from mychordsheets.auth import login_required
from mychordsheets.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    songs = db.execute(
        'SELECT s.id, title, author, body, created, creator_id, username'
        ' FROM song s JOIN user u ON s.creator_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html.jinja2', songs=songs)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO song (title, author, body, creator_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, author, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html.jinja2')

def get_song(id, check_author=True):
    song = get_db().execute(
        'SELECT s.id, title, author, body, created, creator_id, username'
        ' FROM song s JOIN user u ON s.creator_id = u.id'
        ' WHERE s.id = ?',
        (id,)
    ).fetchone()

    if song is None:
        abort(404, "Song id {0} doesn't exist.".format(id))

    if check_author and song['creator_id'] != g.user['id']:
        abort(403)

    return song

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    song = get_song(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE song SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html.jinja2', song=song)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
