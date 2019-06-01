from bin import configure
from bin import common

# Using preset ---------------------------------------------------------------------------------------------------------

def job_start():
    pass
def job_stop():
    pass
def job_confirm():
    pass


# Monitor and Trace ----------------------------------------------------------------------------------------------------

def trace_start(target_name, bomb_name, count_detail):
    sentences = configure.Sentences()
    targets = configure.Targets()
    bombs = configure.Bombs()

    pattern = sentences.get_sentence('trace_start')
    target_pack = targets.get_package(target_name)
    bomb_pack = bombs.get_package(bomb_name)

    pattern_dict = {'count_detail': count_detail}
    pattern_dict.update(target_pack)
    pattern_dict.update(bomb_pack)

    return pattern.format(**pattern_dict)

def trace_stop(target_name, bomb_name, count_detail, elapsed_detail, trace_gap):
    sentences = configure.Sentences()
    targets = configure.Targets()
    bombs = configure.Bombs()

    pattern = sentences.get_sentence('trace_stop')
    target_pack = targets.get_package(target_name)
    bomb_pack = bombs.get_package(bomb_name)

    pattern_dict = {
        'count_detail': count_detail,
        'elapsed_detail': elapsed_detail,
        'trace_gap': trace_gap,
    }
    pattern_dict.update(target_pack)
    pattern_dict.update(bomb_pack)

    return pattern.format(**pattern_dict)

def trace_finish(target_name, bomb_name, elapsed_detail, trace_gap):
    sentences = configure.Sentences()
    targets = configure.Targets()
    bombs = configure.Bombs()

    pattern = sentences.get_sentence('trace_finish')
    target_pack = targets.get_package(target_name)
    bomb_pack = bombs.get_package(bomb_name)

    pattern_dict = {
        'elapsed_detail': elapsed_detail,
        'trace_gap': trace_gap,
    }
    pattern_dict.update(target_pack)
    pattern_dict.update(bomb_pack)

    return pattern.format(**pattern_dict)

# Remind thins ---------------------------------------------------------------------------------------------------------

def trace_remind(target_name, bomb_name, count_secs, level):
    sentences = configure.Sentences()
    targets = configure.Targets()
    bombs = configure.Bombs()

    pattern = sentences.get_sentence('trace_remind_' + level)
    target_pack = targets.get_package(target_name)
    bomb_pack = bombs.get_package(bomb_name)


    pattern_dict = {
        'count_secs': count_secs,
        'count_detail': common.seconds2str(count_secs),
    }
    pattern_dict.update(target_pack)
    pattern_dict.update(bomb_pack)

    return pattern.format(**pattern_dict)

# Report things --------------------------------------------------------------------------------------------------------

def report_mission():
    pass
def report_lastest():
    pass
def report_minutes():
    pass
def report_systime():
    pass


# Disturb thins --------------------------------------------------------------------------------------------------------

def disturb_d():
    pass
def disturb_c():
    pass
def disturb_b():
    pass
def disturb_a():
    pass
def disturb_s():
    pass