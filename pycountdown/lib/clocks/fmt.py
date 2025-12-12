from typing import TYPE_CHECKING

from pyrandyos.gui.qt import QColor
from pyrandyos.utils.time.fmt import TimeFormat, TimeFormatter

from .epoch import Epoch
if TYPE_CHECKING:
    from .displayclocks import DisplayClock

DEFAULT_COLOR = QColor('white')


def parse_color(in_color: str | list[int | float] | QColor):
    if in_color is None:
        return
    if isinstance(in_color, QColor):
        return in_color
    if not isinstance(in_color, str):
        return QColor(*in_color)
    return QColor(in_color)


class ClockFormatter(TimeFormatter):
    def __init__(self, hidden: bool = False, time_format: TimeFormat = None,
                 digits: int = 0, zeropad: int = 0,
                 color: str | list[int | float] | QColor = DEFAULT_COLOR,
                 thresh_set: str = None):
        super().__init__(time_format, digits, zeropad)
        self.hidden = hidden
        self.color = parse_color(color) or DEFAULT_COLOR
        self.thresh_set = thresh_set or None

    def get_color(self, dclock: 'DisplayClock', tai: float):
        thresh_set = self.thresh_set
        default = self.color or DEFAULT_COLOR
        if thresh_set:
            t = dclock.clock.tai_to_clock_time(tai).epoch_sec
            color = ThresholdSet.pool[thresh_set].get_color_for_t(t)
            return color or default
        return default


class ClockThreshold:
    def __init__(self, epoch: Epoch,
                 color: str | list[int | float] | QColor = DEFAULT_COLOR
                 ):
        self.epoch = epoch
        self.color = parse_color(color)


class ThresholdSet:
    pool: dict[str, 'ThresholdSet'] = dict()

    def __init__(self, thresh_id: str, thresh_list: list[ClockThreshold]):
        self.thresh_id = thresh_id
        self.thresh_list = thresh_list

    def get_sorted_indices_by_t(self) -> list[tuple[int, float]]:
        my_list = self.thresh_list
        if not my_list:
            return

        default = None
        tmp = list(enumerate(None if x.epoch is None else x.epoch.epoch_sec
                             for x in my_list))
        for x in tmp:
            i, t = x
            if t is None:
                default = x
                del tmp[i]
                break

        out = [] if default is None else [default]
        return out + sorted(tmp, key=lambda x: x[1])

    def get_color_for_t(self, t: float):
        idx_list = self.get_sorted_indices_by_t()
        if not idx_list:
            return
        my_list = self.thresh_list
        color = None
        for i, tcheck in idx_list or ():
            if tcheck is None or t >= tcheck:
                color = my_list[i].color
            else:
                return color

        return color
