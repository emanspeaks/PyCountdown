from pyrandyos.gui.qt import QComboBox
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType
from pyrandyos.utils.time.rate import BaseClockRate

from ...logging import log_func_call


class RateListWidget(QtWidgetWrapper[QComboBox]):
    @log_func_call
    def create_qtobj(self, *args, **kwargs):
        parent_qtobj: GuiWidgetParentType = self.gui_parent.qtobj
        qtobj = QComboBox(parent_qtobj)

        for x in BaseClockRate:
            qtobj.addItem(x.name, x.value)

        return qtobj

    def get_rate(self):
        return BaseClockRate(self.qtobj.currentData())

    def set_rate(self, rate: str | BaseClockRate | int):
        if isinstance(rate, str):
            rate = BaseClockRate[rate]

        elif isinstance(rate, int):
            rate = BaseClockRate(rate)

        index = self.qtobj.findData(rate.value)
        if index != -1:
            self.qtobj.setCurrentIndex(index)
