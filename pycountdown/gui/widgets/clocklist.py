from pyrandyos.gui.qt import QComboBox
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType

from ...logging import log_func_call
from ...lib.clocks.displayclocks import DisplayClock, NOW_ID
from ...lib.clocks.clock import Clock


class ClockListWidget(QtWidgetWrapper[QComboBox]):
    def __init__(self, gui_parent: GuiWidgetParentType, show_now: bool = False,
                 *qtobj_args, **qtobj_kwargs):
        self.show_now = show_now
        super().__init__(gui_parent, *qtobj_args, **qtobj_kwargs)

    @log_func_call
    def create_qtobj(self, *args, **kwargs):
        parent_qtobj: GuiWidgetParentType = self.gui_parent.qtobj
        qtobj = QComboBox(parent_qtobj)

        if self.show_now:
            qtobj.addItem("(now)", NOW_ID)

        for name, clk_id in DisplayClock.get_valid_dclock_name_id_full_list():
            qtobj.addItem(name, clk_id)

        return qtobj

    def get_clock_id(self):
        return self.qtobj.currentData()

    def get_clock(self):
        return DisplayClock.get_clock_for_id(self.get_clock_id())

    def set_clock_id(self, clk_id: str):
        index = self.qtobj.findData(clk_id)
        if index == -1:
            index = 0

        self.qtobj.setCurrentIndex(index)

    def set_clock(self, clk: Clock):
        self.set_clock_id(DisplayClock.get_id_for_clock(clk))
