from typing import TYPE_CHECKING

from pyrandyos.gui.widgets import GuiWindowLikeParentType
from pyrandyos.gui.dialogs import GuiDialog
from pyrandyos.gui.qt import QAbstractButton, QDialogButtonBox
from pyrandyos.utils.time.now import now_tai_sec

from ....logging import log_func_call
# from ....app import PyCountdownApp
from ....lib.clocks.displayclocks import DisplayClock
from ....lib.clocks.clock import Clock, DEFAULT_CLOCKS
from ....lib.clocks.fmt import ClockFormatter

from .view import ClockEditorDialogView

if TYPE_CHECKING:
    from ...main.pres import MainWindow


class ClockEditorDialog(GuiDialog[ClockEditorDialogView]):
    @log_func_call
    def __init__(self, gui_parent: GuiWindowLikeParentType,
                 dclk: DisplayClock = None):
        self.dclk = dclk or DisplayClock(
            "", "", Clock(DEFAULT_CLOCKS['TAI'], now_tai_sec()),
            ClockFormatter()
        )
        title = "Edit Clock" if dclk else "New Clock"
        super().__init__(title, gui_parent)

    def save_clock(self):
        pass

    @log_func_call
    def dlgbtn_clicked(self, btn: QAbstractButton = None):
        dlgview = self.gui_view
        buttons = dlgview.dlgbuttons

        self.save_clock()
        mw: 'MainWindow' = self.gui_parent
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
                        **kwargs) -> ClockEditorDialogView:
        return ClockEditorDialogView(basetitle, self, *args, **kwargs)
