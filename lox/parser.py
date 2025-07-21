# lox/parser.py

from .lexer import TokenType, Token
import sys
from .errors import ParserError # Importa a exceção personalizada

# Classes para a Árvore de Sintaxe Abstrata (AST).
# Cada classe representa um nó na árvore.

class AST:
    """Classe base abstrata para todos os nós da Árvore de Sintaxe Abstrata (AST)."""
    pass

class BinOp(AST):
    """Representa uma operação binária na AST (ex: `left OP right`)."""
    def __init__(self, left, op, right):
        """Inicializa um nó de operação binária.

        Args:
            left (AST): O nó da subexpressão esquerda.
            op (Token): O token do operador (PLUS, NEG, MULTIPLY, DIVIDE).
            right (AST): O nó da subexpressão direita.
        """
        self.left = left    # Subexpressão esquerda
        self.op = op        # Token do operador
        self.right = right  # Subexpressão direita
    def __repr__(self):
        return f"BinOp({repr(self.left)}, {self.op.value}, {repr(self.right)})"

class Num(AST):
    """Representa um número inteiro na AST."""
    def __init__(self, token):
        """Inicializa um nó de número.

        Args:
            token (Token): O token INTEGER que contém o valor numérico.
        """
        self.token = token
        self.value = token.value # O valor numérico
    def __repr__(self):
        return f"Num({self.value})"

# O Parser constrói a AST a partir dos tokens.
class Parser:
    """O analisador sintático que constrói a Árvore de Sintaxe Abstrata (AST)."""
    def __init__(self, lexer):
        """Inicializa o parser com uma instância do lexer.

        Args:
            lexer (Lexer): Uma instância do analisador léxico.
        """
        self.lexer = lexer
        # O primeiro token da entrada.
        self.current_token = self.lexer.get_next_token()

    def error(self, message="Erro de sintaxe"):
        """Levanta uma exceção ParserError com detalhes sobre o erro sintático.

        Args:
            message (str): A mensagem de erro.
        
        Raises:
            ParserError: Sempre levanta uma ParserError com a mensagem formatada.
        """
        raise ParserError(f"{message} em '{self.current_token.value}' do tipo {self.current_token.type}")

    def eat(self, token_type):
        """Consome o token atual se ele corresponder ao tipo esperado e avança.

        Args:
            token_type (TokenType): O tipo de token esperado.

        Raises:
            ParserError: Se o token atual não for do tipo esperado.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Esperado token '{token_type}', mas encontrado '{self.current_token.type}'")

    def factor(self):
        """
        Analisa um 'factor' da gramática: INTEGER | LPAREN expr RPAREN.
        Lida com números inteiros e expressões agrupadas por parênteses.

        Returns:
            AST: Um nó Num ou um nó AST que representa a expressão dentro dos parênteses.
        """
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr() # Chama expr recursivamente para a subexpressão
            self.eat(TokenType.RPAREN)
            return node
        else:
            self.error("Esperado um número ou '('")

    def term(self):
        """
        Analisa um 'term' da gramática: factor ((MULTIPLY | DIVIDE) factor)*.
        Lida com operações de multiplicação e divisão, aplicando a precedência correta.

        Returns:
            AST: Um nó AST que representa o termo analisado.
        """
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        Analisa uma 'expr' da gramática: term ((PLUS | NEG) term)*.
        Lida com operações de adição e subtração, aplicando a precedência correta.
        Esta é a regra de maior nível para a análise de expressões.

        Returns:
            AST: Um nó AST que representa a expressão analisada.
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.NEG):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.NEG:
                self.eat(TokenType.NEG)

            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        """
        Inicia o processo de análise sintática e retorna a raiz da AST.

        Returns:
            AST: O nó raiz da Árvore de Sintaxe Abstrata (AST).

        Raises:
            ParserError: Se houver caracteres extras após a expressão válida.
        """
        node = self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error("Caracteres extras após a expressão")
        return node

# Exemplos de uso para testar o parser.
if __name__ == "__main__":
    from lexer import Lexer, TokenType

    # Teste 1: Expressão simples
    text1 = "3 + 5"
    print(f"Parsing: '{text1}'")
    lexer1 = Lexer(text1)
    parser1 = Parser(lexer1)
    ast1 = parser1.parse()
    print(f"AST para '{text1}' construída com sucesso (tipo da raiz: {type(ast1).__name__})\n")

    # Teste 2: Precedência de operadores
    text2 = "10 + 2 * 3"
    print(f"Parsing: '{text2}'")
    lexer2 = Lexer(text2)
    parser2 = Parser(lexer2)
    ast2 = parser2.parse()
    print(f"AST para '{text2}' construída com sucesso (tipo da raiz: {type(ast2).__name__})\n")

    # Teste 3: Parênteses
    text3 = "(7 - 2) / 5"
    print(f"Parsing: '{text3}'")
    lexer3 = Lexer(text3)
    parser3 = Parser(lexer3)
    ast3 = parser3.parse()
    print(f"AST para '{text3}' construída com sucesso (tipo da raiz: {type(ast3).__name__})\n")

    # Teste 4: Expressão complexa
    text4 = "2 + 3 * (4 - 1) / 2"
    print(f"Parsing: '{text4}'")
    lexer4 = Lexer(text4)
    parser4 = Parser(lexer4)
    ast4 = parser4.parse()
    print(f"AST para '{text4}' construída com sucesso (tipo da raiz: {type(ast4).__name__})\n")

    # Teste 5: Erro de sintaxe (parênteses não fechados)
    text5 = "2 * (3 + 4"
    print(f"Parsing: '{text5}' (Esperado erro)")
    try:
        lexer5 = Lexer(text5)
        parser5 = Parser(lexer5)
        parser5.parse()
    except Exception as e:
        print(e)
    print("-" * 30 + "\n")

    # Teste 6: Erro de sintaxe (operador no lugar errado)
    text6 = "2 + * 3"
    print(f"Parsing: '{text6}' (Esperado erro)")
    try:
        lexer6 = Lexer(text6)
        parser6 = Parser(lexer6)
        parser6.parse()
    except Exception as e:
        print(e)
    print("-" * 30 + "\n")