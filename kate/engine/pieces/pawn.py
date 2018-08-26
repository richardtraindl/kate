from .piece import *


class cPawn(cPiece):
    DIRS = { 'north' : 1,
             'south' : 2,
             'north-east' : 5,
             'south-west' : 6,
             'north-west' : 7,
             'south-east' : 8,
             '2north' : 9,
             '2south' : 10,
             'valid' : 13,
             'undefined' : 14 }

    REVERSE_DIRS = { DIRS['north'] : DIRS['south'],
                     DIRS['south'] : DIRS['north'],
                     DIRS['north-east'] : DIRS['south-west'],
                     DIRS['south-west'] : DIRS['north-east'],
                     DIRS['north-west'] : DIRS['south-east'],
                     DIRS['south-east'] : DIRS['north-west'],
                     DIRS['2north'] : DIRS['2south'],
                     DIRS['2south'] : DIRS['2north'],
                     DIRS['valid']  : DIRS['valid'],
                     DIRS['undefined']  : DIRS['undefined'] }

    STEP_1N_X = 0
    STEP_1N_Y = 1
    STEP_2N_X = 0
    STEP_2N_Y = 2
    STEP_1N1E_X = 1
    STEP_1N1E_Y = 1
    STEP_1N1W_X = -1
    STEP_1N1W_Y = 1
    STEP_1S_X = 0
    STEP_1S_Y = -1
    STEP_2S_X = 0
    STEP_2S_Y = -2
    STEP_1S1E_X = 1
    STEP_1S1E_Y = -1
    STEP_1S1W_X = -1
    STEP_1S1W_Y = -1
    
    A2_Y = 1
    A7_Y = 6

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)
        if(self.color == self.match.COLORS['white']):
            self.STEPS = [ [1, 1], [-1, 1] ]
            self.BACK_STEPS = [ [1, -1], [-1, -1] ]
        else:
            self.STEPS = [ [1, -1], [-1, -1] ]
            self.BACK_STEPS = [ [1, 1], [-1, 1] ]

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == cls.STEP_1N_X and step_y == cls.STEP_1N_Y):
            return cls.DIRS['north']
        elif(step_x == cls.STEP_2N_X and step_y == cls.STEP_2N_Y and srcy == cls.A2_Y):
            return cls.DIRS['2north']
        elif(step_x == cls.STEP_1N1E_X and step_y == cls.STEP_1N1E_Y):
            return cls.DIRS['north-east']
        elif(step_x == cls.STEP_1N1W_X and step_y == cls.STEP_1N1W_Y):
            return cls.DIRS['north-west']
        elif(step_x == cls.STEP_1S_X and step_y == cls.STEP_1S_Y):
            return cls.DIRS['south']
        elif(step_x == cls.STEP_2S_X and step_y == cls.STEP_2S_Y and srcy == cls.A7_Y):
            return cls.DIRS['2south']
        elif(step_x == cls.STEP_1S1E_X and step_y == cls.STEP_1S1E_Y):
            return cls.DIRS['south-east']
        elif(step_x == cls.STEP_1S1W_X and step_y == cls.STEP_1S1W_Y):
            return cls.DIRS['south-west']
        else:
            return cls.DIRS['undefined']

    #step_for_dir(direction):
        # not used for pawn

    def is_piece_trapped(self):
        return False # pawn cannot be trapped

    #is_piece_stuck_new(self):
        # works with inherited class

    #is_move_stuck(self, dstx, dsty)
        # works with inherited class

    def is_move_valid(self, dstx, dsty, prom_piece):
        move_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(move_dir == self.DIRS['undefined']):
            return False

        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos) #self.color, 

        dstpiece = self.match.readfield(dstx, dsty)

        if(self.color == self.match.COLORS['white']):
            # check pins
            if(move_dir == self.DIRS['north'] or move_dir == self.DIRS['2north']):
                if(pin_dir != self.DIRS['north'] and pin_dir != self.DIRS['south'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['north-west']):
                if(pin_dir != self.DIRS['north-west'] and pin_dir != self.DIRS['south-east'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['north-east']):
                if(pin_dir != self.DIRS['north-east'] and pin_dir != self.DIRS['south-west'] and pin_dir != self.DIRS['undefined']):
                    return False
            else:
                return False

            # check fields
            if(move_dir == self.DIRS['north'] and dstpiece != self.match.PIECES['blk']):
                return False
            elif(move_dir == self.DIRS['2north']):
                midpiece = self.match.readfield(dstx, self.ypos + self.STEP_1N_Y)
                if(midpiece != self.match.PIECES['blk'] or dstpiece != self.match.PIECES['blk']):
                    return False
            elif(move_dir == self.DIRS['north-west'] or move_dir == self.DIRS['north-east']):
                if(self.match.color_of_piece(dstpiece) != self.match.COLORS['black']):
                    return self.is_white_ep_move_ok(dstx, dsty)

            # check promotion
            if(dsty == 7 and prom_piece != self.match.PIECES['wQu'] and 
               prom_piece != self.match.PIECES['wRk'] and 
               prom_piece != self.match.PIECES['wBp'] and 
               prom_piece != self.match.PIECES['wKn']):
                return False
            elif(dsty < 7 and prom_piece != self.match.PIECES['blk']):
                return False
        else:
            # check pins
            if(move_dir == self.DIRS['south'] or move_dir == self.DIRS['2south']):
                if(pin_dir != self.DIRS['north'] and pin_dir != self.DIRS['south'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['south-east']):
                if(pin_dir != self.DIRS['north-west'] and pin_dir != self.DIRS['south-east'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['south-west']):
                if(pin_dir != self.DIRS['north-east'] and pin_dir != self.DIRS['south-west'] and pin_dir != self.DIRS['undefined']):
                    return False
            else:
                return False
            
            # check fields
            if(move_dir == self.DIRS['south'] and dstpiece != self.match.PIECES['blk']):
                return False
            elif(move_dir == self.DIRS['2south']):
                midpiece = self.match.readfield(dstx, self.ypos + self.STEP_1S_Y)
                if(midpiece != self.match.PIECES['blk'] or dstpiece != self.match.PIECES['blk']):
                    return False
            elif(move_dir == self.DIRS['south-east'] or move_dir == self.DIRS['south-west']):
                if(self.match.color_of_piece(dstpiece) != self.match.COLORS['white']):
                    return self.is_black_ep_move_ok(dstx, dsty)

            # check promotion
            if(dsty == 0 and prom_piece != self.match.PIECES['bQu'] and prom_piece != self.match.PIECES['bRk'] and prom_piece != self.match.PIECES['bBp'] and prom_piece != self.match.PIECES['bKn']):
                return False
            elif(dsty > 0 and prom_piece != self.match.PIECES['blk']):
                return False

        return True

    def do_move(self, dstx, dsty, prom_piece):
        move = cMove(self.match, 
                    self.match.movecnt + 1, 
                    cMove.TYPES['standard'],
                    self.xpos, 
                    self.ypos, 
                    dstx, 
                    dsty, 
                    None,
                    None,
                    self.match.PIECES['blk'], 
                    prom_piece, 
                    self.match.fifty_moves_count)

        srcpiece = self.match.readfield(move.srcx, move.srcy)
        dstpiece = self.match.readfield(move.dstx, move.dsty)

        if(prom_piece != self.match.PIECES['blk']):
            move.move_type = move.TYPES['promotion']
            move.captured_piece = dstpiece

            self.match.movecnt += 1 
            self.match.writefield(move.srcx, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, move.prom_piece)
            self.match.fifty_moves_count = 0
            self.match.score -= (self.match.SCORES[move.prom_piece] - self.match.SCORES[srcpiece])
            self.match.score += self.match.SCORES[dstpiece]
            self.match.move_list.append(move)
            return move
        elif(dstpiece == self.match.PIECES['blk'] and move.srcx != move.dstx):
            move.move_type = cMove.TYPES['en_passant']
            move.e_p_fieldx = move.dstx
            move.e_p_fieldy = move.srcy
            enemy = self.match.readfield(move.e_p_fieldx, move.e_p_fieldy)
            move.captured_piece = enemy

            self.match.movecnt += 1 
            self.match.writefield(move.srcx, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, srcpiece)
            self.match.fifty_moves_count = 0
            self.match.writefield(move.e_p_fieldx, move.e_p_fieldy, self.match.PIECES['blk'])
            self.match.score += self.match.SCORES[enemy]
            self.match.move_list.append(move)
            return move
        else:
            move.captured_piece = dstpiece

            self.match.movecnt += 1
            self.match.writefield(move.srcx, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, srcpiece)
            if(dstpiece != self.match.PIECES['blk']):
                self.match.fifty_moves_count = 0
                move.fifty_moves_count = self.match.fifty_moves_count
            else:
                self.match.fifty_moves_count += 1
                move.fifty_moves_count = self.match.fifty_moves_count

            self.match.score += self.match.SCORES[dstpiece]
            self.match.move_list.append(move)
            return move

    def undo_move(self, move):
        if(move.captured_piece == self.match.PIECES['wQu']):
            self.match.wQu_cnt += 1
        elif(move.captured_piece == self.match.PIECES['bQu']):
            self.match.bQu_cnt += 1
        elif(move.captured_piece == self.match.PIECES['wKn'] or move.captured_piece == self.match.PIECES['wBp'] or move.captured_piece == self.match.PIECES['wRk']):
            self.match.wOfficer_cnt += 1
        elif(move.captured_piece == self.match.PIECES['bKn'] or move.captured_piece == self.match.PIECES['bBp'] or move.captured_piece == self.match.PIECES['bRk']):
            self.match.bOfficer_cnt += 1

        self.match.movecnt -= 1
        self.match.fifty_moves_count = move.fifty_moves_count

        if(move.move_type == move.TYPES['standard']):
            piece = self.match.readfield(move.dstx, move.dsty)
            self.match.writefield(move.srcx, move.srcy, piece)
            self.match.writefield(move.dstx, move.dsty, move.captured_piece)
            self.match.score -= self.match.SCORES[move.captured_piece]
            return move
        elif(move.move_type == move.TYPES['promotion']):
            if(move.dsty == 7):
                piece = self.match.PIECES['wPw']
            else:
                piece = self.match.PIECES['bPw']
            self.match.writefield(move.srcx, move.srcy, piece)
            self.match.writefield(move.dstx, move.dsty, move.captured_piece)
            self.match.score += (self.match.SCORES[move.prom_piece] - self.match.SCORES[piece])
            self.match.score -= self.match.SCORES[move.captured_piece]
            return move
        elif(move.move_type == move.TYPES['en_passant']):
            piece = self.match.readfield(move.dstx, move.dsty)
            self.match.writefield(move.srcx, move.srcy, piece)
            self.match.writefield(move.dstx, move.dsty, match.PIECES['blk'])
            self.match.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
            self.match.score -= self.match.SCORES[move.captured_piece]
            return move

    def is_white_ep_move_ok(self, dstx, dsty):
        if(len(self.match.move_list) == 0):
            return False
        else:
            move = self.match.move_list[-1]

        dstpiece = self.match.readfield(dstx, dsty)
        opp_piece = self.match.readfield(move.dstx, move.dsty)
        if(dstpiece == self.match.PIECES['blk'] and opp_piece == self.match.PIECES['bPw'] and 
           move.srcy - move.dsty == 2 and move.dsty == self.ypos and move.dstx == dstx and 
           move.dsty - dsty == -1):
            return True
        else:
            return False

    def is_black_ep_move_ok(self, dstx, dsty):
        if(len(self.match.move_list) == 0):
            return False
        else:
            move = self.match.move_list[-1]

        dstpiece = self.match.readfield(dstx, dsty)
        opp_piece = self.match.readfield(move.dstx, move.dsty)
        if(dstpiece == self.match.PIECES['blk'] and opp_piece == self.match.PIECES['wPw'] and 
           move.srcy - move.dsty == -2 and move.dsty == self.ypos and move.dstx == dstx and 
           move.dsty - dsty == 1):
            return True
        else:
            return False
        
    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        from .. analyze_helper import field_touches_beyond

        opp_color = self.match.oppcolor_of_piece(self.piece)

        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(x1 == self.xpos and y1 == self.ypos):
                    continue

                piece = self.match.readfield(x1, y1)
            
                if(piece == self.match.PIECES['blk']):
                    continue

                cpawn = cPawn(self.match, dstx, dsty)
                if(self.is_move_stuck(x1, y1)):
                    continue

                if(self.match.color_of_piece(piece) == opp_color):
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    attacked.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, opp_color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###
                else:
                    if(piece == self.match.PIECES['blk'] or piece == self.match.PIECES['wKg'] or piece == self.match.PIECES['bKg']):
                        continue

                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    supported.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, self.color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###
                    
    def move_defends_forked_field(self, dstx, dsty):
        from .. analyze_helper import is_fork_field

        if(self.is_move_stuck(dstx, dsty)):
            return False

        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]

            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)

                if(piece == self.match.PIECES['blk'] or self.match.color_of_piece(piece) == self.color):
                    if(is_fork_field(self.match, self.color, x1, y1)):
                        #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                        #analyses.lst_fork_defended.append(cfork)
                        return True
        return False

    def move_controles_file(self, dstx, dsty):
        return False

    def is_running(self):
        if(self.color == self.match.COLORS['white']):
            stepx = 0
            stepy = 1
            opp_pawn = self.match.PIECES['bPw']
        else:
            stepx = 0
            stepy = -1
            opp_pawn = self.match.PIECES['wPw']

        STARTX = [0, 1, -1]
        for i in range(3):
            x1 = self.xpos + STARTX[i]
            y1 = self.ypos
            while(x1 != self.match.UNDEF_X and self.match.is_inbounds(x1, y1) ):
                x1, y1 = self.match.search(x1, y1, stepx, stepy)
                if(x1 != self.match.UNDEF_X):
                    piece = self.match.readfield(x1, y1)
                    if(piece == opp_pawn):
                        return False
        return True

    def score_attacks(self):
        from .. analyze_helper import list_all_field_touches

        score = 0

        opp_color = self.match.oppcolor_of_piece(self.piece)

        frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, self.xpos, self.ypos)
        if(len(frdlytouches) < len(enmytouches)):
            return score

        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(self.is_move_stuck(x1, y1)):
                    continue

                frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                #if(len(frdlytouches) < len(enmytouches)):
                    #continue

                piece = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(piece) == opp_color):
                    score += self.match.ATTACKED_SCORES[piece]

                    # extra score if attacked is pinned
                    enmy_pin = self.match.evaluate_pin_dir(x1, y1) #opp_color
                    if(enmy_pin != self.DIRS['undefined']):
                        score += self.match.ATTACKED_SCORES[piece]

                    if(self.match.is_soft_pin(x1, y1)):
                        score += self.match.ATTACKED_SCORES[piece]
        return score

    def score_supports(self):
        score = 0

        opp_color = self.match.oppcolor_of_piece(self.piece)

        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(self.is_move_stuck(x1, y1)):
                    continue

                supported = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(supported) == self.color):
                    if(self.match.is_field_touched(opp_color, x1, y1, 1)):
                        score += self.match.SUPPORTED_SCORES[supported]
        return score

# class end

