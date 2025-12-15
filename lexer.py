import sys
from enum import Enum
from typing import Optional


class TokenType(Enum):
    """Token types for language."""
    INT = "INT"
    ID = "ID"
    INTEGER = "INTEGER"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    ASSIGN = "="
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"


class Token:
    """Represents a lexical token."""
    
    def __init__(self, type: TokenType, value: str = "", line: int = 0, pos: int = 0) -> None:
        self.type: TokenType = type
        self.value: str = value
        self.line: int = line
        self.pos: int = pos
    
    def __str__(self) -> str:
        if self.value:
            return f"{self.type.value}({self.value})"
        return f"{self.type.value}"
    
    def __repr__(self) -> str:
        return self.__str__()


class Scanner:
    """Lexical analyzer that converts source code into tokens."""
    
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.position: int = 0
        self.line: int = 1
        self.line_pos: int = 1
        self.current_char: Optional[str] = self.source[0] if self.source else None
    
    def error(self, message: str) -> None:
        """Report a lexical error and exit."""
        print(f"Lexical error at line {self.line}, position {self.line_pos}: {message}")
        sys.exit(1)
    
    def advance(self) -> None:
        """Move to the next character in the source."""
        self.position += 1
        self.line_pos += 1
        
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
            
            if self.current_char == '\n':
                self.line += 1
                self.line_pos = 0
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters (space, tab, newline)."""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def get_number(self) -> str:
        """Read a sequence of digits forming a number."""
        result = ""
        start_pos = self.position
        
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char and self.current_char.isalpha():
            self.error(f"Invalid numeric literal: {result}{self.current_char}")
        
        return result
    
    def get_identifier(self) -> str:
        """Read an identifier (alphanumeric + underscore)."""
        result = ""
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        return result
    
    def get_next_token(self) -> Token:
        """Get the next token from the source."""
        while self.current_char and self.current_char.isspace():
            self.skip_whitespace()
        
        if not self.current_char:
            return Token(TokenType.EOF, "", self.line, self.line_pos)
        
        if self.current_char.isdigit():
            start_line = self.line
            start_pos = self.line_pos
            number = self.get_number()
            return Token(TokenType.INTEGER, number, start_line, start_pos)
        
        if self.current_char.isalpha() or self.current_char == '_':
            start_line = self.line
            start_pos = self.line_pos
            identifier = self.get_identifier()
            
            if identifier == "int":
                return Token(TokenType.INT, "int", start_line, start_pos)
            
            return Token(TokenType.ID, identifier, start_line, start_pos)
        
        start_line = self.line
        start_pos = self.line_pos
        char = self.current_char
        
        if char == '+':
            self.advance()
            return Token(TokenType.PLUS, "+", start_line, start_pos)
        elif char == '-':
            self.advance()
            return Token(TokenType.MINUS, "-", start_line, start_pos)
        elif char == '*':
            self.advance()
            return Token(TokenType.MULTIPLY, "*", start_line, start_pos)
        elif char == '/':
            self.advance()
            return Token(TokenType.DIVIDE, "/", start_line, start_pos)
        elif char == '=':
            self.advance()
            return Token(TokenType.ASSIGN, "=", start_line, start_pos)
        elif char == ';':
            self.advance()
            return Token(TokenType.SEMICOLON, ";", start_line, start_pos)
        elif char == '(':
            self.advance()
            return Token(TokenType.LPAREN, "(", start_line, start_pos)
        elif char == ')':
            self.advance()
            return Token(TokenType.RPAREN, ")", start_line, start_pos)
        
        self.error(f"Unknown character: '{char}'")
        return Token(TokenType.UNKNOWN, char, start_line, start_pos)
