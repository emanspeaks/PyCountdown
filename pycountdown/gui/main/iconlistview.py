from pyrandyos.gui.qt import Qt, QSize, QListView, QResizeEvent
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType

from ...logging import log_func_call, DEBUGLOW2


class IconListView(QtWidgetWrapper[QListView]):
    @log_func_call
    def __init__(self, columns: int, parent: GuiWidgetParentType = None):
        super().__init__(parent)
        self.columns = columns

    def create_qtobj(self):
        qtwin = self.gui_parent.gui_view.qtobj
        lv = QListView(qtwin)
        lv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        lv.resize = self.resize
        lv.resizeEvent = self.resizeEvent
        return lv

    @log_func_call
    def setColumns(self, cols: int):
        """
        Set columns number and resize.
        """
        self.columns = cols
        self.resize()

    @log_func_call(DEBUGLOW2, trace_only=True)
    def resize(self):
        """
        Set grid and icon size taking into account the number of columns.
        """
        lv = self.qtobj
        width = lv.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tileWidth = width/self.columns
        iconWidth = int(tileWidth*0.8)
        # tileWidth needs to be an integer for setGridSize
        tileWidth = int(tileWidth)

        lv.setGridSize(QSize(tileWidth, tileWidth))
        lv.setIconSize(QSize(iconWidth, iconWidth))

    @log_func_call(DEBUGLOW2, trace_only=True)
    def resizeEvent(self, event: QResizeEvent):
        self.resize()
        return QListView.resizeEvent(self.qtobj, event)
