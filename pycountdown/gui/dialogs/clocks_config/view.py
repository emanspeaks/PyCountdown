from typing import TYPE_CHECKING

from ....logging import log_func_call
from ....app import PyCountdownApp
from pyrandyos.gui.qt import (
    QVBoxLayout, QHBoxLayout, QDialogButtonBox, Qt, QKeySequence, QShortcut,
)
from pyrandyos.gui.dialogs import GuiDialogView
from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.widgets.json_edit import JsonEditorWidget

if TYPE_CHECKING:
    from .pres import ClocksConfigDialog


class ClocksConfigDialogView(GuiDialogView['ClocksConfigDialog']):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'ClocksConfigDialog' = None,
                 *qtobj_args, **qtobj_kwargs):
        GuiDialogView.__init__(self, basetitle, presenter, *qtobj_args,
                               **qtobj_kwargs)
        qtobj = self.qtobj
        qtobj.resize(*PyCountdownApp.get_default_win_size())
        self.layout = QVBoxLayout(qtobj)
        self.create_editor()
        self.create_dialog_buttons()
        self.create_shortcuts()

    @log_func_call
    def create_shortcuts(self):
        qtobj = self.qtobj
        pres = self.gui_pres
        save_shortcut = QShortcut(QKeySequence(Qt.CTRL+Qt.Key_S), qtobj)
        save_shortcut.activated.connect(qt_callback(pres.save_clicked))
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
        # dlgbuttons.accepted.connect(qt_callback(pres.save_and_close))
        dlgbuttons.rejected.connect(qtobj.reject)
        dlgbuttons.clicked.connect(qt_callback(pres.save_clicked))
        hbox.addStretch()
        hbox.addWidget(dlgbuttons)
        self.dlgbuttons = dlgbuttons

    @log_func_call
    def create_editor(self):
        # qtobj = self.qtobj
        pres = self.gui_pres
        layout = self.layout

        editor = JsonEditorWidget(self)
        layout.addWidget(editor.qtobj)
        self.editor = editor

        editor.set_text(pres.load_clocks_file())
