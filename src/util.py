from typing import Tuple

def extract_name_and_ext(filename: str) -> Tuple[str, str]:
    ext = ''
    for char in filename[::-1]:
        if char == '.':
            if not ext:
                break
            return filename[:-len(ext)-1], ext[::-1]
        ext += char
    return filename, ''

def minify_css(css_path: str) -> str:
    css = open(css_path).read()
    css_len = len(css)
    min_css = ''
    inside_comment = False
    inside_block = False
    i = 0
    try:
        while i < css_len:

            def backslash_n(c: str) -> bool:
                return c == '\n'

            def space(c: str) -> bool:
                return c == ' '

            def backslash_n_or_space(c: str) -> bool:
                return backslash_n(c) or space(c)

            cur_char = css[i]

            if backslash_n(cur_char):
                i += 1
                continue

            if inside_block and space(cur_char):
                i += 1
                continue

            if cur_char == '{' or cur_char == '}':
                inside_block = cur_char == '{'
                min_css += cur_char
                i += 1
                while i < css_len and backslash_n_or_space(css[i]):
                    i += 1
                continue

            if cur_char == '@':
                while i < css_len and css[i] != '{':
                    if not backslash_n(css[i]):
                        min_css += css[i]
                    i += 1
                inside_block = False
                min_css += css[i]
                i += 1
                while i < css_len and backslash_n_or_space(css[i]):
                    i += 1
                continue

            if i + 1 == css_len:
                min_css += cur_char
                break

            next_char = css[i+1]

            if not inside_block and cur_char == ' ' and next_char == '{':
                inside_block = True
                min_css += '{'
                i += 2
                continue

            if cur_char == '/' and next_char == '*':
                inside_comment = True
                i += 2
                continue

            if cur_char == '*' and next_char == '/':
                inside_comment = False
                i += 2
                while i < css_len and backslash_n_or_space(css[i]):
                    i += 1
                continue

            if inside_comment:
                i += 1
                continue

            if inside_block and cur_char == ':' and next_char == ' ':
                min_css += cur_char
                i += 2
                while i < css_len and css[i] != ';' and css[i] != '}':
                    if not backslash_n(css[i]):
                        min_css += css[i]
                    i += 1
                if css[i] == '}':
                    inside_block = False
                min_css += css[i]
                i += 1
                continue

            min_css += cur_char
            i += 1
    except Exception as e:
        min_css = ''
        print(f'Exception while minifying css: {e}', e)
    finally:
        return min_css
