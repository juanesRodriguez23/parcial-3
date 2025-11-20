#!/usr/bin/env python3
"""
Intérprete principal para el lenguaje MatLang
Numeral 3: Implementación ANTLR con Python
"""

import sys
import os
from antlr4 import *
from MatrixLangLexer import MatrixLangLexer
from MatrixLangParser import MatrixLangParser
from matrix_visitor import MatrixLangEvalVisitor

def main():
    """Función principal del intérprete"""
    
    print("=" * 60)
    print("        INTÉRPRETE MATLANG - OPERACIONES MATRICIALES")
    print("=" * 60)
    
    # Verificar si se proporcionó un archivo
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print(f"Error: El archivo '{input_file}' no existe.")
            sys.exit(1)
        
        print(f"Ejecutando archivo: {input_file}")
        input_stream = FileStream(input_file, encoding='utf-8')
    else:
        print("Modo interactivo. Escribe 'exit' para salir.")
        print("Ejemplo: matrix A = [[1,2],[3,4]]; print(dot(A, A));")
        print("-" * 60)
        
        lines = []
        while True:
            try:
                line = input("matlang> ")
                if line.strip().lower() in ['exit', 'quit', 'salir']:
                    break
                lines.append(line)
                if line.strip().endswith(';'):
                    input_text = '\n'.join(lines)
                    input_stream = InputStream(input_text)
                    process_input(input_stream)
                    lines = []
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nSaliendo...")
                break
        return

    # Procesar entrada
    process_input(input_stream)

def process_input(input_stream):
    """Procesa la entrada y ejecuta el programa"""
    try:
        # Crear lexer y parser
        lexer = MatrixLangLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = MatrixLangParser(stream)
        
        # Configurar manejo de errores
        lexer.removeErrorListeners()
        parser.removeErrorListeners()
        
        # Parsear el input
        tree = parser.program()
        
        if parser.getNumberOfSyntaxErrors() > 0:
            print("Errores de sintaxis detectados.")
            return
        
        # Visitar el árbol de parsing
        visitor = MatrixLangEvalVisitor()
        print("Ejecutando programa...")
        print("-" * 40)
        
        result = visitor.visit(tree)
        
        print("-" * 40)
        print("Ejecución completada exitosamente.")
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()