import unittest

from lexer.lexer import Lexer


class LexerTests(unittest.TestCase):
    def test_one(self):
        l = Lexer('sample.ps')
        l.lex()
        print l.tokens


if __name__ == '__main__':
    unittest.main()
