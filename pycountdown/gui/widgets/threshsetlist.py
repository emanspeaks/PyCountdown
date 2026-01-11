from pyrandyos.gui.qt import QComboBox
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType

from ...logging import log_func_call
from ...lib.clocks.fmt import ThresholdSet


class ThreshSetListWidget(QtWidgetWrapper[QComboBox]):
    @log_func_call
    def create_qtobj(self, *args, **kwargs):
        parent_qtobj: GuiWidgetParentType = self.gui_parent.qtobj
        qtobj = QComboBox(parent_qtobj)

        for k, v in ThresholdSet.pool.items():
            qtobj.addItem(k, v)

        return qtobj

    def get_threshset_name(self):
        return self.qtobj.currentText()

    def get_threshset(self):
        return self.qtobj.currentData()

    def set_threshset(self, threshset: str | ThresholdSet):
        if isinstance(threshset, str):
            threshset = ThresholdSet.pool.get(threshset)

        index = self.qtobj.findData(threshset)
        if index != -1:
            self.qtobj.setCurrentIndex(index)
