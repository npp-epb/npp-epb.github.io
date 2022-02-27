import os
from functools import wraps

from flask import Flask, make_response, render_template, request, abort, redirect
from gevent.pywsgi import WSGIServer

from src.util import *
from src.template_vars import *

pw = os.environ.get('password')
assert(pw)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

main_css = 'static/main.css'
__file__dirname = os.path.dirname(os.path.realpath(__file__))

def requires_password(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if request.cookies.get('pw') != pw:
            return redirect('/login')
        return route(*args, **kwargs)
    return wrapper


def is_safe_path(path: str) -> bool:
    return __file__dirname == os.path.commonprefix((__file__dirname, os.path.abspath(path)))


@app.route('/')
def index():
    return render_template('index.jinja', **globals())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.jinja')
    elif request.method == 'POST':
        password = request.form.get('pw')
        if password == pw:
            response = make_response(redirect('/files'))
            response.set_cookie('pw', pw)
            return response
    abort(400)


@app.route('/files', defaults={'subpath': '.'})
@app.route('/files/<path:subpath>')
@requires_password
def get_file(subpath: str):
    if not os.path.exists(subpath) or not is_safe_path(subpath):
        abort(400)
    if os.path.isfile(subpath):
        return {'text': open(subpath, encoding='utf-8').read()}
    files = os.listdir(subpath)
    return render_template('files.jinja', files=files, subpath=subpath, isfile=os.path.isfile)


@app.route('/edit')
def edit():
    return redirect('/files')


@app.route('/edit/<path:subpath>', methods=['GET', 'POST'])
@requires_password
def edit_file(subpath: str):
    if not is_safe_path(subpath):
        abort(400)
    if request.method == 'GET':
        if subpath.endswith('.py'):
            lang = 'python'
        else:
            lang = 'html'
        return render_template('edit.jinja', path=subpath, lang=lang)
    elif request.method == 'POST':
        text = request.form.get('text')
        if text:
            with open(subpath, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
        if subpath.endswith('.py'):
            return redirect(request.referrer or '/')
        if subpath.endswith('index.jinja'):
            return redirect('/')
        if subpath.endswith('edit.jinja'):
            return redirect('/edit/templates/edit.jinja')
        return redirect(f'/{subpath}'.removesuffix('.jinja'))
    abort(400)


if __name__ == '__main__':
    main_css = 'static/main.min.css'
    wsgi = WSGIServer(('0.0.0.0', int(os.environ.get('PORT'))), app)
    wsgi.serve_forever()
