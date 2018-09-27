from .values import *


class cBoard:
    COORD = {
        '1' : 0,
        '2' : 1,
        '3' : 2,
        '4' : 3,
        '5' : 4,
        '6' : 5,
        '7' : 6,
        '8' : 7,
    }

    def __init__(self):
        self.fields = [ [PIECES['wRk'], PIECES['wKn'], PIECES['wBp'], PIECES['wQu'], PIECES['wKg'], PIECES['wBp'], PIECES['wKn'], PIECES['wRk']],
                        [PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw']],
                        [PIECES['bRk'], PIECES['bKn'], PIECES['bBp'], PIECES['bQu'], PIECES['bKg'], PIECES['bBp'], PIECES['bKn'], PIECES['bRk']] ]

    def set_to_base(self):
        self.fields[self.COORD['1']][self.COORD['1']] = PIECES['wRk']
        self.fields[self.COORD['1']][self.COORD['2']] = PIECES['wKn']
        self.fields[self.COORD['1']][self.COORD['3']] = PIECES['wBp']
        self.fields[self.COORD['1']][self.COORD['4']] = PIECES['wQu']
        self.fields[self.COORD['1']][self.COORD['5']] = PIECES['wKg']
        self.fields[self.COORD['1']][self.COORD['6']] = PIECES['wBp']
        self.fields[self.COORD['1']][self.COORD['7']] = PIECES['wKn']
        self.fields[self.COORD['1']][self.COORD['8']] = PIECES['wRk']

        for y in range (self.COORD['2'], (self.COORD['2'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = PIECES['wPw']

        for y in range (self.COORD['3'], (self.COORD['6'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = PIECES['blk']

        for y in range (self.COORD['7'], (self.COORD['7'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = PIECES['bPw']

        self.fields[self.COORD['8']][self.COORD['1']] = PIECES['bRk']
        self.fields[self.COORD['8']][self.COORD['2']] = PIECES['bKn']
        self.fields[self.COORD['8']][self.COORD['3']] = PIECES['bBp']
        self.fields[self.COORD['8']][self.COORD['4']] = PIECES['bQu']
        self.fields[self.COORD['8']][self.COORD['5']] = PIECES['bKg']
        self.fields[self.COORD['8']][self.COORD['6']] = PIECES['bBp']
        self.fields[self.COORD['8']][self.COORD['7']] = PIECES['bKn']
        self.fields[self.COORD['8']][self.COORD['8']] = PIECES['bRk']

    def writefield(self, x, y, value):
        self.fields[y][x] = value

    def readfield(self, x, y):
        return self.fields[y][x]

    def search(self, srcx, srcy, stepx, stepy):
        x = srcx + stepx
        y = srcy + stepy
        while(x >= self.COORD['1'] and x <= self.COORD['8'] and y >= self.COORD['1'] and y <= self.COORD['8']):
            field = self.readfield(x, y)
            if(field != PIECES['blk']):
                return x, y
            x += stepx
            y += stepy
        return None, None

    @classmethod
    def is_inbounds(cls, x, y):
        if(x < cls.COORD['1'] or x > cls.COORD['8'] or y < cls.COORD['1'] or y > cls.COORD['8']):
            return False
        else:
            return True

    @classmethod
    def is_move_inbounds(cls, srcx, srcy, dstx, dsty):
        if(srcx < cls.COORD['1'] or srcx > cls.COORD['8'] or srcy < cls.COORD['1'] or srcy > cls.COORD['8'] or
           dstx < cls.COORD['1'] or dstx > cls.COORD['8'] or dsty < cls.COORD['1'] or dsty > cls.COORD['8']):
            return False
        else:
            return True

# class end