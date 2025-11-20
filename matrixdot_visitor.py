from antlr4 import *
from MatrixDotParser import MatrixDotParser
from MatrixDotVisitor import MatrixDotVisitor

class EvalVisitor(MatrixDotVisitor):
    def __init__(self):
        super().__init__()
        self.env = {}

    def visitProg(self, ctx:MatrixDotParser.ProgContext):
        for s in ctx.stat():
            self.visit(s)

    def visitMatrix_decl(self, ctx:MatrixDotParser.Matrix_declContext):
        name = ctx.ID().getText()
        mat = self.visit(ctx.matrix_literal())
        self.env[name] = mat
        return mat

    def visitAssign_stmt(self, ctx:MatrixDotParser.Assign_stmtContext):
        name = ctx.ID().getText()
        val = self.visit(ctx.expr())
        self.env[name] = val
        return val

    def visitPrint_stmt(self, ctx:MatrixDotParser.Print_stmtContext):
        val = self.visit(ctx.expr())
        print(val)
        return val

    def visitExpr(self, ctx:MatrixDotParser.ExprContext):
        if ctx.function_call():
            return self.visit(ctx.function_call())
        if ctx.matrix_literal():
            return self.visit(ctx.matrix_literal())
        if ctx.ID():
            name = ctx.ID().getText()
            if name not in self.env:
                raise Exception(f"Variable '{name}' no definida")
            return self.env[name]
        if ctx.NUMBER():
            numtext = ctx.NUMBER().getText()
            return float(numtext) if '.' in numtext else int(numtext)

    def visitFunction_call(self, ctx:MatrixDotParser.Function_callContext):
        if ctx.getChild(0).getText() == 'dot':
            a = self.visit(ctx.expr(0))
            b = self.visit(ctx.expr(1))
            return self._dot(a, b)
        else:
            a = self.visit(ctx.expr(0))
            b = self.visit(ctx.expr(1))
            return self._matmul(a, b)

    def visitMatrix_literal(self, ctx:MatrixDotParser.Matrix_literalContext):
        if ctx.row_list() is None:
            return []
        rows = []
        for r in ctx.row_list().row():
            if r.number_list() is None:
                rows.append([])
            else:
                nums = []
                for n in r.number_list().NUMBER():
                    t = n.getText()
                    nums.append(float(t) if '.' in t else int(t))
                rows.append(nums)
        return rows

    def _shape(self, m):
        rows = len(m)
        cols = 0 if rows == 0 else len(m[0])
        return (rows, cols)

    def _flatten(self, m):
        flat = []
        for r in m:
            flat.extend(r)
        return flat

    def _dot(self, a, b):
        flat_a = self._flatten(a) if isinstance(a, list) else [a]
        flat_b = self._flatten(b) if isinstance(b, list) else [b]
        if len(flat_a) != len(flat_b):
            raise Exception("Dimensiones incompatibles para dot")
        return sum(x*y for x, y in zip(flat_a, flat_b))

    def _matmul(self, a, b):
        ra, ca = self._shape(a)
        rb, cb = self._shape(b)
        if ca != rb:
            raise Exception("Dimensiones incompatibles para matmul")
        res = [[0 for _ in range(cb)] for _ in range(ra)]
        for i in range(ra):
            for j in range(cb):
                res[i][j] = sum(a[i][k] * b[k][j] for k in range(ca))
        return res
