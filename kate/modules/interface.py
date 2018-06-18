import random, threading, copy, time
import django_rq
from rq import Queue
from tasks import job_calc_and_do_move
from django.conf import settings
from .. models import Match as ModelMatch, Move as ModelMove
from .. engine.match import *
from .. engine.move import *
from .. engine import matchmove, rules, calc



MAP_DIR = { 'model-to-engine' : 0, 'engine-to-model' : 1 }


def map_matches(src, dst, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        moves = ModelMove.objects.filter(match_id=src.id).order_by("count")
        if(len(moves) > 0):
            for move in moves:
                dst.move_list.append(move)

    dst.id = src.id
    dst.status = src.status
    dst.level = src.level
    dst.begin = src.begin
    dst.time_start = src.time_start
    dst.white_player_name = src.white_player_name
    dst.white_player_is_human = src.white_player_is_human
    dst.white_elapsed_seconds = src.white_elapsed_seconds
    dst.black_player_name = src.black_player_name
    dst.black_player_is_human = src.black_player_is_human
    dst.black_elapsed_seconds = src.black_elapsed_seconds

    for y in range(8):
        for x in range(8):
            piece = src.readfield(x, y)
            dst.writefield(x, y, piece)

    if(map_dir == MAP_DIR['model-to-engine']):
        dst.update_attributes()


def map_moves(src, dst, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        dst.id = src.id
        dst.match = src.match

    dst.count = src.count
    dst.move_type = src.move_type
    dst.srcx = src.srcx
    dst.srcy = src.srcy
    dst.dstx = src.dstx
    dst.dsty = src.dsty
    dst.e_p_fieldx = src.e_p_fieldx
    dst.e_p_fieldy = src.e_p_fieldy
    dst.captured_piece = src.captured_piece
    dst.prom_piece = src.prom_piece
    dst.fifty_moves_count = src.fifty_moves_count


def status(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return rules.status(match)


def is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece)


def movecnt(modelmatch):
    moves = ModelMove.objects.filter(match_id=modelmatch.id)
    return len(moves)


def is_next_color_human(modelmatch):
    moves = ModelMove.objects.filter(match_id=modelmatch.id)
    if(len(moves) % 2 == 0):
        return modelmatch.white_player_is_human
    else:
        return modelmatch.black_player_is_human


def do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])

    ### time
    if(match.time_start > 0):
        elapsed_time = time.time() - match.time_start
        if(match.next_color() == COLORS['white']):
            match.white_elapsed_seconds += elapsed_time
        else:
            match.black_elapsed_seconds += elapsed_time

    match.time_start = time.time()
    ###

    move = matchmove.do_move(match, srcx, srcy, dstx, dsty, prom_piece)
    match.status = rules.status(match) #STATUS['open']
    map_matches(match, modelmatch, MAP_DIR['engine-to-model'])
    modelmatch.save()

    modelmove = ModelMove()                
    map_moves(move, modelmove, MAP_DIR['engine-to-model'])
    modelmove.match = modelmatch
    modelmove.save()


def undo_move(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    move = matchmove.undo_move(match)
    if(move):
        map_matches(match, modelmatch, MAP_DIR['engine-to-model'])
        modelmatch.save()

        modelmove = ModelMove.objects.filter(match_id=modelmatch.id, count=move.count).last()
        if(modelmove):
            modelmove.delete()


class Msgs:
    META_MATCHID = 'matchid'
    META_ISALIVE = 'isalive'
    META_TERMINATE = 'terminate'
    META_CURRENTSEARCH = 'currentsearch'

    def __init__(self, job):
        self.job = job

    def read_meta(self, key):
        try:
            return self.job.meta[key]
        except KeyError:
            return None

    def write_meta(self, key, value):
        try:
            self.job.meta[key] = value
            self.job.save_meta()
            return True
        except KeyError:
            return False


def calc_move_for_immanuel(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    if(rules.status(match) != STATUS['open']):
        return False, rules.status(match)
    elif(match.is_next_color_human()):
        return False, rules.RETURN_CODES['wrong-color']
    else:
        queue = django_rq.get_queue('default')
        job = queue.enqueue(job_calc_and_do_move, modelmatch, match)
        return True, rules.RETURN_CODES['ok']


def read_searchmoves(): 
    return debug.read_searchmoves(settings.BASE_DIR + "/kate/engine")

