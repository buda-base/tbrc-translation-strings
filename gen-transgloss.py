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

LANGS_DST_LST = ["bo", "zh_CN", "fr", "de", "jp", "ru"]

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
        csvlines.append(csvline)
        for langdst in LANGS_DST_LST:
            if prop in propsother[langdst]:
                csvline.append(propsother[langdst][prop])
            else:
                csvline.append("")
    with open('tbrcorggloss.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for line in csvlines:
            csvwriter.writerow(line)

main()
