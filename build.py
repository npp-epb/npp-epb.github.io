from unittest import loader
if __name__ != '__main__':
    exit(1)

from typing import Tuple

from jinja2 import Environment, FileSystemLoader

def extract_name_and_ext(filename: str) -> Tuple[str, str]:
    ext = ''
    for char in filename[::-1]:
        if char == '.':
            if not ext:
                break
            ext = ext[::-1]
            return filename[:-len(ext)-1], ext
        ext += char
    return filename, ''

jinja_env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)

licenses = {
    "2013-06-13-lic-fsb-crypto.jpg" : "Лицензия ФСБ России № 12947 H от 13 июня 2013 г.",
    "lic tzki.jpg"                  : "Лицензия ФСТЭК №2061 от 12 августа 2013 г. на деятельность по технической защите конфиденциальной информации",
    "lic-fstec-sczi.jpg"            : "Лицензия ФСТЭК №1783 от 18 июля 2017 г. на деятельность по разработке и производству средств защиты конфиденциальной информации",
    "gostaina.jpg"                  : "Лицензия УФСБ России №32358 от 19 октября 2018 г. на осуществление работ, связанных с использованием сведений, составляющих государственную тайну.",
    "attestat acreditacii fstek.jpg": "Аттестат аккредитации органа по аккредитации № СЗИ RU.3505.B013.666 от 13 февраля 2019",
    "lic_fstec_gt.jpg"              : "Лицензия ФСТЭК России №3505 от 18 января 2019 г. на осуществление мероприятий и (или) оказание услуг в области защиты государственной тайны (в части технической защиты информации).",
    "lic-fstec-szi.jpg"             : "Лицензия ФСТЭК России №3506 от 18 января 2019 г. на проведение работ, связанных с созданием средств защиты информации.",
    "ISO 9001-2015 1.jpg"           : "Сертификат соответствия ГОСТ ISO 9001-2015.",
    "ISO 9001-2015 2.jpg"           : "Сертификат соответствия ГОСТ ISO 9001-2015. Область сертификации системы менеджмента качества.",
    "attestat-akreditaci.jpg"       : "Аттестат аккредитации испытательной лаборатории от 8 февраля 2021 года.",
}

index_template = jinja_env.get_template("index.jinja")
index_page = index_template.render(**globals())

with open('index.html', "w", encoding='utf-8') as f:
    f.write(index_page)
