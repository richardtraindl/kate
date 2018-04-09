import time
from operator import attrgetter
from .match import *
from .move import *
from . import matchmove
from .openingmove import retrieve_move
from .analyze_move import *
from .analyze_position import *
from .helper import *
from .cvalues import *
from .rules import is_move_valid, RETURN_CODES, is_field_touched
from .pieces import pawn, rook, bishop, knight, queen, king
from .debug import prnt_attributes, token_to_text


def prnt_move(headmsg, move, tailmsg):
    if(move == None):
        print("no move.....")
    else:
        print(headmsg + 
            index_to_coord(move.srcx, move.srcy) + "-" +
            index_to_coord(move.dstx, move.dsty), end="")
        if(move.prom_piece != PIECES['blk']):
            print(" " + reverse_lookup(PIECES, move.prom_piece), end="")
        print(tailmsg, end="")


def prnt_moves(msg, moves):
    print(msg, end=" ")

    if(len(moves) == 0):
        print("no move.....")
    else:
        for move in moves:
            if(move):
                prnt_move("[", move, "] ")
            else:
                break
        print("")


def prnt_priorities(priomoves, priocnts):
    for priomove in priomoves:
        token = priomove.tokens[0]
        prnt_move("\n ", priomove.gmove, "")        
        print("piece:" + str(priomove.piece) + " token:" + hex(token) + 
               " " + reverse_lookup(PRIO, priomove.prio) + 
               " \ntoken: " + hex(token) + " " + token_to_text(token))

    for i in range(len(priocnts)):
        print(reverse_lookup(PRIO, i)  + ": " + str(priocnts[i]))


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    prom_piece = steps[dir_idx][step_idx][2]
    return stepx, stepy, prom_piece

class PrioMove:
    def __init__(self, gmove=None, piece=None, tokens=None, prio=None, prio_sec=None):
        self.gmove = gmove
        self.piece = piece
        self.tokens = tokens
        self.prio = prio
        self.prio_sec = prio_sec

def generate_moves(match):
    color = match.next_color()
    priomoves = []
    priocnts = [0] * len(PRIO)

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['blk'] or color != Match.color_of_piece(piece)):
                continue
            else:
                dir_idx = 0
                step_idx = 0
                if(piece == PIECES['wPw']):
                    if(y < 6):
                        steps = pawn.GEN_WSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_WPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['bPw']):
                    if(y > 1):
                        steps = pawn.GEN_BSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_BPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                    steps = rook.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                    steps = bishop.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                    steps = knight.GEN_STEPS
                    max_dir = 8
                    max_step = 1
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    steps = queen.GEN_STEPS
                    max_dir = 8
                    max_step = 7
                else:
                    steps = king.GEN_STEPS
                    max_dir = 10
                    max_step = 1

            for dir_idx in range(0, max_dir, 1):
                for step_idx in range(0, max_step, 1):
                    stepx, stepy, prom_piece = read_steps(steps, dir_idx, step_idx)
                    dstx = x + stepx
                    dsty = y + stepy
                    flag, errmsg = rules.is_move_valid(match, x, y, dstx, dsty, prom_piece)
                    if(flag):
                        gmove = GenMove(x, y, dstx, dsty, prom_piece)
                        tokens = analyze_move(match, gmove)
                        priomove = PrioMove(gmove, piece, tokens, PRIO['last'], PRIO['last'])
                        priomoves.append(priomove)
                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    if(match.next_color() == COLORS['white']):
        kg_attacked = rules.is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y, 0)
    else:
        kg_attacked = rules.is_field_touched(match, COLORS['white'], match.bKg_x, match.bKg_y, 0)

    if(kg_attacked):
        for priomove in priomoves:
            priomove.prio = PRIO['defend-check']

        priomoves.sort(key=attrgetter('prio'))

        for i in range(len(PRIO)):
            priocnts[i] = 0
        priocnts[0] = len(priomoves)
    else:
        rank_moves(match, priomoves)
        priomoves.sort(key=attrgetter('prio', 'prio_sec'))

        for priomove in priomoves:
            priocnts[priomove.prio] += 1

    return priomoves, priocnts


