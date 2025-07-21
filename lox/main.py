# lox/main.py

import sys
import os

from .lexer import Lexer, TokenType
from .parser import Parser
from .code_generator import CodeGenerator
from .errors import LexerError, ParserError # Exceções personalizadas

def run_compiler(expression_text):
    """Executa as fases de compilação para uma dada expressão.

    Realiza análise léxica, análise sintática e geração de código.

    Args:
        expression_text (str): A string contendo a expressão a ser compilada.

    Raises:
        LexerError: Se ocorrer um erro durante a análise léxica.
        ParserError: Se ocorrer um erro durante a análise sintática.
        Exception: Para quaisquer outros erros inesperados durante o processo.
    """
    print(f"\n--- Processando Expressão: '{expression_text}' ---")
    try:
        # Análise Léxica
        lexer = Lexer(expression_text)
        print("\nTokens Gerados:")
        tokens = []
        token = lexer.get_next_token()
        while token.type != TokenType.EOF:
            print(f"  {token}")
            tokens.append(token)
            token = lexer.get_next_token()
        print(f"  {token}") # Imprime o token EOF

        # Reinicia o lexer para garantir que o parser consuma os tokens do início.
        lexer_for_parser = Lexer(expression_text)

        # Análise Sintática e Construção da AST
        parser = Parser(lexer_for_parser)
        print("\nConstruindo Árvore de Sintaxe Abstrata (AST)...")
        ast = parser.parse()
        print(f"  AST construída com sucesso. Raiz da AST: {type(ast).__name__}")
        # print(f"  Estrutura da AST: {repr(ast)}") # Comentado para depuração

        # Geração de Código
        code_generator = CodeGenerator()
        print("\nGerando Código para Máquina de Pilha...")
        instructions = code_generator.generate(ast)
        print("  Código Gerado:")
        for instr in instructions:
            print(f"    {instr}")

    except LexerError as e:
        print(f"\n!!! ERRO LÉXICO: {e}", file=sys.stderr)
    except ParserError as e:
        print(f"\n!!! ERRO DE SINTAXE: {e}", file=sys.stderr)
    except Exception as e:
        print(f"\n!!! ERRO INESPERADO: {e}", file=sys.stderr)

def main():
    """Ponto de entrada principal do compilador Lox.

    Suporta execução via linha de comando (com expressão direta ou arquivo)
    e um modo interativo (REPL).
    """
    args = sys.argv[1:]

    if len(args) > 0:
        # Modo de linha de comando
        expression_input = " ".join(args)
        if expression_input.startswith("-f"): # Leitura de arquivo
            if len(args) < 2:
                print("Uso: python3 -m lox.main -f <caminho_do_arquivo>", file=sys.stderr)
                sys.exit(1)
            file_path = args[1]
            if not os.path.exists(file_path):
                print(f"Erro: Arquivo não encontrado: {file_path}", file=sys.stderr)
                sys.exit(1)
            with open(file_path, 'r', encoding='utf-8') as f:
                expression_to_process = f.read()
            run_compiler(expression_to_process)
        else:
            run_compiler(expression_input)
    else:
        # Modo Interativo (REPL - Read-Eval-Print Loop)
        print("Bem-vindo ao Gerador de Código de Expressões Aritméticas!")
        print("Digite uma expressão (ex: 10 + 2 * 3) ou 'sair' para encerrar.")
        while True:
            try:
                expression_input = input(">>> ")
                if expression_input.lower() == 'sair':
                    print("Saindo...")
                    break
                if not expression_input.strip(): # Ignora entradas vazias
                    continue

                run_compiler(expression_input)
                print("\n" + "="*50 + "\n") # Separador para facilitar a leitura

            except EOFError: # Ctrl+D
                print("\nSaindo...")
                break
            except Exception as e:
                # Captura erros inesperados que não foram tratados pelas exceções específicas
                print(f"Erro inesperado no REPL: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Garante que as importações relativas funcionem quando main.py é executado como módulo.
    # É a forma recomendada para execução em Python para lidar com pacotes.
    if __name__ == "__main__" and not hasattr(sys, 'frozen'):
        pass
    main()