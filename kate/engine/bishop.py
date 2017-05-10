from kate.engine import match
from kate.engine import rules


NEAST_X = 1
NEAST_Y = 1
SWEST_X = -1
SWEST_Y = -1
NWEST_X = -1
NWEST_Y = 1
SEAST_X = 1
SEAST_Y = -1

STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]

blank = match.PIECES['blk']
GEN_STEPS = [ [[1, 1, blank], [2, 2, blank], [3, 3, blank], [4, 4, blank], [5, 5, blank], [6, 6, blank], [7, 7, blank]],
              [[-1, -1, blank], [-2, -2, blank], [-3, -3, blank], [-4, -4, blank], [-5, -5, blank], [-6, -6, blank], [-7, -7, blank]],
              [[1, -1, blank], [2, -2, blank], [3, -3, blank], [4, -4, blank], [5, -5, blank], [6, -6, blank], [7, -7, blank]],
              [[-1, 1, blank], [-2, 2, blank], [-3, 3, blank], [-4, 4, blank], [-5, 5, blank], [-6, 6, blank], [-7, 7, blank]] ]


def is_field_touched(match, color, fieldx, fieldy):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == match.COLORS['white'] and (piece == match.PIECES['wQu'] or piece == match.PIECES['wBp'])) or
                (color == match.COLORS['black'] and (piece == match.PIECES['bQu'] or piece == match.PIECES['bBp'])) ):
                return True

    return False


def list_field_touches(match, color, fieldx, fieldy):
    touches = []
    
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == match.COLORS['white'] and (piece == match.PIECES['wQu'] or piece == match.PIECES['wBp'])) or
                (color == match.COLORS['black'] and (piece == match.PIECES['bQu'] or piece == match.PIECES['bBp'])) ):
                touches.append([piece, x1, y1])

    return touches

  
def does_attack(match, srcx, srcy, dstx, dsty):
    priority = 5

    bishop = match.readfield(srcx, srcy)

    if(bishop != match.PIECES['wBp'] and bishop != match.PIECES['wQu'] and bishop != match.PIECES['bBp'] and bishop != match.PIECES['bQu']):
        return False, 0

    color = match.color_of_piece(bishop)
    opp_color = match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                if(piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
                    return True, 2 # priority
                else:
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        priority = min(priority, 2)
                    else:
                        match.writefield(srcx, srcy, match.PIECES['blk'])
                        touched = rules.is_field_touched(match, opp_color, dstx, dsty)
                        match.writefield(srcx, srcy, bishop)
                        if(touched):
                            priority = min(priority, 3)
                        elif(rules.is_field_touched(match, opp_color, x1, y1)):
                            if(match.PIECES_RANK[piece] >= match.PIECES_RANK[bishop]):
                                priority = min(priority, 2)
                            else:
                                priority = min(priority, 3)
                        else:
                            priority = min(priority, 2)

    if(priority == 5):
        return False, 0
    else:
        return True, priority


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    bishop = match.readfield(srcx, srcy)

    if(bishop != match.PIECES['wBp'] and bishop != match.PIECES['wQu'] and bishop != match.PIECES['bBp'] and bishop != match.PIECES['bQu']):
        return count

    color = match.color_of_piece(bishop)
    opp_color = match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                count += 1

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    bishop = match.readfield(srcx, srcy)

    if(bishop != match.PIECES['wBp'] and bishop != match.PIECES['wQu'] and bishop != match.PIECES['bBp'] and bishop != match.PIECES['bQu']):
        return score

    color = match.color_of_piece(bishop)
    opp_color = match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                score += match.ATTACKED_SCORES[piece]
                pin_dir = rules.pin_dir(match, x1, y1)
                direction = bp_dir(srcx, srcy, x1, y1)
                if(pin_dir == direction):
                    if(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp'] or piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
                        score += match.ATTACKED_SCORES[piece] // 4
                    else:
                        score += match.ATTACKED_SCORES[piece] // 2     

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = 5

    bishop = match.readfield(srcx, srcy)

    if(bishop != match.PIECES['wBp'] and bishop != match.PIECES['wQu'] and bishop != match.PIECES['bBp'] and bishop != match.PIECES['bQu']):
        return False, 0

    color = match.color_of_piece(bishop)
    opp_color = match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == match.PIECES['blk'] or piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
                continue
            if( color == match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, 2 # priority
                    else:
                        if(match.PIECES_RANK[piece] >= match.PIECES_RANK[bishop]):
                            return True, 2 # priority
                        else:
                            priority = min(priority, 3)

    if(priority == 5):
        return False, 0
    else:
        return True, priority


def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    bishop = match.readfield(srcx, srcy)

    if(bishop != match.PIECES['wBp'] and bishop != match.PIECES['wQu'] and bishop != match.PIECES['bBp'] and bishop != match.PIECES['bQu']):
        return score

    color = match.color_of_piece(bishop)
    opp_color = match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == match.PIECES['blk'] or piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
                continue
            if( color == match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += match.SUPPORTED_SCORES[piece]

    return score 


def bp_dir(srcx, srcy, dstx, dsty):
    DIRS = rules.DIRS
    if( (srcx - dstx) == (srcy - dsty) and (srcy < dsty) ):
        return DIRS['north-east']
    elif( (srcx - dstx) == (srcy - dsty) and (srcy > dsty) ):
        return DIRS['south-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy < dsty) ):
        return DIRS['north-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy > dsty) ):
        return DIRS['south-east']
    else:
        return DIRS['undefined']


def bp_step(direction=None, srcx=None, srcy=None, dstx=None, dsty=None):
    DIRS = rules.DIRS
    if(direction == None):
        direction = bp_dir(srcx, srcy, dstx, dsty)

    if(direction == DIRS['north-east']):
        return direction, NEAST_X, NEAST_Y
    elif(direction == DIRS['south-west']):
        return direction, SWEST_X, SWEST_Y
    elif(direction == DIRS['north-west']):
        return direction, NWEST_X, NWEST_Y
    elif(direction == DIRS['south-east']):
        return direction, SEAST_X, SEAST_Y
    else:
        return direction, rules.UNDEF_X, rules.UNDEF_Y

    
def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
    DIRS = rules.DIRS
    direction, stepx, stepy = bp_step(None, srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    color = match.color_of_piece(piece)

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(direction == DIRS['north-east'] or direction == DIRS['south-west']):
        if(pin_dir != DIRS['north-east'] and pin_dir != DIRS['south-west'] and pin_dir != DIRS['undefined']):
            return False
    elif(direction == DIRS['north-west'] or direction == DIRS['south-east']):
        if(pin_dir != DIRS['north-west'] and pin_dir != DIRS['south-east'] and pin_dir != DIRS['undefined']):
            return False

    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(x == dstx and y == dsty):
            if(match.color_of_piece(field) == color):
                return False
            else:
                return True
        elif(field != match.PIECES['blk']):
            return False

        x += stepx
        y += stepy

    return False
