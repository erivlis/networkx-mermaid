from enum import Enum, StrEnum


class DiagramLayout(StrEnum):
    """Layout of a Mermaid diagram"""
    DAGRE = 'dagre'
    ELK = 'elk'


class DiagramLook(StrEnum):
    """Look of a Mermaid diagram"""
    NEO = 'neo'


class DiagramTheme(StrEnum):
    """Theme of a Mermaid diagram"""
    NEUTRAL = 'neutral'


class DiagramOrientation(StrEnum):
    """Orientation of a Mermaid graph"""
    TOP_DOWN = 'TD'
    BOTTOM_UP = 'BT'
    LEFT_RIGHT = 'LR'
    RIGHT_LEFT = 'RL'


class DiagramNodeShape(Enum):
    """Shapes of a Mermaid graph node"""
    DEFAULT = ("(", ")")
    RECTANGLE = ("[", "]")
    ROUND_RECTANGLE = ("([", "])")
    SUBROUTINE = ("[[", "]]")
    DATABASE = ("[(", ")]")
    CIRCLE = ("((", "))")
    DOUBLE_CIRCLE = ("(((", ")))")
    FLAG = (">", "]")
    DIAMOND = ("{", "}")
    HEXAGON = ("{{", "}}")
    PARALLELOGRAM = ("[/", "/]")
    PARALLELOGRAM_ALT = ("[\\", "\\]")
    TRAPEZOID = ("[/", "\\]")
    TRAPEZOID_ALT = ("[\\", "/]")
