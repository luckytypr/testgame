from ..core import DictionarableTextChoices


class WinnerStatus(DictionarableTextChoices):
    UNDERFINED = "UNDERFIND", "Underfind"
    LEFT = "LEFT", "Left player won"
    RIGHT = "RIGHT", "Right player won"
    DRAW = "DRAW", "Draw game"
