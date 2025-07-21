# lox/errors.py

class CompilerError(Exception):
    """Classe base para erros do compilador."""
    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.line = line
        self.column = column

    def __str__(self):
        if self.line is not None and self.column is not None:
            return f"[Erro na linha {self.line}, coluna {self.column}] {self.args[0]}"
        return f"[Erro] {self.args[0]}"

class LexerError(CompilerError):
    """Erro ocorrido durante a fase de análise léxica."""
    pass

class ParserError(CompilerError):
    """Erro ocorrido durante a fase de análise sintática."""
    pass
