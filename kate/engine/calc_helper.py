from kate.engine import move, rules, debug, helper
from kate.engine.pieces import pawn
from kate.engine.match import *


SCORES = { 
        PIECES['blk'] : 0,
        PIECES['wKg'] : -20000,
        PIECES['wPw'] : -100,
        PIECES['wRk'] : -500,
        PIECES['wKn'] : -336,
        PIECES['wBp'] : -340,
        PIECES['wQu'] : -950,
        PIECES['bKg'] : 20000,
        PIECES['bPw'] : 100,
        PIECES['bRk'] : 500,
        PIECES['bKn'] : 336,
        PIECES['bBp'] : 340,
        PIECES['bQu'] : 950 }

REVERSED_SCORES = {
        PIECES['blk'] : PIECES['blk'],
        PIECES['wKg'] : PIECES['bKg'],
        PIECES['wPw'] : PIECES['bPw'],
        PIECES['wRk'] : PIECES['bRk'] ,
        PIECES['wKn'] : PIECES['bKn'],
        PIECES['wBp'] : PIECES['bBp'],
        PIECES['wQu'] : PIECES['bQu'],
        PIECES['bKg'] : PIECES['wKg'],
        PIECES['bPw'] : PIECES['wPw'],
        PIECES['bRk'] : PIECES['wRk'],
        PIECES['bKn'] : PIECES['wKn'],
        PIECES['bBp'] : PIECES['wBp'],
        PIECES['bQu'] : PIECES['wQu'] }

ATTACKED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : -10,
        PIECES['wPw'] : -1,
        PIECES['wRk'] : -5,
        PIECES['wKn'] : -4,
        PIECES['wBp'] : -4,
        PIECES['wQu'] : -7,
        PIECES['bKg'] : 10,
        PIECES['bPw'] : 1,
        PIECES['bRk'] : 5,
        PIECES['bKn'] : 4,
        PIECES['bBp'] : 4,
        PIECES['bQu'] : 7 }

SUPPORTED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : 10,
        PIECES['wPw'] : 1,
        PIECES['wRk'] : 5,
        PIECES['wKn'] : 4,
        PIECES['wBp'] : 4,
        PIECES['wQu'] : 7,
        PIECES['bKg'] : -10,
        PIECES['bPw'] : -1,
        PIECES['bRk'] : -5,
        PIECES['bKn'] : -4,
        PIECES['bBp'] : -4,
        PIECES['bQu'] : -7 }

PIECES_RANK = {
        PIECES['blk'] : 0,
        PIECES['wPw'] : 1,
        PIECES['bPw'] : 1,
        PIECES['wKn'] : 2,
        PIECES['bKn'] : 2,
        PIECES['wBp'] : 2,
        PIECES['bBp'] : 2,
        PIECES['wRk'] : 4,
        PIECES['bRk'] : 4,
        PIECES['wQu'] : 5,
        PIECES['bQu'] : 5,
        PIECES['wKg'] : 6,
        PIECES['bKg'] : 6 }

PRIO = {
    'prio1' : 1,
    'prio2' : 2,
    'prio3' : 3,
    'prio4' : 4,
    'prio5' : 5,
    'prio6' : 6,
    'priolast' : 7,
    'undefinded' : 10 }

"""
def analyse(match):
    analyses = []
    qu_analyses = []
    rk_analyses = []
    bp_analyses = []
    kn_analyses = []
    pw_analyses = []
    
    color = match.next_color()
    opp_color = Match.REVERSED_COLORS[color]

    for y1 in range(8):
        for x1 in range(8):
            piece = match.readfield(x1, y1)
            if(color == Match.color_of_piece(piece)):
                if(piece == Match.PIECES['wPw'] or Match.PIECES['bPw']):
                    if( rules.is_field_touched(match, opp_color, x1, y1) ):
                        pw_analyses.append("pw")
                elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
                    if( rules.is_field_touched(match, opp_color, x1, y1) ):
                        rk_analyses.append("rk")
                elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
                    if( rules.is_field_touched(match, opp_color, x1, y1) ):
                        bp_analyses.append("bp")
                elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
                    if( rules.is_field_touched(match, opp_color, x1, y1) ):
                        kn_analyses.append("kn")
                elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
                    if( rules.is_field_touched(match, opp_color, x1, y1) ):
                        qu_analyses.append("qu")
                else:
                    if( rules.is_field_touched(match, opp_color, x1, y1) ):
                        analyses.append("kg")

    analyses.extend(qu_analyses)
    analyses.extend(rk_analyses)
    analyses.extend(bp_analyses)
    analyses.extend(kn_analyses)
    analyses.extend(pw_manalyses)
    return analyses
"""


def is_capture(match, move):
    piece = match.readfield(move.srcx, move.srcy)

    dstpiece = match.readfield(move.dstx, move.dsty)

    if(dstpiece != PIECES['blk']):
        if(PIECES_RANK[dstpiece] >= PIECES_RANK[piece]):
            return True, PRIO['prio1']
        else:
            match.writefield(move.srcx, move.srcy, PIECES['blk'])
            touched = rules.is_field_touched(match, Match.color_of_piece(dstpiece), move.dstx, move.dsty)
            match.writefield(move.srcx, move.srcy, piece)        
            if(touched):
                return True, PRIO['prio2']
            else:
                return True, PRIO['prio1']
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and move.srcx != move.dstx ):
        return True, PRIO['prio1']
    else:
        return False, PRIO['undefinded']