def rate(color, newscore, newmove, newcandidates, score, candidates):
    if( (color == COLORS["white"] and score >= newscore) or (color == COLORS["black"] and score <= newscore) ):
        return score
    else:
        candidates.clear()
        candidates.append(newmove)

        if(len(newcandidates) > 0):
            for newcandidate in newcandidates:
                if(newcandidate):
                    candidates.append(newcandidate)
                else:
                    break

        candidates.append(None)
        return newscore


def was_last_move_stormy(last_prio):
    if(last_prio == PRIO['promotion'] or
       last_prio == PRIO['capture-good-deal'] or
       last_prio == PRIO['attack-king-good-deal'] or 
       last_prio == PRIO['capture-bad-deal'] or       
       last_prio == PRIO['attack-king-bad-deal'] or
       last_prio == PRIO['attack-stormy']):
        return True
    else:
        return False

def select_maxcnt(match, depth, priomoves, priocnts, last_pmove):
    mvcnt = len(priomoves)
    prio_mvcnt1 = 0
    prio_mvcnt2 = 0
    prio_mvcnt3 = 0
    time_exceeded = False

    calc_time = time.time() - match.calc_time_start

    for i in range(PRIO_LIMES3 + 1):
        prio_mvcnt3 += priocnts[i]

    prio_mvcnt2 = prio_mvcnt3
    for i in range(PRIO_LIMES3 + 1, PRIO_LIMES2 + 1):
        prio_mvcnt2 += priocnts[i]

    prio_mvcnt1 = prio_mvcnt2
    for i in range(PRIO_LIMES2 + 1, PRIO_LIMES1 + 1):
        prio_mvcnt1 += priocnts[i]

    if(last_pmove):
        last_prio = last_pmove.prio
    else:
        last_prio = PRIO['last']

    if(match.level == LEVELS['blitz']):
        cnt = 8
        dpth = 2
        max_dpth = 8
        if(calc_time > 30):
            time_exceeded = True
    elif(match.level == LEVELS['low']):
        cnt = 10
        dpth = 3
        max_dpth = 10
        if(calc_time > 60):
            time_exceeded = True
    elif(match.level == LEVELS['medium']):
        cnt = 12
        dpth = 4
        max_dpth = 12
        if(calc_time > 90):
            time_exceeded = True
    else:
        cnt = 16
        dpth = 5
        max_dpth = 14
        if(calc_time > 120):
            time_exceeded = True

    if(is_endgame(match)):
        dpth += 2

    if(depth <= dpth):
        if(time_exceeded):
            return min(cnt, prio_mvcnt1)
        else:
            return max(cnt, prio_mvcnt1)
    elif(depth <= dpth + 3 and (was_last_move_stormy(last_prio) or is_stormy(match))):
        return prio_mvcnt2
    elif(depth <= max_dpth and was_last_move_stormy(last_prio)):
        return prio_mvcnt3
    else:
        return 0


def calc_max(match, depth, alpha, beta, last_pmove):
    color = match.next_color()
    candidates = []
    newcandidates = []
    maxscore = SCORES[PIECES['wKg']] * 2
    count = 0

    priomoves, priocnts = generate_moves(match)
    
    maxcnt = select_maxcnt(match, depth, priomoves, priocnts, last_pmove)

    if(depth == 1):
        prnt_priorities(priomoves, priocnts)
        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            return score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(priomoves)), candidates

    for priomove in priomoves:
        newmove = priomove.gmove

        count += 1

        if(depth == 1):
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, "")
            print("   " + reverse_lookup(PRIO, priomove.prio) + " | " + reverse_lookup(PRIO, priomove.prio_sec))

            token = priomove.tokens[0]
            print("token: " + hex(token) + " " + token_to_text(token))

        move = matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcandidates = calc_min(match, depth + 1, maxscore, beta, priomove) # , dbginfo

        if(match.movecnt <= 20):
            if(piece_movecnt(match, move) >= 3):
                if(color == COLORS['white']):
                    newscore += ATTACKED_SCORES[PIECES['bPw']]
                else:
                    newscore += ATTACKED_SCORES[PIECES['wPw']]

        score = rate(color, newscore, newmove, newcandidates, maxscore, candidates)

        matchmove.undo_move(match)

        if(depth == 1):
            prnt_move("\nCURR SEARCH: " + str(newscore).rjust(8, " ") + " [", newmove, "]")
            prnt_moves("", newcandidates)

            prnt_moves("CANDIDATES:  " + str(score).rjust(8, " "), candidates)
            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

            calc_time = time.time() - match.calc_time_start
            if(match.level == LEVELS['blitz']):
                if(calc_time > 30):
                    maxcnt = 8
            elif(match.level == LEVELS['low']):
                if(calc_time > 60):
                    maxcnt = 10
            elif(match.level == LEVELS['medium']):
                if(calc_time > 90):
                    maxcnt = 12
            else:
                if(calc_time > 120):
                    maxcnt = 16

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, candidates

        if(count >= maxcnt):
            return maxscore, candidates

    return maxscore, candidates


