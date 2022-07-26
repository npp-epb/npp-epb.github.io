#!/usr/bin/env python3

if __name__ != '__main__':
    exit(1)

# Minify CSS
from src.util import *

def minify(css_path: str, min_css_path: str) -> None:
    min_css = minify_css(css_path)
    if min_css:
        with open(min_css_path, "w") as f:
            f.write(min_css)

minify('static/main.css', 'static/main.min.css')
minify('static/fixed_footer.css', 'static/fixed_footer.min.css')

# Evaluate Template
from src.template_vars import *

from jinja2 import Environment, FileSystemLoader

def build_page(name: str) -> None:
    template = env.get_template(f'{name}.jinja')
    page = template.render(**globals())
    with open(f'{name}.html', "w", encoding='utf-8') as f:
        f.write(page)

main_css = 'static/main.min.css'
fixed_footer_css = 'static/fixed_footer.min.css'

env = Environment(loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True)

build_page("index")
build_page("solutions")
build_page("legal")
build_page("about")
build_page("products")
