from kate.models import Match, Move
from kate.modules import helper, rules, openings, calc_helper, debug
import random, threading, copy, time 



RK_STEPS = [ [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
          [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
          [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
          [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]] ]


BP_STEPS = [ [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
             [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
             [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
             [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]] ]


QU_STEPS = [ [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
             [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
             [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
             [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
             [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
             [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
             [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
             [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]] ]


KN_STEPS = [ [[1, 2]],
             [[2, 1]],
             [[2, -1]], 
             [[1, -2]],
             [[-1, -2]],
             [[-2, -1]],
             [[-2, 1]],
             [[-1, 2]] ]


KG_STEPS = [ [[0, 1]],
             [[1, 1]],
             [[1, 0]], 
             [[1, -1]],
             [[0, -1]], 
             [[-1, -1]],
             [[-1, 0]],
             [[-1, 1]],
             [[2, 0]],
             [[-2, 0]] ]


WPW_STEPS = [ [[0, 1]],
              [[0, 2]],
              [[1, 1]], 
              [[-1, 1]] ]

WPROM_STEPS = [ [[0, 1, Match.PIECES['wQu']], [1, 1, Match.PIECES['wQu']], [-1, 1, Match.PIECES['wQu']], [0, 1, Match.PIECES['wRk']]],
                [[1, 1, Match.PIECES['wRk']], [-1, 1, Match.PIECES['wRk']], [0, 1, Match.PIECES['wBp']], [1, 1, Match.PIECES['wBp']]],
                [[-1, 1, Match.PIECES['wBp']], [0, 1, Match.PIECES['wKn']], [1, 1, Match.PIECES['wKn']], [-1, 1, Match.PIECES['wKn']]] ]


BPW_STEPS = [ [[0, -1]],
              [[0, -2]],
              [[-1, -1]], 
              [[1, -1]] ]

BPROM_STEPS = [ [[0, -1, Match.PIECES['bQu']], [0, -1, Match.PIECES['bRk']], [0, -1, Match.PIECES['bBp']], [0, -1, Match.PIECES['bKn']]],
                [[1, -1, Match.PIECES['bQu']], [1, -1, Match.PIECES['bRk']], [1, -1, Match.PIECES['bBp']], [1, -1, Match.PIECES['bKn']]],
                [[-1, -1, Match.PIECES['bQu']], [-1, -1, Match.PIECES['bRk']], [-1, -1, Match.PIECES['bBp']], [-1, -1, Match.PIECES['bKn']]] ]


MOVEFILTER = {
                'ALL' : 0,
                'LARGE' : 1,
                'SMALL' : 2 }


def prnt_move(msg, move):
    if(move == None):
        print("no move.....")
    else:
        print(msg + 
            Match.index_to_koord(move.srcx, move.srcy) + " " +
            Match.index_to_koord(move.dstx, move.dsty) + " " +
            helper.reverse_lookup(Match.PIECES, move.prom_piece), end="")


class GenMove(object):
    def __init__(self, srcx=None, srcy=None, dstx=None, dsty=None, prom_piece=None):
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.prom_piece = prom_piece


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    if(len(steps[dir_idx][step_idx]) == 3):
        prom_piece = steps[dir_idx][step_idx][2]
    else:
        prom_piece = Match.PIECES['blk']
    return stepx, stepy, prom_piece


def generate_moves(match, gmoves, movefilter):
    color = match.next_color()
    kg_moves = []
    qu_moves = []
    rk_moves = []
    bp_moves = []
    kn_moves = []
    pw_moves = []

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == Match.PIECES['blk'] or color != Match.color_of_piece(piece)):
                continue
            else:
                dir_idx = 0
                step_idx = 0
                if(piece == Match.PIECES['wPw']):
                    moves = pw_moves
                    if(y < 6):
                        steps = WPW_STEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = WPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == Match.PIECES['bPw']):
                    moves = pw_moves
                    if(y > 1):
                        steps = BPW_STEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = BPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
                    moves = rk_moves
                    steps = RK_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
                    moves = bp_moves
                    steps = BP_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
                    moves = kn_moves
                    steps = KN_STEPS
                    max_dir = 8
                    max_step = 1
                elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
                    moves = qu_moves
                    steps = QU_STEPS
                    max_dir = 8
                    max_step = 7
                else:
                    moves = kg_moves
                    steps = KG_STEPS
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
                        if(movefilter == MOVEFILTER['ALL']):
                            moves.append(gmove)
                        elif(movefilter == MOVEFILTER['LARGE']):
                            capture = calc_helper.is_capture(match, gmove)
                            promotion = calc_helper.is_promotion(match, gmove)
                            castling = calc_helper.is_castling(match, gmove)
                            attack = calc_helper.does_attack(match, gmove)
                            support = calc_helper.does_support_attacked(match, gmove)
                            attacked_king = calc_helper.is_king_attacked(match, gmove)
                            # escape for attacked pieces rules.
                            if(capture or promotion or castling or attack or support or attacked_king):
                                moves.append(gmove)
                        else: # MOVEFILTER['SMALL']
                            capture = calc_helper.is_capture(match, gmove)
                            promotion = calc_helper.is_promotion(match, gmove)
                            castling = calc_helper.is_castling(match, gmove)
                            attacked_king = calc_helper.is_king_attacked(match, gmove)
                            if(capture or promotion or castling or attacked_king):
                                moves.append(gmove)
                    elif(errmsg != rules.ERROR_CODES['king-error']):
                        break
    gmoves.extend(kn_moves)
    gmoves.extend(bp_moves)
    gmoves.extend(rk_moves)
    gmoves.extend(pw_moves)
    gmoves.extend(kg_moves)
    gmoves.extend(qu_moves)


class immanuelsThread(threading.Thread):
    def __init__(self, name, match):
        threading.Thread.__init__(self)
        self.name = name
        self.match = copy.deepcopy(match)
        self.candidate_srcx = None
        self.candidate_srcy = None
        self.candidate_dstx = None
        self.candidate_dsty = None
        self.candidate_prom_piece = None

        Match.remove_outdated_threads(match)
        Match.add_thread(self)
        print("match.id: " + str(match.id))

    def run(self):
        print("Starting " + str(self.name))
        move = Move.objects.filter(match_id=self.match.id).order_by("count").last()
        if(move != None):
            self.match.move_list.append(move)

        if(self.match.level == Match.LEVEL['low']):
            maxdepth = 1
        elif(self.match.level == Match.LEVEL['medium']):
            maxdepth = 2
        elif(self.match.level == Match.LEVEL['high']):
            maxdepth = 3
        else:
            maxdepth = 4 # professional

        gmove = calc_move(self.match, maxdepth)
        if(gmove != None):
            curr_match = Match.objects.get(id=self.match.id)
            if(curr_match.count == self.match.count and Match.does_thread_exist(self)):
                move = self.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
                move.save()
                self.match.save()
                print("move saved")
            else:
                print("thread outdated - move dropped")
        return gmove

    def populate_candiate(self, gmove):
        if(gmove):
            self.candidate_srcx = gmove.srcx
            self.candidate_srcy = gmove.srcy
            self.candidate_dstx = gmove.dstx
            self.candidate_dsty = gmove.dsty
            self.candidate_prom_piece = gmove.prom_piece


def rate(color, gmove, newgmove, score, newscore):
    if(color == Match.COLORS["white"] and score < newscore):
        return newscore, newgmove
    elif(color == Match.COLORS["black"] and score > newscore):
        return newscore, newgmove
    else:
        return score, gmove


def calc_max(match, maxdepth, depth, alpha, beta):
    gmove = None
    color = match.next_color()
    newscore = None
    maxscore = -200000
    oldscore = 0
    gmoves = []

    if(match.next_color() == Match.COLORS['white']):
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['white'], match.bKg_x, match.bKg_y)

    if(kg_attacked or depth <= maxdepth):
        movefilter = MOVEFILTER['ALL']
    elif(depth <= maxdepth + 1):
        movefilter = MOVEFILTER['LARGE']
    else:
        movefilter = MOVEFILTER['SMALL']

    generate_moves(match, gmoves, movefilter)
    for newgmove in gmoves:
        oldscore = match.score

        move = match.do_move(newgmove.srcx, newgmove.srcy, newgmove.dstx, newgmove.dsty, newgmove.prom_piece)

        if(depth == 1):
            msg = "\nmatch.id:" + str(match.id) + " calculate "
            prnt_move(msg, newgmove)
            if(gmove):
                prnt_move(" CANDIDATE ", gmove)
                print(" score: " + str(newscore))
                thread = Match.get_active_thread(match)
                if(thread and newscore):
                    thread.populate_candiate(gmove)

        if(depth <= maxdepth + 2):
            newscore = calc_min(match, maxdepth, depth + 1, maxscore, beta)[0]
        else:
            newscore = match.score + calc_helper.evaluate_position(match)

        newscore, gmove = rate(color, gmove, newgmove, maxscore, newscore)
        match.undo_move(True)
        if(newscore > maxscore):
            maxscore = newscore
            if(maxscore >= beta):
                break

    if(len(gmoves) == 0):
        status = rules.game_status(match)
        if(status == Match.STATUS['winner_black']):
            newscore = Match.SCORES[Match.PIECES['wKg']]
        elif(status == Match.STATUS['winner_white']):
            newscore = Match.SCORES[Match.PIECES['bKg']]
        elif(status == Match.STATUS['draw']):
            newscore = Match.SCORES[Match.PIECES['blk']]
        else:
            newscore = match.score

        if(depth == 1):
            msg = "\nmatch.id:" + str(match.id) + " CANDIDATE "
            prnt_move(msg, gmove)
            print(" score: " + str(newscore))
            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_candiate(gmove)

        return newscore, gmove

    return maxscore, gmove


def calc_min(match, maxdepth, depth, alpha, beta):
    gmove = None
    color = match.next_color()
    newscore = None
    minscore = 200000
    oldscore = 0
    gmoves = []

    if(match.next_color() == Match.COLORS['white']):
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['white'], match.bKg_x, match.bKg_y)

    if(kg_attacked or depth <= maxdepth):
        movefilter = MOVEFILTER['ALL']
    elif(depth <= maxdepth + 1):
        movefilter = MOVEFILTER['LARGE']
    else:
        movefilter = MOVEFILTER['SMALL']

    generate_moves(match, gmoves, movefilter)
    for newgmove in gmoves:
        oldscore = match.score

        move = match.do_move(newgmove.srcx, newgmove.srcy, newgmove.dstx, newgmove.dsty, newgmove.prom_piece)

        if(depth == 1):
            msg = "\nmatch.id:" + str(match.id) + " calculate "
            prnt_move(msg, newgmove)
            if(gmove):
                prnt_move(" CANDIDATE ", gmove)
                print(" score: " + str(newscore))
                thread = Match.get_active_thread(match)
                if(thread and newscore):
                    thread.populate_candiate(gmove)

        if(depth <= maxdepth + 2):
            newscore = calc_max(match, maxdepth, depth + 1, alpha, minscore)[0]
        else:
            newscore = match.score + calc_helper.evaluate_position(match)

        newscore, gmove = rate(color, gmove, newgmove, minscore, newscore)
        match.undo_move(True)
        if(newscore < minscore):
            minscore = newscore
            if(minscore <= alpha):
                break

    if(len(gmoves) == 0):
        status = rules.game_status(match)
        if(status == Match.STATUS['winner_black']):
            newscore = Match.SCORES[Match.PIECES['wKg']]
        elif(status == Match.STATUS['winner_white']):
            newscore = Match.SCORES[Match.PIECES['bKg']]
        elif(status == Match.STATUS['draw']):
            newscore = Match.SCORES[Match.PIECES['blk']]
        else:
            newscore = match.score

        if(depth == 1):
            msg = "\nmatch.id:" + str(match.id) + " CANDIDATE "
            prnt_move(msg, gmove)
            print(" score: " + str(newscore))
            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_candiate(gmove)

        return newscore, gmove

    return minscore, gmove


def calc_move(match, maxdepth):
    gmove = openings.retrieve_move(match)

    if(gmove):
        score = match.score
    elif(match.next_color() == Match.COLORS['white']):
        score, gmove = calc_max(match, maxdepth, 1, -200000, 200000)
    else:
        score, gmove = calc_min(match, maxdepth, 1, -200000, 200000)

    if(gmove != None):
        msg = "\nresult: " + str(score) + " match.id: " + str(match.id) + " "
        prnt_move(msg, gmove)
        print("")
    else:
        print("no results found!!!" + str(score))
    return gmove


def thread_do_move(match):
    thread = immanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
    thread.start()


