from pyknp import MList
from pyknp import Juman
from collections import Counter
from collections.abc import Iterable, Mapping

class MorphemeCounter():
    def __init__(self, counter=None, ignore_list=[]):
        self.counter = Counter()
        if isinstance(counter, (Iterable, Mapping)):
            self.counter = Counter(counter)
        self.ignore_list = ignore_list

    def process(self, word_list):
        assert(isinstance(word_list, MList))
        filtered = filter(self.ignore, word_list)
        self.counter.update(map(lambda x: x.genkei, filtered))
        
    def ignore(self, x):
        for ignore_type in self.ignore_list:
            if (x.hinsi == ignore_type or x.bunrui == ignore_type):
                return False
        return True

    def get(self):
        return self.counter.most_common()
    