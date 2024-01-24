from enum import Enum

Check = Enum("Check", ["NONE", "CHECK"])
Mate = Enum("Mate", ["NONE", "SHARP", "DOUBLE_CHECK"])
Castle = Enum("Castle", ["OO", "O_O"])
PawnCapture = Enum("PawnCapture", ["de", "dxe", "de4", "dxe4", "xe4", "PxN"])
PieceCapture = Enum("PieceCapture", ["Ne4", "Nxe4", "NxN"])
Default = Enum("Default", ["DEFAULT"])

Style = Check | Mate | Castle | PawnCapture | PieceCapture | Default
