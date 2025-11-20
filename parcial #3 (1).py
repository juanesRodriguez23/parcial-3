"""
Modelo de Gramática SQL-CRUD
Definiciones formales de producciones y atributos
"""

class SQLGrammarModel:
    """Modelo formal de la gramática SQL-CRUD"""
    
    @staticmethod
    def get_formal_grammar():
        """Retorna la gramática formal en notación EBNF"""
        return {
            'Producciones Principales': {
                'program': 'statement_list',
                'statement_list': 'statement statement_list | ε',
                'statement': 'create_stmt | select_stmt | insert_stmt | update_stmt | delete_stmt'
            },
            
            'CREATE TABLE': {
                'create_stmt': 'CREATE TABLE ID ( column_def_list ) ;',
                'column_def_list': 'column_def ( , column_def )*',
                'column_def': 'ID type_spec ( PRIMARY KEY )?',
                'type_spec': 'INT | FLOAT | STRING | BOOL | DATE'
            },
            
            'SELECT': {
                'select_stmt': 'SELECT select_list FROM ID where_opt ;',
                'select_list': '* | column_list',
                'column_list': 'ID ( , ID )*',
                'where_opt': 'WHERE condition | ε'
            },
            
            'INSERT': {
                'insert_stmt': 'INSERT INTO ID ( column_list ) VALUES ( value_list ) ;',
                'value_list': 'literal ( , literal )*'
            },
            
            'UPDATE': {
                'update_stmt': 'UPDATE ID SET set_list where_opt ;',
                'set_list': 'set_item ( , set_item )*',
                'set_item': 'ID = expr'
            },
            
            'DELETE': {
                'delete_stmt': 'DELETE FROM ID where_opt ;'
            },
            
            'Expresiones y Condiciones': {
                'condition': 'expr comp_operator expr | condition logic_operator condition',
                'expr': 'ID | literal | expr binop expr',
                'comp_operator': '= | != | > | < | >= | <=',
                'logic_operator': 'AND | OR',
                'literal': 'NUMBER | STRING | NULL'
            }
        }
    
    @staticmethod
    def get_attribute_definitions():
        """Retorna las definiciones de atributos sintéticos e inherentes"""
        return {
            'Atributos Sintéticos': {
                'symbol_table': 'Tabla de símbolos actualizada',
                'type': 'Tipo de la sentencia o expresión',
                'table_def': 'Definición de tabla',
                'columns': 'Lista de columnas',
                'name': 'Nombre de columna',
                'data_type': 'Tipo de dato'
            },
            
            'Atributos Inherentes': {
                'inherited_symbol_table': 'Tabla de símbolos del contexto padre',
                'parent_table': 'Tabla padre para herencia',
                'inherited_table': 'Definición de tabla del contexto'
            },
            
            'Reglas Semánticas Principales': {
                'Validación de existencia': 'Verificar que tablas y columnas existan',
                'Compatibilidad de tipos': 'Validar tipos en operaciones y asignaciones',
                'Consistencia de esquema': 'Mantener integridad del schema',
                'Verificación de constraints': 'Validar PRIMARY KEY, etc.'
            }
        }


class SQLExampleGenerator:
    """Generador de ejemplos SQL válidos"""
    
    @staticmethod
    def generate_examples():
        """Genera ejemplos de sentencias SQL válidas"""
        return {
            'CREATE TABLE': [
                "CREATE TABLE users (id INT PRIMARY KEY, name STRING, age INT);",
                "CREATE TABLE products (id INT, name STRING, price FLOAT);"
            ],
            
            'SELECT': [
                "SELECT * FROM users;",
                "SELECT name, age FROM users WHERE age > 18;",
                "SELECT id, name FROM products WHERE price < 100.0;"
            ],
            
            'INSERT': [
                "INSERT INTO users (id, name, age) VALUES (1, 'John', 25);",
                "INSERT INTO products (id, name, price) VALUES (1, 'Laptop', 999.99);"
            ],
            
            'UPDATE': [
                "UPDATE users SET age = 26 WHERE id = 1;",
                "UPDATE products SET price = 899.99 WHERE name = 'Laptop';"
            ],
            
            'DELETE': [
                "DELETE FROM users WHERE id = 1;",
                "DELETE FROM products WHERE price > 1000;"
            ]
        }