from pyrandyos.utils.json import parse_jsonc
from pyrandyos.utils.casesafe import (
    casesafe_dict_get, casesafe_value_in_container, casesafe_is_equal,
)
from pyrandyos.utils.time.gregorian import ymdhms_to_sec
from pyrandyos.utils.time.dhms import dhms_to_sec
from pyrandyos.utils.time.rate import BaseClockRate
from pyrandyos.utils.time.fmt import TimeFormat, parse_time_format
from pyrandyos.utils.time.julian import DAY2SEC

from ...logging import log_error

from .clock import Clock, DEFAULT_CLOCKS
from .displayclocks import DisplayClock
from .epoch import Epoch
from .fmt import ClockFormatter, ThresholdSet, ClockThreshold


JsonEpochTimeType = float | int | list[float | int] | str
_SECS = TimeFormat.S
TO_SEC = {
    TimeFormat.S: 1,
    TimeFormat.M: 60,
    TimeFormat.H: 3600,
    TimeFormat.D: DAY2SEC,
}
CLOCK_NOT_FOUND = object()
CLOCK_UNRESOLVED = object()


def clock_has_problems(clock: Clock | None):
    return clock is CLOCK_NOT_FOUND or clock is CLOCK_UNRESOLVED


def is_clock_resolved(clock: Clock | None):
    return clock is not CLOCK_UNRESOLVED


def handle_clock_problems(clock: Clock | None, json: str):
    if clock is CLOCK_NOT_FOUND:
        log_error(f"Clock not found: {json}")

    return clock_has_problems(clock)


def get_clock_by_id(clk_id: str, pool: list[DisplayClock],
                    id2idx: dict[str, int], label_list: list[str] = None):
    if clk_id is None:
        return

    idx = casesafe_dict_get(id2idx, clk_id, None, True)
    if (idx is None and label_list
            and casesafe_value_in_container(label_list, clk_id, True)):
        for i, x in enumerate(label_list):
            if casesafe_is_equal(x, clk_id, True):
                idx = i
                break

    if idx is not None:
        dclk = pool[idx]
        if dclk:
            return dclk.clock

    clock = casesafe_dict_get(DEFAULT_CLOCKS, clk_id, CLOCK_NOT_FOUND, True)
    if clock is CLOCK_NOT_FOUND and idx is not None:
        return CLOCK_UNRESOLVED
    return clock


def extract_clock_ids(data: list[dict]):
    label_list: list[str] = list()
    id_list: list[str] = list()
    id2idx: dict[str, int] = dict()
    for i, row in enumerate(data):
        # blank = row.get('blank')
        label = row.get('label')
        clk_id = row.get('id', label)
        label_list.append(label)
        id_list.append(clk_id)
        if clk_id:
            id2idx[clk_id] = i

    return label_list, id_list, id2idx


def parse_rate(input_rate: str, follow: Clock = None):
    if input_rate is None:
        input_rate = follow.rate.name if follow else 'TAI'

    return BaseClockRate[input_rate.upper()]


def parse_epoch_time(t: JsonEpochTimeType,
                     input_fmt: TimeFormat = _SECS):
    if isinstance(t, list):
        epochlen = len(t)
        if epochlen == 4 or (epochlen == 5
                             and input_fmt is TimeFormat.DHMS):
            return dhms_to_sec(*t), TimeFormat.DHMS

        elif epochlen == 6:
            return ymdhms_to_sec(*t), TimeFormat.YMDHMS

        else:
            raise NotImplementedError

    elif isinstance(t, str):
        tparts = t.strip().split('/')
        len_tparts = len(tparts)
        if len_tparts > 2:
            raise NotImplementedError
        if len_tparts == 1:
            tparts = t.strip().split('\\')
            len_tparts = len(tparts)
            if len_tparts != 2:
                raise NotImplementedError
        tmp = tparts[0]
        sign = -1 if tmp.startswith('-') else 1
        day = int(tmp.split('-')[-1].strip())
        hms = tparts[1].strip()
        h = int(hms[:2])
        m = int(hms[3:5])
        s = float(hms[6:])
        return dhms_to_sec(day, h, m, s, sign), TimeFormat.DHMS

    elif t is not None:
        return float(t)*TO_SEC[input_fmt], input_fmt
    return None, input_fmt


def parse_epoch(data: dict, pool: list[DisplayClock] = None,
                id2idx: dict[str, int] = None, label_list: list[str] = None,
                skip_clock: bool = False):
    if data is None:
        return

    if skip_clock:
        clock = None

    else:
        clockname: str = data.get('clock')  # or data.get('anchor')
        clock = get_clock_by_id(clockname, pool, id2idx, label_list)
        if clock_has_problems(clock):
            return clock

    t, fmt = parse_epoch_time(data['t'],
                              parse_time_format(data.get('format', 's')))
    fold_known: bool = data.get('fold_known', False)
    fold: bool = data.get('fold', False)
    return Epoch(clock, t, fold_known, fold, fmt)


