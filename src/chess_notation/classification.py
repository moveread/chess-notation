from .styles import Style, Check, Mate, Castle, PawnCapture, PieceCapture, Default

def is_check(san: str) -> bool:
    return "+" in san

def is_mate(san: str) -> bool:
    return "#" in san

def is_pawn_capture(san: str) -> bool:
    return "x" in san and not san[0].isupper()

def is_piece_capture(san: str) -> bool:
    return "x" in san and san[0].isupper()

def is_castle(san: str) -> bool:
    return "-" in san

def king_effect(san_move: str) -> Style:
    """Effect a move has on the enemy king: check, mate or none"""
    if is_mate(san_move):
        return Mate
    elif is_check(san_move):
        return Check
    else:
        return Default

def motion(san_move: str) -> Style:
    """Type of motion of a move: castle, piece capture, pawn capture or normal"""
    if is_castle(san_move):
        return Castle
    elif is_piece_capture(san_move):
        return PieceCapture
    elif is_pawn_capture(san_move):
        return PawnCapture
    else:
        return Default