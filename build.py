from src.common import *

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
template = env.get_template("templates/index.jinja")
index_page = template.render(**globals())
with open('index.html', "w", encoding='utf-8') as f:
    f.write(index_page)
