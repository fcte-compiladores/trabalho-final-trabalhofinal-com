#parser

import unittest
import sys
import os

# Adiciona o diretório pai (lox/) ao sys.path para permitir importações relativas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lox.lexer import Lexer, TokenType
from lox.parser import Parser, Num, BinOp
from lox.errors import ParserError # Importa a exceção personalizada

class TestParser(unittest.TestCase):

    def test_single_integer(self):
        lexer = Lexer("5")
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, Num)
        self.assertEqual(ast.value, 5)

    def test_simple_addition(self):
        lexer = Lexer("3 + 5")
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, BinOp)
        self.assertIsInstance(ast.left, Num)
        self.assertEqual(ast.left.value, 3)
        self.assertEqual(ast.op.type, TokenType.PLUS)
        self.assertIsInstance(ast.right, Num)
        self.assertEqual(ast.right.value, 5)

    def test_simple_subtraction(self):
        lexer = Lexer("10 - 2")
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, BinOp)
        self.assertEqual(ast.left.value, 10)
        self.assertEqual(ast.op.type, TokenType.NEG)
        self.assertEqual(ast.right.value, 2)

    def test_multiplication_precedence(self):
        # 2 + 3 * 4  -> 2 + (3 * 4)
        lexer = Lexer("2 + 3 * 4")
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, BinOp) # A raiz deve ser o +
        self.assertEqual(ast.op.type, TokenType.PLUS)
        self.assertEqual(ast.left.value, 2)

        self.assertIsInstance(ast.right, BinOp) # O lado direito do + deve ser um *
        self.assertEqual(ast.right.op.type, TokenType.MULTIPLY)
        self.assertEqual(ast.right.left.value, 3)
        self.assertEqual(ast.right.right.value, 4)

    def test_parentheses(self):
        # (7 - 2) * 5
        lexer = Lexer("(7 - 2) * 5")
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, BinOp) # A raiz deve ser o *
        self.assertEqual(ast.op.type, TokenType.MULTIPLY)
        self.assertEqual(ast.right.value, 5)

        self.assertIsInstance(ast.left, BinOp) # O lado esquerdo do * deve ser um -
        self.assertEqual(ast.left.op.type, TokenType.NEG)
        self.assertEqual(ast.left.left.value, 7)
        self.assertEqual(ast.left.right.value, 2)

    def test_complex_expression(self):
        # 10 + 5 * (2 - 1)
        lexer = Lexer("10 + 5 * (2 - 1)")
        parser = Parser(lexer)
        ast = parser.parse()
        # Estrutura esperada: BinOp(Num(10), +, BinOp(Num(5), *, BinOp(Num(2), -, Num(1))))
        self.assertIsInstance(ast, BinOp)
        self.assertEqual(ast.op.type, TokenType.PLUS)
        self.assertEqual(ast.left.value, 10)

        # Verifica o lado direito (multiplicação)
        right_mul_node = ast.right
        self.assertIsInstance(right_mul_node, BinOp)
        self.assertEqual(right_mul_node.op.type, TokenType.MULTIPLY)
        self.assertEqual(right_mul_node.left.value, 5)

        # Verifica o lado direito da multiplicação (subtração dentro dos parênteses)
        right_sub_node = right_mul_node.right
        self.assertIsInstance(right_sub_node, BinOp)
        self.assertEqual(right_sub_node.op.type, TokenType.NEG)
        self.assertEqual(right_sub_node.left.value, 2)
        self.assertEqual(right_sub_node.right.value, 1)

    def test_missing_rparen_error(self):
        # Teste para parêntese não fechado
        lexer = Lexer("2 * (3 + 4")
        parser = Parser(lexer)
        with self.assertRaisesRegex(ParserError, "Erro de sintaxe: Esperado token 'TokenType.RPAREN', mas encontrado 'TokenType.EOF'"): # Usa ParserError
            parser.parse()

    def test_unexpected_token_error(self):
        # Teste para operador no lugar errado
        lexer = Lexer("2 + * 3")
        parser = Parser(lexer)
        with self.assertRaisesRegex(ParserError, "Erro de sintaxe: Esperado um número ou '\('"): # Usa ParserError
            parser.parse()

if __name__ == '__main__':
    unittest.main() ----- a fazer