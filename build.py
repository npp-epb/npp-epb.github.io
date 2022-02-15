#!/usr/bin/env python3

if __name__ != '__main__':
    exit(1)

# Minify CSS
from src.util import *

main_min_css_path = 'static/main.min.css'
main_css_path = 'static/main.css'
main_min_css = minify_css(main_css_path)

if main_min_css:
    with open(main_min_css_path, "w") as f:
        f.write(main_min_css)

# Evaluate Template
from src.template_vars import *

from jinja2 import Environment, FileSystemLoader

main_css = main_min_css_path if main_min_css else main_css_path

env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
template = env.get_template("templates/index.jinja")
index_page = template.render(**globals())
with open('index.html', "w", encoding='utf-8') as f:
    f.write(index_page)