def parse_display(data: dict):
    if data is None:
        return

    hidden = data.get('hidden', False)
    fmt = parse_time_format(data.get('format'))
    digits: int = data.get('digits', 0)
    zeropad: int = data.get('zeropad', 0)
    return ClockFormatter(hidden, fmt, digits, zeropad, data.get('color'),
                          data.get('thresholds'))


def parse_threshold(data: dict):
    return ClockThreshold(parse_epoch(data.get('epoch'), skip_clock=True),
                          data.get('color'))


def parse_thresh_sets(data: dict[str, dict]):
    if data:
        return {k: ThresholdSet(k, [parse_threshold(x) for x in v])
                for k, v in data.items()}


def parse_clocks_jsonc(data: str | dict):
    "returns dclk_to_add, thresh_sets"
    if isinstance(data, str):
        data: dict = parse_jsonc(data)

    thresh_sets = parse_thresh_sets(data.get('threshold_sets'))

    clocks: list[dict] = data['clocks']

    # first get names and IDs of all clocks
    label_list, id_list, id2idx = extract_clock_ids(clocks)
    ids_to_resolve = list(enumerate(id_list))
    last_to_resolve = None
    dclk_to_add: list[DisplayClock] = [None]*len(clocks)

    while ids_to_resolve:
        if last_to_resolve == ids_to_resolve:
            log_error(f"Unresolved clocks: {ids_to_resolve}")
            break

        last_to_resolve = ids_to_resolve.copy()
        for resolve_tmp in ids_to_resolve.copy():
            i, clk_id = resolve_tmp
            row = clocks[i]
            blank = row.get('blank')
            label = label_list[i]
            display_fmt = parse_display(row.get('display')) or ClockFormatter()
            if blank:
                ids_to_resolve.remove(resolve_tmp)
                if clk_id:
                    dclk_to_add[i] = DisplayClock(clk_id, label, None,
                                                  display_fmt)

                continue

            json_follow = row.get('follow')
            follow = get_clock_by_id(json_follow, dclk_to_add, id2idx,
                                     label_list)
            if handle_clock_problems(follow, json_follow):
                continue

            rate = parse_rate(row.get('rate'), follow)

            json_epoch: dict = row.get('epoch')
            epoch = parse_epoch(json_epoch, dclk_to_add, id2idx,
                                label_list)
            if handle_clock_problems(epoch,
                                     json_epoch.get('clock') if json_epoch
                                     else None):
                continue

            json_ref: dict = row.get('ref')
            ref = parse_epoch(json_ref, dclk_to_add, id2idx, label_list)
            if handle_clock_problems(ref,
                                     json_ref.get('clock') if json_ref
                                     else None):
                continue

            # future work
            offset_sec = None
            _abs = False

            clock = Clock(epoch, ref, follow, rate, offset_sec, _abs)

            dclk_to_add[i] = DisplayClock(clk_id, label, clock, display_fmt)

            ids_to_resolve.remove(resolve_tmp)

    return dclk_to_add, thresh_sets


def export_clocks_jsonc(dclks: list[DisplayClock],
                        thresh_sets: dict[str, ThresholdSet]):
    thresh_items = thresh_sets.items() if thresh_sets else ()
    return {
        "$schema": "https://raw.githubusercontent.com/emanspeaks/PyCountdown/refs/heads/master/pycountdown/assets/clocks.schema.jsonc",  # noqa: E501
        'threshold_sets': {k: export_threshold_set(v)
                           for k, v in thresh_items},
        'clocks': [export_clock(x) for x in dclks]
    }


def export_threshold_set(thrset: ThresholdSet):
    return [export_threshold(x) for x in thrset.thresh_list]


def export_threshold(x: ClockThreshold):
    out = {'color': x.color.name()}
    epoch = x.epoch
    if epoch:
        out['epoch'] = export_epoch(epoch)
    return out


def export_epoch(x: Epoch):
    out = {
        't': x.as_fmt(),
        'format': x.input_fmt.name,
        'fold_known': x.fold_known,
        'fold': x.fold,
    }
    clk = x.clock
    if clk:
        out['clock'] = DisplayClock.get_id_for_clock(clk)

    return out


def export_clock(x: DisplayClock):
    if x is None:
        return {'blank': True}
    out = {
        'label': x.label,
        'id': x.clk_id,
        'display': export_formatter(x.formatter),
    }
    clk = x.clock
    epoch = clk.epoch
    ref = clk.ref
    follow = clk.follow
    rate = clk.rate
    absclk = clk._abs

    if epoch:
        out['epoch'] = export_epoch(epoch)

    if ref:
        out['ref'] = export_epoch(ref)

    if follow:
        out['follow'] = DisplayClock.get_id_for_clock(follow)

    if rate:
        out['rate'] = rate.name

    if absclk:
        out['_abs'] = absclk

    return out


def export_formatter(fmt: ClockFormatter):
    if fmt is None:
        return {}
    return {
        'color': fmt.color.name(),
        'digits': fmt.digits,
        'hidden': fmt.hidden,
        'thresh_set': fmt.thresh_set,
        'time_format': fmt.time_format.name,
        'zeropad': fmt.zeropad,
    }
