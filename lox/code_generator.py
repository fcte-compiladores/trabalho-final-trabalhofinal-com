# lox/code_generator.py

from .parser import BinOp, Num
from .lexer import TokenType # Tipos de token para operadores

# Gera código para uma máquina de pilha a partir da AST.
class CodeGenerator:
    """Gera código de máquina de pilha a partir de uma Árvore de Sintaxe Abstrata (AST)."""
    def __init__(self):
        """Inicializa o gerador de código."""
        self.instructions = [] # Armazena as instruções geradas

    def generate(self, node):
        """Inicia a geração de código a partir de um nó raiz da AST.

        Args:
            node (AST): O nó raiz da AST a ser percorrida.

        Returns:
            list: Uma lista de strings, onde cada string é uma instrução da máquina de pilha.
        """
        self.instructions = [] # Limpa instruções para cada nova geração
        self._visit(node)
        return self.instructions

    def _visit(self, node):
        """Visita um nó da AST e chama o método de visitação apropriado.

        Este método implementa o padrão 'visitor' para percorrer a AST.

        Args:
            node (AST): O nó da AST a ser visitado.

        Raises:
            Exception: Se não houver um método de visitação implementado para o tipo de nó.
        """
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        """Método de visitação padrão para tipos de nós não esperados, usado para depuração.

        Args:
            node (AST): O nó da AST não reconhecido.

        Raises:
            Exception: Sempre levanta uma exceção para tipos de nós não implementados.
        """
        raise Exception(f'Nenhum método _visit_{type(node).__name__} implementado')

    def _visit_BinOp(self, node):
        """Visita um nó de operação binária (BinOp) e gera as instruções correspondentes.

        Gera código para os operandos esquerdo e direito, seguido da instrução do operador.

        Args:
            node (BinOp): O nó BinOp a ser visitado.

        Raises:
            Exception: Se um tipo de operador desconhecido for encontrado.
        """
        self._visit(node.left)  # Código para o operando esquerdo
        self._visit(node.right) # Código para o operando direito

        # Emite a instrução da operação
        if node.op.type == TokenType.PLUS:
            self.instructions.append('ADD')
        elif node.op.type == TokenType.NEG:
            self.instructions.append('SUB')
        elif node.op.type == TokenType.MULTIPLY:
            self.instructions.append('MUL')
        elif node.op.type == TokenType.DIVIDE:
            self.instructions.append('DIV')
        else:
            # Isso não deve acontecer se o parser estiver correto
            self.error(f"Operador desconhecido: {node.op.type}")

    def _visit_Num(self, node):
        """Visita um nó de número (Num) e gera uma instrução PUSH com seu valor.

        Args:
            node (Num): O nó Num a ser visitado.
        """
        self.instructions.append(f'PUSH {node.value}')

# Exemplos de uso para testar o gerador de código.
if __name__ == "__main__":
    from lexer import Lexer, TokenType
    from parser import Parser, BinOp, Num # Importa nós da AST do parser

    print("--- Testando CodeGenerator ---")

    # Exemplo 1: 3 + 5
    text1 = "3 + 5"
    print(f"\nExpressão: '{text1}'")
    lexer1 = Lexer(text1)
    parser1 = Parser(lexer1)
    ast1 = parser1.parse()
    generator1 = CodeGenerator()
    code1 = generator1.generate(ast1)
    print("Código Gerado:")
    for instruction in code1:
        print(instruction)
    # Saída esperada:
    # PUSH 3
    # PUSH 5
    # ADD

    # Exemplo 2: 10 + 2 * 3
    text2 = "10 + 2 * 3"
    print(f"\nExpressão: '{text2}'")
    lexer2 = Lexer(text2)
    parser2 = Parser(lexer2)
    ast2 = parser2.parse()
    generator2 = CodeGenerator()
    code2 = generator2.generate(ast2)
    print("Código Gerado:")
    for instruction in code2:
        print(instruction)
    # Saída esperada:
    # PUSH 10
    # PUSH 2
    # PUSH 3
    # MUL
    # ADD

    # Exemplo 3: (7 - 2) / 5
    text3 = "(7 - 2) / 5"
    print(f"\nExpressão: '{text3}'")
    lexer3 = Lexer(text3)
    parser3 = Parser(lexer3)
    ast3 = parser3.parse()
    generator3 = CodeGenerator()
    code3 = generator3.generate(ast3)
    print("Código Gerado:")
    for instruction in code3:
        print(instruction)
    # Saída esperada:
    # PUSH 7
    # PUSH 2
    # SUB
    # PUSH 5
    # DIV

    # Exemplo 4: (10 + 2) * (5 - 1) / 3
    text4 = "(10 + 2) * (5 - 1) / 3"
    print(f"\nExpressão: '{text4}'")
    lexer4 = Lexer(text4)
    parser4 = Parser(lexer4)
    ast4 = parser4.parse()
    generator4 = CodeGenerator()
    code4 = generator4.generate(ast4)
    print("Código Gerado:")
    for instruction in code4:
        print(instruction)
    # Saída esperada:
    # PUSH 10
    # PUSH 2
    # ADD
    # PUSH 5
    # PUSH 1
    # SUB
    # MUL
    # PUSH 3
    # DIV