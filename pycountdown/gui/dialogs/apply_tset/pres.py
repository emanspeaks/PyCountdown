from typing import TYPE_CHECKING

from pyrandyos.gui.widgets import GuiWindowLikeParentType
from pyrandyos.gui.dialogs import GuiDialog
from pyrandyos.gui.qt import QAbstractButton, QDialogButtonBox

from ....logging import log_func_call
from ....app import PyCountdownApp
from ....lib.clocks.displayclocks import DisplayClock

from .view import ApplyTSetDialogView

if TYPE_CHECKING:
    from ...main.pres import MainWindow


class ApplyTSetDialog(GuiDialog[ApplyTSetDialogView]):
    @log_func_call
    def __init__(self, gui_parent: GuiWindowLikeParentType,
                 r_dclks: list[tuple[int, DisplayClock]]):
        self.r_dclks = r_dclks
        super().__init__("Apply threshold set", gui_parent,
                         gui_parent.gui_view.qtobj)

    def get_message(self):
        msg = "Apply threshold set to selected clocks:\n"
        labels = [f"{r + 1}: {repr(dc.label) if dc.label else '(blank)'}"
                  for r, dc in self.r_dclks]
        msg += ", ".join(labels)
        return msg

    def save_selected_tset(self):
        tset = self.gui_view.tsetlist.get_threshset()
        if tset:
            tset = tset.thresh_id

        for _, dc in self.r_dclks:
            dc.formatter.thresh_set = tset

    @log_func_call
    def dlgbtn_clicked(self, btn: QAbstractButton = None):
        dlgview = self.gui_view
        buttons = dlgview.dlgbuttons
        if btn is buttons.button(QDialogButtonBox.Cancel):
            self.gui_view.qtobj.reject()
            return
        mw: 'MainWindow' = self.gui_parent
        if mw.set_save_path_if_unset():
            self.save_selected_tset()
            PyCountdownApp.export_clocks_file()
            mw.refresh_clocks_file(True)

        if btn is buttons.button(QDialogButtonBox.Ok):
            self.gui_view.qtobj.accept()

    @log_func_call
    def show(self):
        dialog = self.gui_view.qtobj

        # Show and raise the dialog
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    @log_func_call
    def create_gui_view(self, basetitle: str, *args,
                        **kwargs) -> ApplyTSetDialogView:
        return ApplyTSetDialogView(basetitle, self, *args, **kwargs)
