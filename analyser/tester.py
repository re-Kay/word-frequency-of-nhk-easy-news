from pyknp import Juman
import json

with open('./../result/output-2020-10-29.json', encoding='utf-8') as f:
    data = json.load(f)

print(data[0]['title'], data[0]['date'])
article = data[0]['title']
jumanpp = Juman(jumanpp=False)
result = jumanpp.analysis(article)

for mrph in result.mrph_list():
    print("原形:%s \n" % (mrph.genkei))

