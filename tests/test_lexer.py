lexer


import unittest
import sys
import os

# Adiciona o diretório pai (lox/) ao sys.path para permitir importações relativas
# Isso é necessário ao executar os testes diretamente, pois 'tests' não é um pacote.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lox.lexer import Lexer, TokenType
from lox.errors import LexerError # Importa a exceção personalizada

class TestLexer(unittest.TestCase):

    def test_single_digit_integer(self):
        lexer = Lexer("5")
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.INTEGER)
        self.assertEqual(token.value, 5)
        self.assertEqual(lexer.get_next_token().type, TokenType.EOF)

    def test_multi_digit_integer(self):
        lexer = Lexer("123")
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.INTEGER)
        self.assertEqual(token.value, 123)
        self.assertEqual(lexer.get_next_token().type, TokenType.EOF)

    def test_operators(self):
        # Teste para +, -, *, /
        lexer = Lexer("+ - * /")
        self.assertEqual(lexer.get_next_token().type, TokenType.PLUS)
        self.assertEqual(lexer.get_next_token().type, TokenType.NEG)
        self.assertEqual(lexer.get_next_token().type, TokenType.MULTIPLY)
        self.assertEqual(lexer.get_next_token().type, TokenType.DIVIDE)
        self.assertEqual(lexer.get_next_token().type, TokenType.EOF)

    def test_parentheses(self):
        # Teste para ( e )
        lexer = Lexer("()")
        self.assertEqual(lexer.get_next_token().type, TokenType.LPAREN)
        self.assertEqual(lexer.get_next_token().type, TokenType.RPAREN)
        self.assertEqual(lexer.get_next_token().type, TokenType.EOF)

    def test_whitespace(self):
        # Teste para espaços em branco
        lexer = Lexer("  10   + \t 5")
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.INTEGER)
        self.assertEqual(token.value, 10)

        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.PLUS)
        self.assertEqual(token.value, '+')

        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.INTEGER)
        self.assertEqual(token.value, 5)
        self.assertEqual(lexer.get_next_token().type, TokenType.EOF)

    def test_complex_expression(self):
        # Teste de expressão mais complexa
        text = "10 + 2 * (5 - 1) / 3"
        lexer = Lexer(text)
        tokens = [
            (TokenType.INTEGER, 10),
            (TokenType.PLUS, '+'),
            (TokenType.INTEGER, 2),
            (TokenType.MULTIPLY, '*'),
            (TokenType.LPAREN, '('),
            (TokenType.INTEGER, 5),
            (TokenType.NEG, '-'),
            (TokenType.INTEGER, 1),
            (TokenType.RPAREN, ')'),
            (TokenType.DIVIDE, '/'),
            (TokenType.INTEGER, 3),
            (TokenType.EOF, None)
        ]
        for expected_type, expected_value in tokens:
            token = lexer.get_next_token()
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_invalid_character(self):
        # Teste para caractere inválido
        lexer = Lexer("10 + #")
        # Consome os tokens válidos primeiro
        lexer.get_next_token()  # Token INTEGER (10)
        lexer.get_next_token()  # Token PLUS (+)

        # A próxima chamada deve encontrar o caractere inválido e levantar a exceção
        with self.assertRaises(LexerError) as cm: # Usa LexerError
            lexer.get_next_token()
        self.assertIn("Caractere desconhecido", str(cm.exception))

if __name__ == '__main__':
    unittest.main() 