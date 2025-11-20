from antlr4 import *
from MatrixLangParser import MatrixLangParser
from MatrixLangVisitor import MatrixLangVisitor

class MatrixLangEvalVisitor(MatrixLangVisitor):
    """
    Visitor para evaluar programas MatLang
    Implementa las operaciones matriciales y validaciones semánticas
    """
    
    def __init__(self):
        self.symbol_table = {}
        super().__init__()

    def visitProgram(self, ctx: MatrixLangParser.ProgramContext):
        """Visita un programa completo"""
        results = []
        for stmt in ctx.statement():
            result = self.visit(stmt)
            if result is not None:
                results.append(result)
        return results

    def visitMatrix_declaration(self, ctx: MatrixLangParser.Matrix_declarationContext):
        """Visita una declaración de matriz"""
        var_name = ctx.ID().getText()
        matrix_value = self.visit(ctx.matrix_expression())
        self.symbol_table[var_name] = matrix_value
        print(f"Matriz '{var_name}' definida: {self._format_value(matrix_value)}")
        return matrix_value

    def visitAssignment(self, ctx: MatrixLangParser.AssignmentContext):
        """Visita una asignación"""
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expression())
        self.symbol_table[var_name] = value
        print(f"Variable '{var_name}' asignada: {self._format_value(value)}")
        return value

    def visitPrint_statement(self, ctx: MatrixLangParser.Print_statementContext):
        """Visita una sentencia print"""
        value = self.visit(ctx.expression())
        formatted = self._format_value(value)
        print(f"Resultado: {formatted}")
        return value

    def visitExpression(self, ctx: MatrixLangParser.ExpressionContext):
        """Visita una expresión"""
        if ctx.function_call():
            return self.visit(ctx.function_call())
        elif ctx.matrix_expression():
            return self.visit(ctx.matrix_expression())
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name not in self.symbol_table:
                raise Exception(f"Error semántico: Variable '{var_name}' no definida")
            return self.symbol_table[var_name]
        elif ctx.NUMBER():
            num_text = ctx.NUMBER().getText()
            return float(num_text) if '.' in num_text else int(num_text)

    def visitMatrix_expression(self, ctx: MatrixLangParser.Matrix_expressionContext):
        """Visita una expresión matricial"""
        if ctx.matrix_literal():
            return self.visit(ctx.matrix_literal())
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name not in self.symbol_table:
                raise Exception(f"Error semántico: Variable '{var_name}' no definida")
            return self.symbol_table[var_name]
        elif ctx.matrix_expression():
            # Operaciones binarias: +, -
            if len(ctx.matrix_expression()) == 2:
                left = self.visit(ctx.matrix_expression(0))
                right = self.visit(ctx.matrix_expression(1))
                operator = ctx.PLUS().getText() if ctx.PLUS() else ctx.MINUS().getText()
                return self._matrix_binary_operation(left, right, operator)
        return None

    def visitFunction_call(self, ctx: MatrixLangParser.Function_callContext):
        """Visita una llamada a función"""
        try:
            if ctx.DOT():
                matrix1 = self.visit(ctx.expression(0))
                matrix2 = self.visit(ctx.expression(1))
                return self._dot_product(matrix1, matrix2)
                
            elif ctx.MATMUL():
                matrix1 = self.visit(ctx.expression(0))
                matrix2 = self.visit(ctx.expression(1))
                return self._matrix_multiplication(matrix1, matrix2)
                
            elif ctx.TRANSPOSE():
                matrix = self.visit(ctx.expression(0))
                return self._transpose_matrix(matrix)
                
            elif ctx.DETERMINANT():
                matrix = self.visit(ctx.expression(0))
                return self._matrix_determinant(matrix)
                
            elif ctx.INVERSE():
                matrix = self.visit(ctx.expression(0))
                return self._matrix_inverse(matrix)
                
        except Exception as e:
            raise Exception(f"Error en operación matricial: {str(e)}")

    def visitMatrix_literal(self, ctx: MatrixLangParser.Matrix_literalContext):
        """Visita un literal de matriz"""
        if not ctx.row_list():
            return []  # Matriz vacía
        
        rows = []
        for row_ctx in ctx.row_list().row():
            row_value = self.visit(row_ctx)
            rows.append(row_value)
        
        # Validar que todas las filas tengan la misma longitud
        if rows:
            first_len = len(rows[0])
            for i, row in enumerate(rows):
                if len(row) != first_len:
                    raise Exception(f"Error semántico: Filas de longitud inconsistente. Fila 0: {first_len}, Fila {i}: {len(row)}")
        
        return rows

    def visitRow(self, ctx: MatrixLangParser.RowContext):
        """Visita una fila de matriz"""
        if not ctx.number_list():
            return []  # Fila vacía
        
        numbers = []
        for num_ctx in ctx.number_list().NUMBER():
            num_text = num_ctx.getText()
            numbers.append(float(num_text) if '.' in num_text else int(num_text))
        return numbers

    # ==================== OPERACIONES MATRICIALES ====================

    def _dot_product(self, a, b):
        """Calcula el producto punto entre dos matrices/vectores"""
        flat_a = self._flatten_matrix(a)
        flat_b = self._flatten_matrix(b)
        
        if len(flat_a) != len(flat_b):
            raise Exception(
                f"Producto punto requiere mismo número de elementos. "
                f"Recibidos: {len(flat_a)} y {len(flat_b)} elementos"
            )
        
        result = sum(x * y for x, y in zip(flat_a, flat_b))
        print(f"Producto punto: {self._format_value(a)} · {self._format_value(b)} = {result}")
        return result

    def _matrix_multiplication(self, a, b):
        """Realiza multiplicación matricial"""
        shape_a = self._get_matrix_shape(a)
        shape_b = self._get_matrix_shape(b)
        
        if shape_a[1] != shape_b[0]:
            raise Exception(
                f"Multiplicación matricial requiere columnas(A) == filas(B). "
                f"Recibidos: {shape_a[1]} columnas y {shape_b[0]} filas"
            )
        
        # Convertir escalares a matrices si es necesario
        if shape_a == (1, 1):
            a = [[a]] if isinstance(a, (int, float)) else a
        if shape_b == (1, 1):
            b = [[b]] if isinstance(b, (int, float)) else b
            
        rows_a, cols_a = self._get_matrix_shape(a)
        rows_b, cols_b = self._get_matrix_shape(b)
        
        result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
        
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += a[i][k] * b[k][j]
        
        print(f"Multiplicación matricial: {shape_a} × {shape_b} = {self._get_matrix_shape(result)}")
        return result

    def _transpose_matrix(self, matrix):
        """Transpone una matriz"""
        shape = self._get_matrix_shape(matrix)
        if shape == (1, 1):
            return matrix
            
        rows, cols = shape
        transposed = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                transposed[j][i] = matrix[i][j]
        
        print(f"Transposición: {shape} -> {self._get_matrix_shape(transposed)}")
        return transposed

    def _matrix_determinant(self, matrix):
        """Calcula el determinante de una matriz (solo 2x2 por simplicidad)"""
        shape = self._get_matrix_shape(matrix)
        if shape != (2, 2):
            raise Exception(f"Determinante solo soportado para matrices 2x2. Recibida: {shape}")
        
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        print(f"Determinante: {self._format_value(matrix)} = {det}")
        return det

    def _matrix_inverse(self, matrix):
        """Calcula la inversa de una matriz 2x2"""
        shape = self._get_matrix_shape(matrix)
        if shape != (2, 2):
            raise Exception(f"Inversa solo soportada para matrices 2x2. Recibida: {shape}")
        
        det = self._matrix_determinant(matrix)
        if det == 0:
            raise Exception("Matriz singular, no tiene inversa")
        
        a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
        inverse = [
            [d/det, -b/det],
            [-c/det, a/det]
        ]
        
        print(f"Inversa calculada para matriz {shape}")
        return inverse

    def _matrix_binary_operation(self, left, right, operation):
        """Realiza operaciones binarias element-wise"""
        shape_left = self._get_matrix_shape(left)
        shape_right = self._get_matrix_shape(right)
        
        if shape_left != shape_right:
            raise Exception(
                f"Operaciones matriciales requieren mismas dimensiones. "
                f"Recibidos: {shape_left} y {shape_right}"
            )
        
        if operation == '+':
            if shape_left == (1, 1):
                return left + right
            return [[left[i][j] + right[i][j] for j in range(len(left[0]))] for i in range(len(left))]
        elif operation == '-':
            if shape_left == (1, 1):
                return left - right
            return [[left[i][j] - right[i][j] for j in range(len(left[0]))] for i in range(len(left))]

    # ==================== UTILIDADES ====================

    def _flatten_matrix(self, matrix):
        """Convierte una matriz en lista plana"""
        if isinstance(matrix, (int, float)):
            return [matrix]
        flat = []
        for item in matrix:
            if isinstance(item, list):
                flat.extend(self._flatten_matrix(item))
            else:
                flat.append(item)
        return flat

    def _get_matrix_shape(self, matrix):
        """Obtiene la forma (filas, columnas) de una matriz"""
        if isinstance(matrix, (int, float)):
            return (1, 1)
        if not matrix:
            return (0, 0)
        if isinstance(matrix[0], list):
            rows = len(matrix)
            cols = len(matrix[0])
            # Verificar consistencia
            for row in matrix:
                if len(row) != cols:
                    raise Exception("Matriz irregular detectada")
            return (rows, cols)
        else:
            return (1, len(matrix))

    def _format_value(self, value):
        """Formatea un valor para impresión"""
        if isinstance(value, list):
            if not value:
                return "[]"
            if isinstance(value[0], list):
                return '[\n  ' + ',\n  '.join(self._format_value(row) for row in value) + '\n]'
            else:
                return '[' + ', '.join(self._format_value(item) for item in value) + ']'
        else:
            return str(value)