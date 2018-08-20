from .piece import *
from .rook import cRook
from .bishop import cBishop


class cQueen(cPiece):
    STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        direction = cRook.dir_for_move(srcx, srcy, dstx, dsty)
        if(rookdir == cls.DIRS['undefined']):
            direction = cBishop.dir_for_move(srcx, srcy, dstx, dsty)
        return direction

    @classmethod
    def step_for_dir(cls, direction):
        stepx, stepy = cRook.step_for_dir(direction)
        if(stepx == cls.UNDEF_X):
            stepx, stepy = cBishop.step_for_dir(direction)
        return stepx, stepy

    def is_piece_trapped(self):
        crook = cRook(self.match, self.xpos, self.ypos)
        rflag = crook.is_piece_trapped()
        cbishop = cBishop(self.match, self.xpos, self.ypos)
        bflag = cbishop.is_piece_trapped()
        return rflag or bflag

    def is_piece_stuck_new(self):
        crook = cRook(self.match, self.xpos, self.ypos)
        rflag = crook.is_piece_stuck_new()
        cbishop = cBishop(self.match, self.xpos, self.ypos)
        bflag = cbishop.is_piece_stuck_new()
        return rflag or bflag

    def is_move_stuck(self, dstx, dsty):
        crook = cRook(self.match, self.xpos, self.ypos)
        rflag = crook.is_move_stuck(dstx, dsty)
        cbishop = cBishop(self.match, self.xpos, self.ypos)
        bflag = cbishop.is_move_stuck(dstx, dsty)
        return rflag or bflag

    def is_move_valid(self, dstx, dsty):
        crook = cRook(self.match, self.xpos, self.ypos)
        rflag = crook.is_move_valid(dstx, dsty)
        cbishop = cBishop(self.match, self.xpos, self.ypos)
        bflag = cbishop.is_move_valid(dstx, dsty)
        return rflag or bflag

# class end

