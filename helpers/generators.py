import random
import string


class Randoms:
    def __init__(self):
        self.letters = string.ascii_lowercase

    def random_string(self):
        return "".join(random.sample(self.letters, 10))
