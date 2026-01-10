from typing import TYPE_CHECKING
from pathlib import Path

from pyrandyos.gui.widgets import GuiWindowLikeParentType
from pyrandyos.gui.dialogs import GuiDialog
from pyrandyos.gui.qt import QAbstractButton, QDialogButtonBox, QFileDialog

from ....logging import log_func_call
from ....app import PyCountdownApp

from .view import ClocksConfigDialogView

if TYPE_CHECKING:
    from ...main.pres import MainWindow


class ClocksConfigDialog(GuiDialog[ClocksConfigDialogView]):
    @log_func_call
    def __init__(self, gui_parent: GuiWindowLikeParentType):
        super().__init__("Clocks Configuration", gui_parent)

    @log_func_call
    def load_clocks_file(self):
        clocks_file = PyCountdownApp.get_clocks_file_path()
        return (clocks_file.read_text() if clocks_file and clocks_file.exists()
                else "")

    @log_func_call
    def dlgbtn_clicked(self, btn: QAbstractButton = None):
        dlgview = self.gui_view
        buttons = dlgview.dlgbuttons
        if btn is buttons.button(QDialogButtonBox.Cancel):
            self.gui_view.qtobj.reject()
            return

        if self.save_clocks_file() is None:
            return
        mw: 'MainWindow' = self.gui_parent
        mw.refresh_clocks_file(True)

        if btn is buttons.button(QDialogButtonBox.Ok):
            self.gui_view.qtobj.accept()

    @log_func_call
    def save_clocks_file(self):
        dlgview = self.gui_view
        editor = dlgview.editor
        txt = editor.get_text()

        mw: 'MainWindow' = self.gui_parent
        if not mw.set_save_path_if_unset():
            return None
        clocks_file = PyCountdownApp.get_clocks_file_path()
        if clocks_file:
            return clocks_file.write_text(txt)
        return None

    @log_func_call
    def show(self):
        dialog = self.gui_view.qtobj

        # Show and raise the dialog
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    @log_func_call
    def create_gui_view(self, basetitle: str, *args,
                        **kwargs) -> ClocksConfigDialogView:
        return ClocksConfigDialogView(basetitle, self, *args, **kwargs)
