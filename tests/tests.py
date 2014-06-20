import unittest

from lexer.lexer import Lexer
from parser.parser import Parser


class Tests(unittest.TestCase):
    def test_one(self):
        l = Lexer('tests/sample.ps')
        l.lex()
        self.assertEqual([(t.name, t.value) for t in l.tokens], [('KEYWORD', 'program'), ('IDENTIFIER', 'hellowld'), ('SEMICOLON', ';'), ('KEYWORD', 'begin'), ('IDENTIFIER', 'writeln'), ('LP', '('), ('BASE10_NUM', '2'), ('RP', ')'), ('SEMICOLON', ';'), ('IDENTIFIER', 'readln'), ('SEMICOLON', ';'), ('KEYWORD', 'end')])

        p = Parser(l.tokens)
        try:
            p.parse()
        except SyntaxError:
            self.fail()

    def test_two(self):
        l = Lexer('tests/sample2.ps')
        l.lex()
        self.assertEqual([(t.name, t.value) for t in l.tokens], [('KEYWORD', 'program'), ('IDENTIFIER', 'exFunction'), ('SEMICOLON', ';'), ('KEYWORD', 'var'), ('IDENTIFIER', 'a'), ('COMMA', ','), ('IDENTIFIER', 'b'), ('COMMA', ','), ('IDENTIFIER', 'ret'), ('COLON', ':'), ('KEYWORD', 'integer'), ('SEMICOLON', ';'), ('KEYWORD', 'function'), ('IDENTIFIER', 'max'), ('LP', '('), ('IDENTIFIER', 'num1'), ('COMMA', ','), ('IDENTIFIER', 'num2'), ('COLON', ':'), ('KEYWORD', 'integer'), ('RP', ')'), ('COLON', ':'), ('KEYWORD', 'integer'), ('SEMICOLON', ';'), ('KEYWORD', 'var'), ('IDENTIFIER', 'result'), ('COLON', ':'), ('KEYWORD', 'integer'), ('SEMICOLON', ';'), ('KEYWORD', 'begin'), ('KEYWORD', 'if'), ('LP', '('), ('IDENTIFIER', 'num1'), ('GT', '>'), ('IDENTIFIER', 'num2'), ('RP', ')'), ('KEYWORD', 'then'), ('IDENTIFIER', 'result'), ('ATTRIB', ':='), ('IDENTIFIER', 'num1'), ('KEYWORD', 'else'), ('IDENTIFIER', 'result'), ('ATTRIB', ':='), ('IDENTIFIER', 'num2'), ('SEMICOLON', ';'), ('IDENTIFIER', 'max'), ('ATTRIB', ':='), ('IDENTIFIER', 'result'), ('SEMICOLON', ';'), ('KEYWORD', 'end'), ('SEMICOLON', ';'), ('KEYWORD', 'begin'), ('IDENTIFIER', 'a'), ('ATTRIB', ':='), ('BASE10_NUM', '100'), ('SEMICOLON', ';'), ('IDENTIFIER', 'b'), ('ATTRIB', ':='), ('BASE10_NUM', '200'), ('SEMICOLON', ';'), ('IDENTIFIER', 'ret'), ('ATTRIB', ':='), ('IDENTIFIER', 'max'), ('LP', '('), ('IDENTIFIER', 'a'), ('COMMA', ','), ('IDENTIFIER', 'b'), ('RP', ')'), ('SEMICOLON', ';'), ('IDENTIFIER', 'writeln'), ('LP', '('), ('IDENTIFIER', 'ret'), ('RP', ')'), ('SEMICOLON', ';'), ('KEYWORD', 'end')])

        p = Parser(l.tokens)
        try:
            p.parse()
        except SyntaxError:
            self.fail()


if __name__ == '__main__':
    unittest.main()
