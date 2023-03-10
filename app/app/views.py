from pathlib import Path

import markdown

from flask import render_template, abort, url_for
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension

from app import flask_app


@flask_app.route('/')
def about():
    return render_template("about.html", active_page="about")


@flask_app.route('/software')
def software():
    return render_template('software.html', active_page="software")


@flask_app.route('/publications')
def publications():
    return render_template('publications.html', active_page="publications")


@flask_app.route('/blog')
def blog_listing():
    return render_template('blog_listing.html', active_page="blog_listing")


@flask_app.route('/blog/<string:name>')
def blog_item(name):

    blog_dir = Path(flask_app.root_path) / '..' / 'blog'
    item = [item for item in blog_dir.iterdir() if item.stem == name]

    if not item:
        abort(404)
    else:
        item = item[0]

    with open(item) as fh:
        md = fh.read()
        html = markdown.markdown(
            md,
            extensions=[
                FencedCodeExtension(),
                CodeHiliteExtension(noclasses=True, pygments_style='solarized-dark')
            ],
        )

    return render_template('blog.html', blog=html, active_page="blog_listing")


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
