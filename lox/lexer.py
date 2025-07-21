import enum
import sys

from .errors import LexerError

# Define os tipos de tokens para o lexer.
class TokenType(enum.Enum):
    # Operadores
    PLUS = 'PLUS'         # +
    NEG = 'NEG'           # - (para subtração)
    MULTIPLY = 'MULTIPLY' # *
    DIVIDE = 'DIVIDE'     # /

    # Delimitadores
    LPAREN = 'LPAREN'     # (
    RPAREN = 'RPAREN'     # )

    # Literais
    INTEGER = 'INTEGER'   # Números inteiros (ex: 123)

    # Fim da entrada
    EOF = 'EOF'           # End Of File

# Representa um token encontrado pelo lexer.
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """Retorna a representação string do token."""
        return f"Token({self.type.name}, {self.value})"

    def __repr__(self):
        """Retorna a representação do token para depuração."""
        return self.__str__()

# O analisador léxico que converte texto em tokens.
class Lexer:
    def __init__(self, text):
        """Inicializa o lexer com o texto de entrada.

        Args:
            text (str): A string de código fonte a ser analisada.
        """
        self.text = text        # O texto de entrada
        self.pos = 0            # Posição atual no texto (índice)
        self.current_char = self.text[self.pos] # Caractere atual na posição

    def error(self, message="Erro léxico"):
        """Levanta uma exceção LexerError com a mensagem e posição do erro."""
        raise LexerError(message, column=self.pos)

    def advance(self):
        """Avança para o próximo caractere na entrada, ou define como None se no final."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Fim da entrada
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Ignora caracteres de espaço em branco (espaços, tabs, novas linhas)."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Lê e retorna um número inteiro da entrada.

        Returns:
            int: O valor inteiro lido.
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Retorna o próximo token da entrada.

        Este é o método principal do lexer, responsável por identificar
        e classificar o próximo elemento léxico.

        Returns:
            Token: O próximo token reconhecido.

        Raises:
            LexerError: Se um caractere desconhecido for encontrado.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.NEG, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            self.error("Caractere desconhecido")

        return Token(TokenType.EOF, None)

# Exemplo de uso para testar o lexer.
if __name__ == "__main__":
    text = "10 + 2 * (5 - 1) / 3"
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != TokenType.EOF:
        print(token)
        token = lexer.get_next_token()
    print(token) # Imprime o token EOF
