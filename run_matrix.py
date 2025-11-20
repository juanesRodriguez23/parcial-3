from antlr4 import *
from MatrixDotLexer import MatrixDotLexer
from MatrixDotParser import MatrixDotParser
from matrixdot_visitor import EvalVisitor

def execute(code):
    input_stream = InputStream(code)
    lexer = MatrixDotLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MatrixDotParser(stream)
    tree = parser.prog()
    visitor = EvalVisitor()
    visitor.visit(tree)

program = """
matrix A = [[1,2,3],[4,5,6]];
matrix B = [[7,8,9],[10,11,12]];
x = dot(A, B);
print(x);
m = matmul([[1,2],[3,4]], [[5,6],[7,8]]);
print(m);
"""

if __name__ == "__main__":
    execute(program)
