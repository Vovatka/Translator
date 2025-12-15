import sys
from typing import Optional, Dict

from modules.lexer import Scanner, Token, TokenType
from modules.ast import ASTNode, NodeType


class Parser:
    """Recursive descent parser with semantic analysis."""
    
    def __init__(self, scanner: Scanner) -> None:
        self.scanner: Scanner = scanner
        self.current_token: Optional[Token] = None
        self.variables: Dict[str, int] = {}
        self.declared_vars: set = set()
        self.next_token()
    
    def error(self, message: str, token: Optional[Token] = None) -> None:
        """Report a syntax error and exit."""
        if token is None:
            token = self.current_token
        
        print(f"Syntax error at line {token.line}, position {token.pos}: {message}")
        print(f"  Got token: {token}")
        sys.exit(1)
    
    def next_token(self) -> None:
        """Advance to the next token."""
        self.current_token = self.scanner.get_next_token()
    
    def eat(self, token_type: TokenType) -> None:
        """Consume a token of expected type or report error."""
        if self.current_token.type == token_type:
            self.next_token()
        else:
            self.error(f"Expected token {token_type.value}", self.current_token)
    
    def parse_program(self) -> ASTNode:
        """Parse a complete program."""
        node = ASTNode(NodeType.PROGRAM, "program")
        
        while self.current_token.type != TokenType.EOF:
            statement_node = self.parse_statement()
            if statement_node:
                node.add_child(statement_node)
        
        return node
    
    def parse_statement_list(self) -> ASTNode:
        """Parse a list of statements."""
        node = ASTNode(NodeType.PROGRAM, "statement_list")
        
        while (self.current_token.type in [TokenType.INT, TokenType.ID] and 
               self.current_token.type != TokenType.EOF):
            statement_node = self.parse_statement()
            node.add_child(statement_node)
        
        return node
    
    def parse_statement(self) -> ASTNode:
        """Parse a single statement (declaration or assignment)."""
        if self.current_token.type == TokenType.INT:
            return self.parse_declaration()
        elif self.current_token.type == TokenType.ID:
            return self.parse_assignment()
        else:
            self.error("Expected declaration or assignment")
            return None  # Never reached due to error()
    
    def parse_declaration(self) -> ASTNode:
        """Parse a variable declaration."""
        self.eat(TokenType.INT)
        
        if self.current_token.type != TokenType.ID:
            self.error("Expected identifier after int")
        
        var_name = self.current_token.value
        
        if var_name in self.declared_vars:
            print(f"Warning at line {self.current_token.line}: variable '{var_name}' already declared")
        
        self.declared_vars.add(var_name)
        self.eat(TokenType.ID)
        
        if self.current_token.type != TokenType.ASSIGN:
            self.error("Expected '=' in variable declaration")
        self.eat(TokenType.ASSIGN)
        
        expr_node = self.parse_expression()
        
        if self.current_token.type != TokenType.SEMICOLON:
            self.error("Expected ';' after expression")
        self.eat(TokenType.SEMICOLON)
        
        node = ASTNode(NodeType.DECLARATION, var_name)
        node.add_child(expr_node)
        
        value = self.evaluate_expression(expr_node)
        self.variables[var_name] = value
        print(f"Declared variable '{var_name}' = {value}")
        
        return node
    
    def parse_assignment(self) -> ASTNode:
        """Parse a variable assignment."""
        var_name = self.current_token.value
        
        if var_name not in self.declared_vars:
            self.declared_vars.add(var_name)
            print(f"Variable '{var_name}' implicitly declared at assignment")
        
        self.eat(TokenType.ID)
        
        if self.current_token.type != TokenType.ASSIGN:
            self.error("Expected '=' in assignment")
        self.eat(TokenType.ASSIGN)
        
        expr_node = self.parse_expression()
        
        if self.current_token.type != TokenType.SEMICOLON:
            self.error("Expected ';' after expression")
        self.eat(TokenType.SEMICOLON)
        
        node = ASTNode(NodeType.ASSIGNMENT, var_name)
        node.add_child(expr_node)
        
        value = self.evaluate_expression(expr_node)
        self.variables[var_name] = value
        
        if var_name in self.declared_vars and var_name not in self.variables:
            print(f"Implicitly declared variable '{var_name}' = {value}")
        else:
            print(f"Assigned '{var_name}' = {value}")
        
        return node
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression (addition/subtraction)."""
        node = self.parse_term()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            
            right_node = self.parse_term()
            
            op_node = ASTNode(NodeType.BINARY_OP, token.value)
            op_node.add_child(node)
            op_node.add_child(right_node)
            node = op_node
        
        return node
    
    def parse_term(self) -> ASTNode:
        """Parse a term (multiplication/division)."""
        node = self.parse_factor()
        
        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            
            right_node = self.parse_factor()
            
            if token.type == TokenType.DIVIDE:
                right_value = self.evaluate_expression(right_node)
                if right_value == 0:
                    self.error("Division by zero")
            
            op_node = ASTNode(NodeType.BINARY_OP, token.value)
            op_node.add_child(node)
            op_node.add_child(right_node)
            node = op_node
        
        return node
    
    def parse_factor(self) -> ASTNode:
        """Parse a factor (number, variable, parenthesized expression, or unary minus)."""
        token = self.current_token
        
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return ASTNode(NodeType.INTEGER, token.value)
        
        elif token.type == TokenType.ID:
            var_name = token.value
            
            if var_name not in self.declared_vars:
                self.error(f"Use of undeclared variable '{var_name}'")
            
            if var_name not in self.variables:
                self.error(f"Use of uninitialized variable '{var_name}'")
            
            self.eat(TokenType.ID)
            return ASTNode(NodeType.VARIABLE, var_name)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return node
        
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = self.parse_factor()
            
            unary_node = ASTNode(NodeType.UNARY_OP, "-")
            unary_node.add_child(node)
            return unary_node
        
        else:
            self.error("Expected number, identifier, parenthesis, or unary minus")
            return None  # Never reached due to error()
    
    def evaluate_expression(self, node: ASTNode) -> int:
        """Evaluate an expression tree to an integer value."""
        if node.node_type == NodeType.INTEGER:
            return int(node.value)
        
        elif node.node_type == NodeType.VARIABLE:
            var_name = node.value
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                self.error(f"Internal error: variable '{var_name}' not found in symbol table")
        
        elif node.node_type == NodeType.BINARY_OP:
            left_val = self.evaluate_expression(node.children[0])
            right_val = self.evaluate_expression(node.children[1])
            
            if node.value == "+":
                return left_val + right_val
            elif node.value == "-":
                return left_val - right_val
            elif node.value == "*":
                return left_val * right_val
            elif node.value == "/":
                if right_val == 0:
                    self.error("Division by zero during evaluation")
                return left_val // right_val
        
        elif node.node_type == NodeType.UNARY_OP:
            child_val = self.evaluate_expression(node.children[0])
            return -child_val
        
        return 0  # Should never be reached
    
    def parse(self) -> ASTNode:
        """Main parsing method."""
        return self.parse_program()
