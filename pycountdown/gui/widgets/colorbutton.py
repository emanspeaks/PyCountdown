from PySide2.QtWidgets import QColorDialog

from pyrandyos.gui.qt import QPushButton, QColor
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType
from pyrandyos.gui.callback import qt_callback
# from pyrandyos.utils.time.fmt import

from ...logging import log_func_call
from ...lib.clocks.fmt import DEFAULT_COLOR


class ColorButtonWidget(QtWidgetWrapper[QPushButton]):
    def __init__(self, gui_parent: GuiWidgetParentType = None,
                 label: str = 'Default color', *qtobj_args, **qtobj_kwargs):
        self.color = DEFAULT_COLOR
        self.label = label
        super().__init__(gui_parent, *qtobj_args, **qtobj_kwargs)

    @log_func_call
    def create_qtobj(self, *args, **kwargs):
        parent_qtobj: GuiWidgetParentType = self.gui_parent.qtobj
        qtobj = QPushButton(self.label, parent_qtobj)
        qtobj.clicked.connect(qt_callback(self.open_color_dialog))
        qtobj.setStyleSheet(self.color_btn_style(self.color))
        return qtobj

    def get_color(self):
        return self.color

    def set_color(self, color: QColor):
        self.color = color
        self.qtobj.setStyleSheet(self.color_btn_style(self.color))

    def color_btn_style(self, color: QColor):
        return f'QPushButton {{ background-color: black; color: {color.name()}; }}'  # noqa: E501

    def open_color_dialog(self):
        color_btn = self.qtobj
        color = QColorDialog.getColor(self.color, color_btn)
        if color.isValid():
            self.set_color(color)
