from pathlib import Path

import markdown

from flask import render_template
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension

from app import flask_app


@flask_app.route('/')
def about():
    return render_template("about.html")


@flask_app.route('/software')
def software():
    return render_template('software.html')


@flask_app.route('/publications')
def publications():
    return render_template('publications.html')


@flask_app.route('/blog')
def blog_listing():

    blogs = []
    blog_dir = Path(flask_app.root_path) / '..' / 'blog'
    for item in blog_dir.iterdir():
        with open(item) as fh:
            md = fh.read()
            html = markdown.markdown(
                md,
                extensions=[
                    FencedCodeExtension(),
                    CodeHiliteExtension(noclasses=True, pygments_style='solarized-dark')
                ],
            )
            blogs.append(html)

    blogs = blogs

    return render_template('blog.html', blogs=blogs)


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
