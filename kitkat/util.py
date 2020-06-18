from collections import Counter
import random

def compare(s,t):
    return Counter(s) == Counter(t)
class RandomHash(object):
    @staticmethod
    def gerator_id():
        return random.getrandbits(128)
