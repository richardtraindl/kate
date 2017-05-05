from kate.models import Match
from kate.modules import rules


STEP_2N1E_X = 1
STEP_2N1E_Y = 2
STEP_1N2E_X = 2
STEP_1N2E_Y = 1
STEP_1S2E_X = 2
STEP_1S2E_Y = -1
STEP_2S1E_X = 1
STEP_2S1E_Y = -2
STEP_2S1W_X = -1
STEP_2S1W_Y = -2
STEP_1S2W_X = -2
STEP_1S2W_Y = -1
STEP_1N2W_X = -2
STEP_1N2W_Y = 1
STEP_2N1W_X = -1
STEP_2N1W_Y = 2

STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]

blank = Match.PIECES['blk']
GEN_STEPS = [ [[1, 2, blank]],
              [[2, 1, blank]],
              [[2, -1, blank]], 
              [[1, -2, blank]],
              [[-1, -2, blank]],
              [[-2, -1, blank]],
              [[-2, 1, blank]],
              [[-1, 2, blank]] ]


def is_field_touched(match, color, fieldx, fieldy):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKn']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bKn']) ):
                return True

    return False


def does_attack(match, srcx, srcy, dstx, dsty):
    priority = 5

    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return False, 0

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                if(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                    return True, 1 # priority
                else:
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, 1 # priority
                    else:
                        if(rules.is_field_touched(match, opp_color, x1, y1)):
                            if(Match.PIECES_RANK[piece] >= Match.PIECES_RANK[knight]):
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

    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return count

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                count += 1

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return score

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += Match.ATTACKED_SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = 5

    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return False, 0

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, 1 # priority
                    else:
                        if(Match.PIECES_RANK[knight] <= Match.PIECES_RANK[piece]):
                            priority = min(priority, 2)
                        else:
                            priority = min(priority, 3)

    if(priority == 5):
        return False, 0
    else:
        return True, priority



def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return score

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += Match.SUPPORTED_SCORES[piece]

    return score 


def kn_dir(srcx, srcy, dstx, dsty):
    DIRS = rules.DIRS
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(step_x == STEP_2N1E_X and step_y == STEP_2N1E_Y):
        return DIRS['valid']
    elif(step_x == STEP_1N2E_X and step_y == STEP_1N2E_Y):
        return DIRS['valid']
    elif(step_x == STEP_1S2E_X and step_y == STEP_1S2E_Y):
        return DIRS['valid']
    elif(step_x == STEP_2S1E_X and step_y == STEP_2S1E_Y):
        return DIRS['valid']
    elif(step_x == STEP_2S1W_X and step_y == STEP_2S1W_Y):
        return DIRS['valid']
    elif(step_x == STEP_1S2W_X and step_y == STEP_1S2W_Y):
        return DIRS['valid']
    elif(step_x == STEP_1N2W_X and step_y == STEP_1N2W_Y):
        return DIRS['valid']
    elif(step_x == STEP_2N1W_X and step_y == STEP_2N1W_Y):
        return DIRS['valid']
    else:
        return DIRS['undefined']


def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
    DIRS = rules.DIRS
    direction = kn_dir(srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    color = Match.color_of_piece(piece)

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(pin_dir != DIRS['undefined']):
        return False

    field = match.readfield(dstx, dsty)
    if(match.color_of_piece(field) == color):
        return False

    return True