def calc_min(match, depth, alpha, beta, last_pmove):
    color = match.next_color()
    candidates = []
    newcandidates = []
    minscore = SCORES[PIECES['bKg']] * 2
    count = 0

    priomoves, priocnts = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, priomoves, priocnts, last_pmove)

    if(depth == 1):
        prnt_priorities(priomoves, priocnts)
        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            return score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(priomoves)), candidates

    for priomove in priomoves:
        newmove = priomove.gmove

        count += 1

        if(depth == 1):
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, "")
            print("   " + reverse_lookup(PRIO, priomove.prio) + " | " + reverse_lookup(PRIO, priomove.prio_sec))

            token = priomove.tokens[0]
            print("token: " + hex(token) + " " + token_to_text(token))

        move = matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcandidates = calc_max(match, depth + 1, alpha, minscore, priomove) # , dbginfo

        if(match.movecnt <= 20):
            if(piece_movecnt(match, move) >= 3):
                if(color == COLORS['white']):
                    newscore += ATTACKED_SCORES[PIECES['bPw']]
                else:
                    newscore += ATTACKED_SCORES[PIECES['wPw']]

        score = rate(color, newscore, newmove, newcandidates, minscore, candidates)

        matchmove.undo_move(match)
        
        if(depth == 1):
            prnt_move("\nCURR SEARCH: " + str(newscore).rjust(8, " ") + " [", newmove, "]")
            prnt_moves("", newcandidates)

            prnt_moves("CANDIDATES:  " + str(score).rjust(8, " "), candidates)
            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

            calc_time = time.time() - match.calc_time_start
            if(match.level == LEVELS['blitz']):
                if(calc_time > 30):
                    maxcnt = 8
            elif(match.level == LEVELS['low']):
                if(calc_time > 60):
                    maxcnt = 10
            elif(match.level == LEVELS['medium']):
                if(calc_time > 90):
                    maxcnt = 12
            else:
                if(calc_time > 120):
                    maxcnt = 16

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, candidates

        if(count >= maxcnt):
            return minscore, candidates

    return minscore, candidates


def calc_move(match):
    prnt_attributes(match, "\n")

    candidates = []

    match.calc_time_start = time.time()

    gmove = retrieve_move(match)
    if(gmove):
        candidates.append(gmove)
        score = match.score
    elif(match.next_color() == COLORS['white']):
        score, candidates = calc_max(match, 1, SCORES[PIECES['bKg']] * 2, SCORES[PIECES['bKg']] * 2, None) # , dbginfo
    else:
        score, candidates = calc_min(match, 1, SCORES[PIECES['wKg']] * 2, SCORES[PIECES['bKg']] * 2, None) # , dbginfo
    
    calc_time = time.time() - match.calc_time_start
    if(match.next_color() == COLORS['white']):
        match.elapsed_time_white += calc_time
    else:
        match.elapsed_time_black += calc_time

    msg = "result: " + str(score) + " match.id: " + str(match.id) + " "
    prnt_moves(msg, candidates)
    prnt_fmttime("\ncalc-time: ", calc_time)
    prnt_attributes(match, "\n")
    return candidates

