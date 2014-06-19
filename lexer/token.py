class Token(object):
    def __init__(self, name, value, lineno):
        self.name = name
        self.value = value
        self.lineno = lineno
