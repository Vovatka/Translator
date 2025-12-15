"""
Grammar:
    Program ::= StatementList
    StatementList ::= Statement | StatementList Statement
    Statement ::= Declaration | Assignment
    Declaration ::= "int" ID "=" Expression ";"
    Assignment ::= ID "=" Expression ";"
    Expression ::= Term | Expression "+" Term | Expression "-" Term
    Term ::= Factor | Term "*" Factor | Term "/" Factor
    Factor ::= INTEGER | ID | "(" Expression ")" | "-" Factor

Features:
    Variable declarations: int x = 10;
    Implicit variable declarations: x = 10;
    Arithmetic operations: +, -, *, /
    Parentheses for precedence control
    Unary minus operator
    Integer arithmetic only
"""

import sys
import os
import traceback
from typing import List

from modules.lexer import Scanner, TokenType
from modules.parser import Parser


def read_source_file(filename: str) -> str:
    """Read source code from a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def perform_lexical_analysis(source_code: str) -> List['Token']:
    """Perform lexical analysis and return list of tokens."""
    scanner = Scanner(source_code)
    tokens: List['Token'] = []
    
    print(f"\n{'-' * 20}LEXICAL ANALYSIS (tokens){'-' * 20}\n")
    
    while True:
        token = scanner.get_next_token()
        tokens.append(token)
        print(f"  Line {token.line}:{token.pos} - {token}")
        if token.type == TokenType.EOF:
            break
    
    return tokens


def perform_syntactic_semantic_analysis(source_code: str) -> 'ASTNode':
    """Perform syntactic and semantic analysis."""
    scanner = Scanner(source_code)
    parser = Parser(scanner)
    return parser.parse()


def main() -> None:
    """Main function."""
    
    print(f"\n{'-' * 20}ARITHMETIC EXPRESSION LANGUAGE TRANSLATOR{'-' * 20}\n")
    
    if len(sys.argv) != 2:
        print("Error: input file required")
        print("")
        print_help()
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: file '{input_file}' not found")
        sys.exit(1)
    
    source_code = read_source_file(input_file)
    
    if not source_code.strip():
        print("Error: empty input file")
        sys.exit(1)
    
    print(f"\nAnalyzing file: {input_file}")
    print(f"\n{'-' * 20}SOURCE CODE{'-' * 20}\n")
    print(source_code)

    
    try:
        perform_lexical_analysis(source_code)
        
        print(f"\n{'-' * 20}SYNTACTIC AND SEMANTIC ANALYSIS{'-' * 20}\n")
        
        scanner = Scanner(source_code)
        parser = Parser(scanner)
        ast = parser.parse()
        
        print(f"\n{'-' * 20}Abstract Syntax Tree (AST){'-' * 20}")
        print(ast)
        
        print(f"\n{'-' * 20}Final variable values{'-' * 20}\n")
        
        for var_name, value in sorted(parser.variables.items()):
            print(f"  {var_name:10} = {value}")
        
        print(f"\n{'-' * 20}TRANSLATION COMPLETED SUCCESSFULLY!{'-' * 20}\n")
        
    except SystemExit:
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
