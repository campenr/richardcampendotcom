from pathlib import Path

from flask import render_template, abort, url_for

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension

from app import flask_app, sitemap


def load_content(name: str):
    file = Path(f'{name}.md')
    try:
        return load_markdown_file(file)
    except FileNotFoundError:
        abort(404)


def load_markdown_file(file: Path):
    item = Path(flask_app.root_path) / '..' / 'content' / file
    with open(item) as fh:
        md = fh.read()
        html = markdown.markdown(
            md,
            extensions=[
                FencedCodeExtension(),
                CodeHiliteExtension(noclasses=True, pygments_style='solarized-dark')
            ],
        )
    return html


@flask_app.route('/')
def about():
    html = load_content('about')
    return render_template("about.html", about=html, active_page="about")


@flask_app.route('/software')
def software():
    return render_template('software.html', active_page="software")


@flask_app.route('/publications')
def publications():
    return render_template('publications.html', active_page="publications")


def _get_blog_items():
    blog_dir = Path(flask_app.root_path) / '..' / 'content' / 'blog'
    items = [item for item in blog_dir.iterdir()]
    return items


blog_items = _get_blog_items()


@sitemap.register_generator
def blog_listing_sitemap():
    for item in blog_items:
        yield 'blog_item', {'name': item.stem}


@flask_app.route('/blog')
def blog_listing():
    return render_template('blog_listing.html', active_page="blog_listing")


@flask_app.route('/blog/<string:name>')
def blog_item(name):
    html = load_content(f'blog/{name}')
    return render_template('blog.html', blog=html, active_page="blog_listing")


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
