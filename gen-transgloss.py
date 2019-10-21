import csv
from jproperties import Properties

def get_map_for_lang(lang):
    path = "AppConstants_%s.properties" % lang
    p = Properties()
    res = {}
    with open(path, "rb") as f:
        p.load(f, "utf-8")
    for key in p:
        val, meta = p[key]
        res[key] = val
    return res

LANGS_NE_MAP = {
    "bo": "bo", 
    "zh": "zh_CN",
    "fr": "fr",
    "de": "de",
    "jp": "jp",
    "ru": "ru"
}

LANGS_DST_LST = ["bo", "zh_CN"
# for some reason, trasifex is not happy when a language is not fully translated...
#, "fr", "de", "jp", "ru"
]

def utf8len(s):
    return len(s.encode('utf-8'))

def main():
    propsen = get_map_for_lang("en")
    propsother = {}
    csvlines = []
    csvtitles = ["Term", "pos", "comment"]
    csvlines.append(csvtitles)
    for langdst in LANGS_DST_LST:
        csvtitles.append(langdst)
    for langsrc, langdst in LANGS_NE_MAP.items():
        propsother[langdst] = get_map_for_lang(langsrc)
    for prop, envalue in propsen.items():
        csvline = [envalue, "", ""]
        if utf8len(envalue) > 70:
            continue
        for langdst in LANGS_DST_LST:
            if prop in propsother[langdst]:
                val = propsother[langdst][prop]
                # transifex has a hardcoded 500 bytes value (due to their SQL database)
                if utf8len(val) > 400:
                    csvline.append("")
                    continue
                csvline.append(val)
            else:
                csvline.append("")
        csvlines.append(csvline)
    with open('tbrcorggloss.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for line in csvlines:
            csvwriter.writerow(line)

main()
