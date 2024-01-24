from typing import Iterable
import chess
from .styles import Style, Check, Mate, Castle, PawnCapture, PieceCapture, Default
from . import language, classification as classif

def check(style: Check, san: str) -> str:
    match style:
        case Check.NONE:
            return san.removesuffix("+")
        case Check.CHECK:
            return san
        case _:
            raise ValueError(f"Invalid check style: {style}")

def mate(style: Mate, san: str) -> str:
    match style:
        case Mate.NONE:
            return san.removesuffix("#")
        case Mate.SHARP:
            return san
        case Mate.DOUBLE_CHECK:
            return san.replace("#", "++")
        case _:
            raise ValueError(f"Invalid mate style: {style}")

def castle(style: Castle, san: str) -> str:
    match style:
        case Castle.OO:
            return san.replace("-", "")
        case Castle.O_O:
            return san
        case _:
            raise ValueError(f"Invalid castle style: {style}")

def pawn_capture(
    style: PawnCapture,
    san: str,
    captured_piece: str,
    pawn: str = "P"
) -> str:
    [d, x, e, n, *tail] = san
    assert x == "x", f"Unexpected SAN move syntax {san}"
    rest = "".join(tail)
    match style:
        case PawnCapture.de:
            return f"{d}{e}{rest}"
        case PawnCapture.dxe:
            return f"{d}x{e}{rest}"
        case PawnCapture.de4:
            return f"{d}{e}{n}{rest}"
        case PawnCapture.dxe4:
            return san
        case PawnCapture.xe4:
            return f"x{e}{n}{rest}"
        case PawnCapture.PxN:
            return f"{pawn}x{captured_piece}{rest}"
        
def piece_capture(style: PieceCapture, san: str, captured_piece: str):
    match style:
        case PieceCapture.Ne4:
            return san.replace("x", "")
        case PieceCapture.Nxe4:
            return san
        case PieceCapture.NxN:
            # Nxd4 => NxP, but also Nexd4 => NexP (to disambiguate)
            if san[1] == "x": # no disambiguation
                [N, x, d, n, *tail] = san
                rest = "".join(tail)
                return f"{N}x{captured_piece}{rest}"
            elif san[2] == "x":
                [N, e, x, d, n, *tail] = san
                rest = "".join(tail)
                return f"{N}{e}x{captured_piece}{rest}"
            else:
                raise ValueError(f"Invalid piece capture '{san}'")
            
def apply(
    style: Style,
    san: str,
    captured_piece: str = None,
    pawn_symbol: str = "P",
) -> str:
    """Applies `style` to `san` if appropiate (e.g. if `san` is 'O-O' and style is `Check.<some style>`)"""
    match style:
        case Check() if classif.is_check(san):
            return check(style, san)
        case Mate() if classif.is_mate(san):
            return mate(style, san)
        case Castle() if classif.is_castle(san):
            return castle(style, san)
        case PawnCapture() if classif.is_pawn_capture(san):
            return pawn_capture(style, san, captured_piece, pawn_symbol)
        case PieceCapture() if classif.is_piece_capture(san):
            return piece_capture(style, san, captured_piece)
        case Default():
            return san
        case s if isinstance(s, Style):
            return san
        case _:
            raise ValueError(f"Invalid style: {style}")

def representations(
    san: str,
    captured_piece: chess.PieceType = None,
    styles: set[Style] = {Check.NONE, Mate.NONE, *Castle, *PawnCapture, *PieceCapture, *Default},
    languages: list[language.Language] = ["CA", "EN"]
) -> Iterable[str]:
    motion_kind = classif.motion(san)
    effect_kind = classif.king_effect(san)
    for motion_style in set(motion_kind) & styles:
        if captured_piece is not None or (motion_style != PieceCapture.NxN and motion_style != PawnCapture.PxN):
            for effect_style in set(effect_kind) & styles:
                san1 = apply(motion_style, san, captured_piece)
                san2 = apply(effect_style, san1, captured_piece)
                for lang in languages:
                    yield language.translate(lang, san2)
