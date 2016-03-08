from kate.models import Match
from kate.modules import values, pawn, rook, knight, bishop, queen, king


DIRS = {
    'north' : 1,
    'south' : 2,
    'east' : 3,
    'west' : 4,
    'north-east' : 5,
    'south-west' : 6,
    'north-west' : 7,
    'south-east' : 8,
    'valid' : 9,
    'undefined' : 10 


REVERSE_DIRS = {
    DIRS['north'] : DIRS['south'],
    DIRS['south'] : DIRS['north'],
    DIRS['east'] : DIRS['west'],
    DIRS['west'] : DIRS['east'],
    DIRS['north-east'] : DIRS['south-west'],
    DIRS['south-west'] : DIRS['north-east'],
    DIRS['north-west'] : DIRS['south-east'],
    DIRS['south-east'] : DIRS['north-west'],
    DIRS['valid'] : DIRS['valid'],
    DIRS['undefined'] : DIRS['undefined']
}

UNDEF_X = 8
UNDEF_Y = 8


def is_move_color_ok(piece, count):
    color = Match.color_of_piece(piece)
    if(count % 2 == 0 and color == Match.COLORS['white']):
        return True
    elif(count % 2 == 1 and color == Match.COLORS['black']):
        return True
    else:
        return False


def is_move_inbounds(srcx, srcy, dstx, dsty):
    if(srcx < 0 or srcx > 7 or srcy < 0 or srcy > 7 or
       dstx < 0 or dstx > 7 or dsty < 0 or dsty > 7):
        return False
    else:
        return True

def search(match, srcx, srcy, stepx, stepy):
    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(field != Match.PIECES['blk']):
            return x, y

        x += stepx
        y += stepy
    return UNDEF_X, UNDEF_Y


def pin_dir(match, scrx, srcy):
    piece = match.readfield(scrx, srcy)
    color = Match.color_of_piece(piece)
    if(color == Match.COLORS['white']):
        kgx = match.wKg_x
        kgy = match.wKg_y
    else:
        kgx = match.bKg_x
        kgy = match.bKg_y

    direction, stepx, stepy = rook.rk_step(None, scrx, srcy, kgx, kgy)
    if(direction != DIRS['undefined']):
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        piece = match.readfield(dstx, dsty)
        if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
            (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
            reverse_dir = REVERSE_DIRS[direction]
            reverse_dir, stepx, stepy = rook.rk_step(reverse_dir, None, None, None, None)
            dstx, dsty = search(match, scrx, srcy, stepx, stepy)
            if(dstx != UNDEF_X):
                piece = match.readfield(dstx, dsty)
                if(color == Match.COLORS['white']):
                    if(piece == Match.PIECES['bQu'] or piece == Match.PIECES['bRk']):
                        return direction
                    else:
                        return DIRS['undefined']
                else:
                    if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['wRk']):
                        return direction
                    else:
                        return DIRS['undefined']

    direction, stepx, stepy = bishop.bp_step(None, scrx, srcy, kgx, kgy)
    if(direction != DIRS['undefined']):
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        piece = match.readfield(dstx, dsty)
        if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
            (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
            reverse_dir = REVERSE_DIRS[direction]
            reverse_dir, stepx, stepy = bishop.bp_step(reverse_dir, None, None, None, None)
            dstx, dsty = search(match, scrx, srcy, stepx, stepy)
            if(dstx != UNDEF_X):
                piece = match.readfield(dstx, dsty)
                if(color == Match.COLORS['white']):
                    if(piece == Match.PIECES['bQu'] or piece == Match.PIECES['bBp']):
                        return direction
                    else:
                        return DIRS['undefined']
                else:
                    if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['wBp']):
                        return direction
                    else:
                        return DIRS['undefined']
        
    return DIRS['undefined']


def attacked(match, scrx, srcy):
    piece = match.readfield(scrx, srcy)

    color = Match.color_of_piece(piece)

    RK_DIRS = [ DIRS['north'], DIRS['south'], DIRS['east'], DIRS['west'] ]
    for i in range(0, 4, 1):
        direction, stepx, stepy = rook.rk_step(RK_DIRS[i], None, None, None, None)
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        if(dstx != UNDEF_X):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bRk'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wRk'])) ):
                return True, dstx, dsty

    BP_DIRS = [ DIRS['north-east'], DIRS['south-west'], DIRS['north-west'], DIRS['south-east'] ]
    for i in range(0, 4, 1):
        direction, stepx, stepy = rook.bp_step(BP_DIRS[i], None, None, None, None)
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        if(dstx != UNDEF_X):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bBp'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wBp'])) ):
                return True, dstx, dsty

    # knight
    # pawn
    # king
    return True


def is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece):
    piece = match.readfield(srcx, srcy)

    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False

    if(not is_move_color_ok(piece, match.count)):
        return False

    if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
        if(not pawn.is_move_ok(match, srcx, srcy, dstx, dsty, piece, prom_piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        if(not rook.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        if(not knight.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        if(not bishop.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
        if(not queen.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
        if(not king.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    else:
        return False
