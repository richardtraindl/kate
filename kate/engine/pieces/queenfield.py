from .piecefield import cPieceField
from .rookfield import cRookField
from .bishopfield import cBishopField


class cQueenField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [match.PIECES['wQu'], match.PIECES['wRk'], match.PIECES['wBp']], [match.PIECES['bQu'], match.PIECES['bRk'], match.PIECES['bBp']])
        self.STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]

    def is_field_touched(self, color, mode):
        crookfield = cRookField(self.match, self.fieldx, self.fieldy)
        cbishopfield = cBishopField(self.match, self.fieldx, self.fieldy)
        return crookfield.is_field_touched(color, mode) or cbishopfield.is_field_touched(color, mode)

    def field_color_touches(self, color, frdlytouches, enmytouches):
        crookfield = cRookField(self.match, self.fieldx, self.fieldy)
        crookfield.field_color_touches(color, frdlytouches, enmytouches)
        cbishopfield = cBishopField(self.match, self.fieldx, self.fieldy)
        cbishopfield.field_color_touches(color, frdlytouches, enmytouches)

    def list_field_touches(self, color):
        crookfield = cRookField(self.match, self.fieldx, self.fieldy)
        crookfield.list_field_touches(color)
        cbishopfield = cBishopField(self.match, self.fieldx, self.fieldy)
        cbishopfield.list_field_touches(color)

# class end
