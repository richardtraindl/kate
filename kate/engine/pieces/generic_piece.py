from .. match import *
#from .. import rules
from .. cvalues import *


def is_piece_stuck(match, srcx, srcy):
    piece = match.readfield(srcx, srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return pawn.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return knight.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        return bishop.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        return rook.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        return bishop.is_piece_stuck(match, srcx, srcy) or rook.is_piece_stuck(match, srcx, srcy)
    else:
        return king.is_piece_stuck(match, srcx, srcy)


def count_contacts(contacts):
    pw_cnt = 0
    kn_cnt = 0
    bp_cnt = 0
    rk_cnt = 0
    qu_cnt = 0
    kg_cnt = 0

    for contact in contacts:
        piece = contact.piece

        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            pw_cnt += 1
        elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
            rk_cnt += 1
        elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
            bp_cnt += 1
        elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
            kn_cnt += 1
        elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
            qu_cnt += 1
        elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            kg_cnt += 1

    return pw_cnt, kn_cnt, bp_cnt, rk_cnt, qu_cnt, kg_cnt


def contacts_to_token(frdlycontacts, enmycontacts, mode):
    token = 0x0

    frdl_pw_cnt, frdl_kn_cnt, frdl_bp_cnt, frdl_rk_cnt, frdl_qu_cnt, frdl_kg_cnt = count_contacts(frdlycontacts)
    enmy_pw_cnt, enmy_kn_cnt, enmy_bp_cnt, enmy_rk_cnt, enmy_qu_cnt, enmy_kg_cnt = count_contacts(enmycontacts)

    if(mode == "SRCFIELDTOUCHES"):
        if(frdl_pw_cnt > 0):
            token = token | SRCFLD_IS_FRDL_TOU_BY_PW
        if(frdl_kn_cnt > 0):
            token = token | SRCFLD_IS_FRDL_TOU_BY_KN
        if(frdl_bp_cnt > 0):
            token = token | SRCFLD_IS_FRDL_TOU_BY_BP
        if(frdl_rk_cnt > 0):
            token = token | SRCFLD_IS_FRDL_TOU_BY_RK
        if(frdl_qu_cnt > 0):
            token = token | SRCFLD_IS_FRDL_TOU_BY_QU
        if(frdl_kg_cnt > 0):
            token = token | SRCFLD_IS_FRDL_TOU_BY_KG
        
        if(enmy_pw_cnt > 0):
            token = token | SRCFLD_IS_ENM_TOU_BY_PW
        if(enmy_kn_cnt > 0):
            token = token | SRCFLD_IS_ENM_TOU_BY_KN
        if(enmy_bp_cnt > 0):
            token = token | SRCFLD_IS_ENM_TOU_BY_BP
        if(enmy_rk_cnt > 0):
            token = token | SRCFLD_IS_ENM_TOU_BY_RK
        if(enmy_qu_cnt > 0):
            token = token | SRCFLD_IS_ENM_TOU_BY_QU
        if(enmy_kg_cnt > 0):
            token = token | SRCFLD_IS_ENM_TOU_BY_KG
    elif(mode == "DSTFIELDTOUCHES"):
        if(frdl_pw_cnt > 0):
            token = token | DSTFLD_IS_FRDL_TOU_BY_PW
        if(frdl_kn_cnt > 0):
            token = token | DSTFLD_IS_FRDL_TOU_BY_KN
        if(frdl_bp_cnt > 0):
            token = token | DSTFLD_IS_FRDL_TOU_BY_BP
        if(frdl_rk_cnt > 0):
            token = token | DSTFLD_IS_FRDL_TOU_BY_RK
        if(frdl_qu_cnt > 0):
            token = token | DSTFLD_IS_FRDL_TOU_BY_QU
        if(frdl_kg_cnt > 0):
            token = token | DSTFLD_IS_FRDL_TOU_BY_KG

        if(enmy_pw_cnt > 0):
            token = token | DSTFLD_IS_ENM_TOU_BY_PW
        if(enmy_kn_cnt > 0):
            token = token | DSTFLD_IS_ENM_TOU_BY_KN
        if(enmy_bp_cnt > 0):
            token = token | DSTFLD_IS_ENM_TOU_BY_BP
        if(enmy_rk_cnt > 0):
            token = token | DSTFLD_IS_ENM_TOU_BY_RK
        if(enmy_qu_cnt > 0):
            token = token | DSTFLD_IS_ENM_TOU_BY_QU
        if(enmy_kg_cnt > 0):
            token = token | DSTFLD_IS_ENM_TOU_BY_KG

    return token


class cTouch:
    def __init__(self, piece, fieldx, fieldy):
        self.piece = piece
        self.fieldx = fieldx
        self.fieldy = fieldy


class cTouchBeyond:
    def __init__(self, srcx, srcy, dstx, dsty, piece, fieldx, fieldy):
        self.agent_srcx = srcx
        self.agent_srcy = srcy
        self.agent_dstx = dstx
        self.agent_dsty = dsty        
        self.piece = piece
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.attacker_beyond = []
        self.supporter_beyond = []


class cFork:
    def __init__(self, srcx, srcy, dstx, dsty, forkx, forky):
        self.agent_srcx = srcx
        self.agent_srcy = srcy
        self.agent_dstx = dstx
        self.agent_dsty = dsty        
        self.forkx = forkx
        self.forky = forky

