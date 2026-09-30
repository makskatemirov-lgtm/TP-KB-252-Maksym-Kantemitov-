import bisect

def find_insert_position(sorted_list, target):
    return bisect.bisect_left(sorted_list, target)