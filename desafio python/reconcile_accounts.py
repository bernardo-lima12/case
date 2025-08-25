from bisect import bisect_left, bisect_right
from datetime import datetime, timedelta, date
from copy import deepcopy
from typing import List


def to_date(string: str) -> date:
    return datetime.strptime(string, '%Y-%m-%d').date()


def get_date_match(dates: List[date], ordered_idx: List[int], dt: date) -> List[int]:
    """Function to do bissection search or binary search"""
    a = bisect_left(dates, dt)
    b = bisect_right(dates, dt)
    return ordered_idx[a:b]


def remove_date(row: List[str]) -> List[str]:
    """Remove date column from the transactions list"""
    return row[1:]


def idx_sorted_by_date(transactions: List[List[str]]) -> List[int]:
    """Sort index according to the date."""
    list_range = range(len(transactions))
    def sort_rule(i): return transactions[i][0]
    return sorted(list_range, key=sort_rule)


def get_ordered_dates(
    transactions: List[List[str]],
    ordered_idx: List[int]
) -> List[date]:
    """Get a list of dates in order"""
    return [to_date(transactions[i][0]) for i in ordered_idx]


def add_missing(transactions: List[List[str]], not_used: set) -> None:
    """Add missing column to the remaining of columns"""
    for i in not_used:
        transactions[i].append('MISSING')


def get_first_match(
    candidates: List[int],
    used_idx: set,
    t1_value: List[str],
    t2_value: List[List[str]]
) -> int:
    """For the candidates transactions get the first match
    if the index was not used (transacation can't be counted twice)
    and if the column values are the same"""
    return next((
        i for i in candidates
        if i not in used_idx and t1_value == t2_value[i]
    ), None)


def get_previous_business_day(dt: date) -> date:
    """Get the previous business day from a given date"""
    if dt.weekday() == 0:  # segunda
        return dt - timedelta(days=3)  # sexta passada
    else:
        return dt - timedelta(days=1)


def get_next_business_day(dt: date) -> date:
    """Get the next business day from a given date"""
    if dt.weekday() == 4:  # sexta
        return dt + timedelta(days=3)  # proxima segunda
    else:
        return dt + timedelta(days=1)


def reconcile_accounts(
    transactions1: List[List[str]],
    transactions2: List[List[str]]
) -> tuple[List[List[str]], List[List[str]]]:

    # final output
    # these lists will be modified during the iteration
    t1_copy = deepcopy(transactions1)
    t2_copy = deepcopy(transactions2)  # create deepcopy because we have a list of lists

    # precalculated values
    t1_values = [remove_date(v) for v in transactions1]
    t2_values = [remove_date(v) for v in transactions2]

    # para duplicados e saber o que está missing
    used_idx = set()

    t2_ordered_idx = idx_sorted_by_date(t2_copy)
    t2_dates_ordered = get_ordered_dates(t2_copy, t2_ordered_idx)

    for i, row in enumerate(transactions1):
        date = to_date(row[0])
        t1_value = t1_values[i]

        for dt in (get_previous_business_day(date), date, get_next_business_day(date)):
            t2_candidates = get_date_match(t2_dates_ordered, t2_ordered_idx, dt)
            match = get_first_match(t2_candidates, used_idx, t1_value, t2_values)

            if match is not None:
                used_idx.add(match)
                t1_copy[i].append('FOUND')
                t2_copy[match].append('FOUND')
                break
        else:
            t1_copy[i].append('MISSING')

    all_idxs = set(range(len(transactions2)))
    not_used_idx = all_idxs - used_idx
    add_missing(t2_copy, not_used_idx)

    return t1_copy, t2_copy
