class Lexer(object):
    def __init__(self, filename):
        self.pos = 0
        self.data = open(filename).read()
        self.lineno = 1
        self.tokens = []

    def _tokenize(self):
        state = 0
        partial = ''
        char = self.data[self.pos]
        self.pos += 1

        while char:
            if char == '\n':
                self.lineno += 1

            partial += char

            if state == 0:
                partial = char
                if char.isspace():
                    state = 0
                elif char.isalpha():
                    state = 1
                elif char.isdigit():
                    state = 3
                elif char == ';':
                    state = 14
                elif char == '.':
                    state = 15
                elif char == ',':
                    state = 18
                elif char == ':':
                    state = 19
                elif char == "<":
                    state = 22
                elif char == ">":
                    state = 26
                elif char in "+-":
                    state = 29
                elif char in "*/":
                    state = 30
                elif char == '(':
                    state = 31
                elif char == ')':
                    state = 32
                elif char == '[':
                    state = 33
                elif char == ']':
                    state = 34
                elif char == '=':
                    state = 35
                elif char == '{':
                    state = 36
                elif char == '\"':
                    state = 37
                elif char == '\'':
                    state = 39
                else:
                    raise Exception('Invalid char %s on line %s' % (char, self.lineno))
            elif state == 1:
                if char.isalnum():
                    state = 1
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 2
            elif state == 2:
                self.pos -= 1
                partial = partial[:-1]
                if is_keyword(partial):
                    return Token('KEYWORD', partial, self.lineno)
                else:
                    return Token('IDENTIFIER', partial, self.lineno)
            elif state == 3:
                if char.isdigit():
                    state = 3
                elif char == '@':
                    state = 5
                elif char == '.':
                    state = 8
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 4
            elif state == 4:
                self.pos -= 1
                partial = partial[:-1]
                return Token(Atoms.BASE10_NUM, partial, self.lineno)
            elif state == 5:
                if is_digit(char):
                    state = 6
                else:
                    raise Exception('Invalid char %s on line %s' % (char, self.lineno))
            elif state == 6:
                if is_digit(char):
                    state = 6
                elif not char.isspace():
                    raise Exception('Invalid char %s on line %s' % (char, self.lineno))
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 7
            elif state == 7:
                self.pos -= 1
                partial = partial[:-1]
                base, number = partial.split("@")
                # Convert to base 10
                partial = str(int(number, int(base)))
                return Token('INTEGER', partial, self.lineno)
            elif state == 8:
                if char.isdigit():
                    state = 9
                elif char == '.':
                    # x..y case; go back 2 positions and return a BASE10_NUM
                    self.pos -= 2
                    partial = partial[:-2]
                    state = 4
                else:
                    raise Exception('Invalid char %s on line %s' % (char, self.lineno))
            elif state == 9:
                if char.isdigit():
                    state = 9
                elif char in 'Ee':
                    state = 11
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 10
            elif state == 10:
                self.pos -= 1
                partial = partial[:-1]
                return Token('REAL', partial, self.lineno)
            elif state == 11:
                if char in '+-':
                    state = 12
                elif char.isdigit():
                    state = 13
                else:
                    raise Exception('Invalid char %s on line %s' % (char, self.lineno))
            elif state == 12:
                if char.isdigit():
                    state = 13
                else:
                    raise Exception('Invalid char %s on line %s' % (char, self.lineno))
            elif state == 13:
                if char.isdigit():
                    state = 13
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 10
            elif state == 14:
                self.pos -= 1
                partial = partial[:-1]
                return Token('SEMICOLON', partial, self.lineno)
            elif state == 15:
                if char == '.':
                    state = 16
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 17
            elif state == 16:
                self.pos -= 1
                partial = partial[:-1]
                return Token('RANGE', partial, self.lineno)
            elif state == 17:
                self.pos -= 1
                partial = partial[:-1]
                return Token('DOT', partial, self.lineno)
            elif state == 18:
                self.pos -= 1
                partial = partial[:-1]
                return Token('COMMA', partial, self.lineno)
            elif state == 19:
                if char == '=':
                    state = 21
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 20
            elif state == 20:
                self.pos -= 1
                partial = partial[:-1]
                return Token('COLON', partial, self.lineno)
            elif state == 21:
                self.pos -= 1
                partial = partial[:-1]
                return Token('ATTRIB', partial, self.lineno)
            elif state == 22:
                if char == '=':
                    state = 23
                elif char == '>':
                    state = 24
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 25
            elif state == 23:
                self.pos -= 1
                partial = partial[:-1]
                return Token('LE', partial, self.lineno)
            elif state == 24:
                self.pos -= 1
                partial = partial[:-1]
                return Token(Atoms.NOT_EQUAL, partial, self.lineno)
            elif state == 25:
                self.pos -= 1
                partial = partial[:-1]
                return Token('LT', partial, self.lineno)
            elif state == 26:
                if char == '=':
                    state = 27
                else:
                    self.pos -= 1
                    partial = partial[:-1]
                    state = 28
            elif state == 27:
                self.pos -= 1
                partial = partial[:-1]
                return Token('GE', partial, self.lineno)
            elif state == 28:
                self.pos -= 1
                partial = partial[:-1]
                return Token('GT', partial, self.lineno)
            elif state == 29:
                self.pos -= 1
                partial = partial[:-1]
                return Token(Atoms.OP_AD, partial, self.lineno)
            elif state == 30:
                self.pos -= 1
                partial = partial[:-1]
                return Token(Atoms.OP_MUL, partial, self.lineno)
            elif state == 31:
                self.pos -= 1
                partial = partial[:-1]
                return Token('LP', partial, self.lineno)
            elif state == 32:
                self.pos -= 1
                partial = partial[:-1]
                return Token('RP', partial, self.lineno)
            elif state == 33:
                self.pos -= 1
                partial = partial[:-1]
                return Token('LSB', partial, self.lineno)
            elif state == 34:
                self.pos -= 1
                partial = partial[:-1]
                return Token('RSB', partial, self.lineno)
            elif state == 35:
                self.pos -= 1
                partial = partial[:-1]
                return Token('EQUAL', partial, self.lineno)
            elif state == 36:
                if char == '}':
                    state = 0
                else:
                    state = 36
            elif state == 37:
                if char == '\"':
                    state = 38
                else:
                    state = 37
            elif state == 38:
                self.pos -= 1
                partial = partial[:-1]
                return Token('STRING', partial, self.lineno)
            elif state == 39:
                state = 40
            elif state == 40:
                if char == '\'':
                    state = 41
                else:
                    raise Exception('Invalid char %s on line %s' % (char, self.lineno))
            elif state == 41:
                self.pos -= 1
                partial = partial[:-1]
                return Token('CHAR', partial, self.lineno)

            char = self.data[self.pos]
            self.pos += 1
        return False

    def lex(self):
        token = self._tokenize()
        while token:
            self.tokens.append(token)
            token = self._tokenize()


def is_keyword(partial):
    return partial in ['begin', 'end', 'case', 'char', 'const', 'div', 'do',
                       'record', 'downto', 'else', 'end', 'for', 'function',
                       'if', 'print', 'integer', 'mod', 'not', 'of', 'or',
                       'procedure', 'program', 'real', 'repeat', 'then',
                       'until', 'var', 'while', 'import', 'array',
                       'otherwise', 'read']
