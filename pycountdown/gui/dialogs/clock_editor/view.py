from typing import TYPE_CHECKING

from ....logging import log_func_call
# from ....app import PyCountdownApp
from pyrandyos.gui.qt import (
    QVBoxLayout, QHBoxLayout, QDialogButtonBox, Qt, QKeySequence, QShortcut,
)
from pyrandyos.gui.dialogs import GuiDialogView
from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.widgets.time_edit.dhms import DhmsWidget
from pyrandyos.gui.widgets.time_edit.ymdhms import YmdhmsWidget
from pyrandyos.gui.widgets.time_edit.y_doy_hms import YDoyHmsWidget

if TYPE_CHECKING:
    from .pres import ClockEditorDialog


class ClockEditorDialogView(GuiDialogView['ClockEditorDialog']):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'ClockEditorDialog' = None,
                 *qtobj_args, **qtobj_kwargs):
        GuiDialogView.__init__(self, basetitle, presenter, *qtobj_args,
                               **qtobj_kwargs)
        qtobj = self.qtobj
        qtobj.setFixedSize(400, 400)
        self.layout = QVBoxLayout(qtobj)
        self.create_editor()
        self.create_dialog_buttons()
        self.create_shortcuts()

    @log_func_call
    def create_shortcuts(self):
        qtobj = self.qtobj
        pres = self.gui_pres
        save_shortcut = QShortcut(QKeySequence(Qt.CTRL+Qt.Key_S), qtobj)
        save_shortcut.activated.connect(qt_callback(pres.dlgbtn_clicked))
        self.save_shortcut = save_shortcut

    @log_func_call
    def create_dialog_buttons(self):
        qtobj = self.qtobj
        pres = self.gui_pres
        layout = self.layout

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Save  # noqa: E501
        dlgbuttons = QDialogButtonBox(btns, qtobj)
        dlgbuttons.rejected.connect(qtobj.reject)
        dlgbuttons.clicked.connect(qt_callback(pres.dlgbtn_clicked))
        hbox.addStretch()
        hbox.addWidget(dlgbuttons)
        self.dlgbuttons = dlgbuttons

    @log_func_call
    def create_editor(self):
        # qtobj = self.qtobj
        # pres = self.gui_pres
        layout = self.layout

        dhms = DhmsWidget(self)
        layout.addWidget(dhms.qtobj)
        self.dhms = dhms

        ymdhms = YmdhmsWidget(self)
        layout.addWidget(ymdhms.qtobj)
        self.ymdhms = ymdhms

        y_doy_hms = YDoyHmsWidget(self)
        layout.addWidget(y_doy_hms.qtobj)
        self.y_doy_hms = y_doy_hms
