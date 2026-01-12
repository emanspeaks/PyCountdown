from typing import TYPE_CHECKING

from ....logging import log_func_call
# from ....app import PyCountdownApp
from pyrandyos.gui.qt import (
    QVBoxLayout, QHBoxLayout, QDialogButtonBox, QLabel,
)
from pyrandyos.gui.dialogs import GuiDialogView
from pyrandyos.gui.callback import qt_callback
# from pyrandyos.gui.widgets.json_edit import JsonEditorWidget

from ...widgets.threshsetlist import ThreshSetListWidget
if TYPE_CHECKING:
    from .pres import ApplyTSetDialog


class ApplyTSetDialogView(GuiDialogView['ApplyTSetDialog']):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'ApplyTSetDialog' = None,
                 *qtobj_args, **qtobj_kwargs):
        GuiDialogView.__init__(self, basetitle, presenter, *qtobj_args,
                               **qtobj_kwargs)
        qtobj = self.qtobj
        # qtobj.resize(1000, 600)
        # qtobj.setMaximumWidth(1000)
        self.layout = QVBoxLayout(qtobj)
        self.create_editor()
        self.create_dialog_buttons()

    @log_func_call
    def create_dialog_buttons(self):
        qtobj = self.qtobj
        pres = self.gui_pres
        layout = self.layout

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlgbuttons = QDialogButtonBox(btns, qtobj)
        dlgbuttons.rejected.connect(qtobj.reject)
        dlgbuttons.clicked.connect(qt_callback(pres.dlgbtn_clicked))
        hbox.addStretch()
        hbox.addWidget(dlgbuttons)
        self.dlgbuttons = dlgbuttons

    @log_func_call
    def create_editor(self):
        tsetlist = ThreshSetListWidget(self, show_none=True)
        tsetlist.set_threshset(None)
        self.tsetlist = tsetlist

        lbl = QLabel(self.gui_pres.get_message())
        lbl.setWordWrap(True)

        layout = self.layout
        layout.addWidget(lbl)
        layout.addWidget(tsetlist.qtobj)
