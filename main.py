from pyknp import Juman
from analyser.frequency_counter import MorphemeCounter
import json

# temp .json file for checking functionality
with open('./result/output-2020-10-29.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rank=[]
with open('./result/rank.txt', 'r', encoding='utf-8') as f:
    for line in f:
        rank.append(tuple(line.split()))

cnt = MorphemeCounter(counter=rank, 
                        ignore_list=['特殊', '未定義語', '助詞', '人名', '地名', '組織名', '判定詞', '助動詞'])
jumanpp = Juman()

for item in data:
    temp = jumanpp.analysis(item['title'])
    cnt.process(temp)
    temp = jumanpp.analysis(item['article'])
    cnt.process(temp)

# expected output from frequency counter
# ます 548
# いる 326
# する 268
# ...

with open('./result/rank.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join('%s %s' % x for x in cnt.get()))