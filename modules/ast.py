from enum import Enum
from typing import List


class NodeType(Enum):
    """Types of AST nodes."""
    PROGRAM = "PROGRAM"
    DECLARATION = "DECLARATION"
    ASSIGNMENT = "ASSIGNMENT"
    BINARY_OP = "BINARY_OP"
    UNARY_OP = "UNARY_OP"
    VARIABLE = "VARIABLE"
    INTEGER = "INTEGER"


class ASTNode:
    """Represents a node in the Abstract Syntax Tree."""
    
    def __init__(self, node_type: NodeType, value: str = "") -> None:
        self.node_type: NodeType = node_type
        self.value: str = value
        self.children: List['ASTNode'] = []
    
    def add_child(self, node: 'ASTNode') -> None:
        """Add a child node to this node."""
        self.children.append(node)
    
    def __str__(self, level: int = 0) -> str:
        """String representation of the AST node with indentation."""
        ret = "  " * level + f"{self.node_type.value}"
        if self.value:
            ret += f": {self.value}"
        ret += "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
    
    def __repr__(self) -> str:
        """Representation of the AST node for debugging."""
        return f"ASTNode({self.node_type.value}, {self.value})"
