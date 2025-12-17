from typing import TYPE_CHECKING

from pyrandyos.gui.widgets import GuiWindowLikeParentType
from pyrandyos.gui.dialogs import GuiDialog
from pyrandyos.gui.qt import QAbstractButton, QDialogButtonBox

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
        return clocks_file.read_text()

    @log_func_call
    def save_clicked(self, btn: QAbstractButton = None):
        dlgview = self.gui_view
        buttons = dlgview.dlgbuttons

        self.save_clocks_file()
        mw: 'MainWindow' = self.gui_parent
        mw.refresh_clocks_file(True)
        if btn is buttons.button(QDialogButtonBox.Ok):
            self.gui_view.qtobj.accept()

    @log_func_call
    def save_clocks_file(self):
        dlgview = self.gui_view
        editor = dlgview.editor
        txt = editor.get_text()
        clocks_file = PyCountdownApp.get_clocks_file_path()
        return clocks_file.write_text(txt)

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