def is_promotion(match, move):
    if(move.prom_piece == PIECES['blk']):
        return False, PRIO['undefinded']
    else:
        return True, PRIO['prio1']


def is_castling(match, move):
    piece = match.readfield(move.srcx, move.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            return True, PRIO['prio1']

    return False, PRIO['undefinded']


def does_attack(match, move):
    return rules.does_attack(match, move.srcx, move.srcy, move.dstx, move.dsty)


def does_support_attacked(match, move):
    return rules.does_support_attacked(match, move.srcx, move.srcy, move.dstx, move.dsty)


def does_attacked_flee(match, move):
    return False, PRIO['undefinded']
    piece = match.readfield(move.srcx, move.srcy)
    
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    touches = rules.list_field_touches(match, opp_color, move.srcx, move.srcy)
    if(len(touches) > 0):
        match.writefield(move.srcx, move.srcy, Match.PIECES['blk'])
        newtouches = rules.list_field_touches(match, opp_color, move.dstx, move.dsty)
        match.writefield(move.srcx, move.srcy, piece)
        if(len(newtouches) < len(touches)):
            return True, PRIO['prio1']
        else:
            return True, PRIO['prio2']
    else:
        return False, PRIO['undefinded']


def is_endgame_move(match, move):
    if(match.count > 60):
        if(pawn.is_running(match, move)):
            return True, PRIO['prio2']
        else:
            piece = match.readfield(move.srcx, move.srcy)
            if(piece == PIECES['wPw'] or piece == PIECES['bPw'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                return True, PRIO['prio3']
            else:
                return False, PRIO['undefinded']
    else:
        return False, PRIO['undefinded']


"""
def is_king_attacked(match, move):
    return rules.is_king_attacked(match, move.srcx, move.srcy)
"""


"""
def pieces_attacked(match, color):
    if(color == Match.COLORS['white']):
        opp_color = Match.COLORS['black']
    else:
        opp_color = Match.COLORS['white']
    
    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == opp_color):
                if(rules.is_field_touched(match, opp_color, x, y)):
                    return True
            else:
                continue

    return False
"""


def evaluate_contacts(match):
    supporter = 0
    attacked = 0

    color = match.next_color()

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == COLORS['undefined']):
                continue

            supporter += rules.score_supports_of_attacked(match, x, y)
            attacked += rules.score_attacks(match, x, y)

    return (supporter + attacked)


def evaluate_piece_moves(match, srcx, srcy):
    color = match.next_color()
    piece = match.readfield(srcx, srcy)
    movecnt = 0

    if(Match.color_of_piece(piece) != color):
        return movecnt
        
    if(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 8
        stepcnt = 7
        value = 2
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
        dircnt = 4
        stepcnt = 7
        value = 4
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        dirs = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 4
        stepcnt = 7
        value = 6
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        dirs =  [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
        dircnt = 8
        stepcnt = 1
        value = 6
    else:
        return movecnt

    for j in range(dircnt):
        stepx = dirs[j][0]
        stepy = dirs[j][1]
        dstx = srcx
        dsty = srcy
        for i in range(stepcnt):
            dstx += stepx
            dsty += stepy
            flag,errcode = rules.is_move_valid(match, srcx, srcy, dstx, dsty, PIECES['blk'])
            if(flag):
                movecnt += value
            elif(errcode == rules.RETURN_CODES['out-of-bounds']):
                break

    return (movecnt)


def evaluate_movecnt(match):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            movecnt += evaluate_piece_moves(match, x1, y1)

    if(match.next_color() == COLORS['white']):
        return movecnt
    else:
        return (movecnt * -1)


def evaluate_developments(match):
    if(match.wKg_first_movecnt > 0 and (match.wRk_a1_first_movecnt > 0 or match.wRk_h1_first_movecnt > 0) ):
        developed_whites = 20
    else:
        developed_whites = 0

    if(match.bKg_first_movecnt > 0 and (match.bRk_a8_first_movecnt > 0 or match.bRk_h8_first_movecnt > 0) ):
        developed_blacks = -20
    else:
        developed_blacks = 0

    return developed_whites + developed_blacks


def evaluate_endgame(match):
    running = 0

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['wPw']):
                if(pawn.is_running):
                    running += REVERSED_SCORES[piece] // 2
                    if(y >= 4):
                        running += REVERSED_SCORES[piece]
            elif(piece == PIECES['bPw']):
                if(pawn.is_running):
                    running += REVERSED_SCORES[piece] // 2
                    if(y <= 3):
                        running += REVERSED_SCORES[piece]

    return running


def evaluate_position(match, movecnt):    
    if(movecnt == 0):
        status = rules.game_status(match)
        if(status == STATUS['winner_black']):
            return ( SCORES[PIECES['wKg']] + match.count )
        elif(status == STATUS['winner_white']):
            return ( SCORES[PIECES['bKg']] - match.count )
        else:   # Match.STATUS['draw']):
            return SCORES[PIECES['blk']]
    else:  
        value = match.score
        
        value += evaluate_contacts(match)

        if(match.count < 30):
            value += evaluate_movecnt(match)
            value += evaluate_developments(match)

        if(match.count > 40):
            value += evaluate_endgame(match)

        return value


