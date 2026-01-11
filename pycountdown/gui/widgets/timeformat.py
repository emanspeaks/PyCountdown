from pyrandyos.gui.qt import QComboBox
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType
from pyrandyos.utils.time.fmt import TimeFormat

from ...logging import log_func_call


class TimeFormatWidget(QtWidgetWrapper[QComboBox]):
    @log_func_call
    def create_qtobj(self, *args, **kwargs):
        parent_qtobj: GuiWidgetParentType = self.gui_parent.qtobj
        qtobj = QComboBox(parent_qtobj)

        for x in TimeFormat:
            qtobj.addItem(x.name)

        return qtobj

    def get_time_format(self):
        return TimeFormat[self.qtobj.currentText()]

    def set_time_format(self, time_format: str | TimeFormat):
        if isinstance(time_format, str):
            time_format = TimeFormat[time_format]

        index = self.qtobj.findText(time_format.name)
        if index != -1:
            self.qtobj.setCurrentIndex(index)
