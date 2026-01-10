from typing import TYPE_CHECKING

from pyrandyos.gui.widgets import GuiWindowLikeParentType
from pyrandyos.gui.dialogs import GuiDialog
from pyrandyos.gui.qt import QAbstractButton, QDialogButtonBox, Qt
from pyrandyos.utils.time.fmt import TimeFormat
from pyrandyos.utils.time.rate import BaseClockRate

from ....app import PyCountdownApp
from ....logging import log_func_call
from ....lib.clocks.displayclocks import DisplayClock
from ....lib.clocks.clock import Clock, DEFAULT_CLOCKS
from ....lib.clocks.fmt import ClockFormatter
from ....lib.clocks.epoch import Epoch

from .view import ClockEditorDialogView

if TYPE_CHECKING:
    from ...main.pres import MainWindow


class ClockEditorDialog(GuiDialog[ClockEditorDialogView]):
    @log_func_call
    def __init__(self, gui_parent: GuiWindowLikeParentType,
                 dclk: DisplayClock = None, timer: bool = False):
        self.new = dclk is None
        default_clock = DEFAULT_CLOCKS['TAI' if timer else 'UTC']
        default_fmt = TimeFormat.DHMS if timer else TimeFormat.YMDHMS
        self.dclk = dclk or DisplayClock(
            "", "", Clock(Epoch(default_clock, input_fmt=default_fmt),
                          rate=None),
            ClockFormatter()
        )
        self.timer = timer
        title = ("Edit Clock" if dclk
                 else ("New Timer" if timer else "New Clock"))
        super().__init__(title, gui_parent)
        self.set_values()

    def save_clock(self):
        self.get_values()
        if self.new:
            DisplayClock.pool.append(self.dclk)

        clocks_file = PyCountdownApp.get_clocks_file_path()
        if clocks_file and clocks_file.exists():
            PyCountdownApp.export_clocks_file()

    @log_func_call
    def dlgbtn_clicked(self, btn: QAbstractButton = None):
        dlgview = self.gui_view
        buttons = dlgview.dlgbuttons

        if btn is buttons.button(QDialogButtonBox.Cancel):
            self.gui_view.qtobj.reject()
            return

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

    def update_epoch_label(self, state: bool | Qt.CheckState):
        view = self.gui_view
        epoch = view.epoch
        if state is True or state == Qt.Checked:
            epoch.set_label('Epoch @ reference:')

        else:
            epoch.set_label('Epoch:')

    def set_values(self):
        view = self.gui_view
        dclk = self.dclk

        dclk_lbl = dclk.label or ""
        view.clk_lbl.setText(dclk_lbl)

        dclk_id = dclk.clk_id or ""
        clk_id = view.clk_id
        clk_id.setText(dclk_id)

        clk_id_chk = view.clk_id_chk
        clk_id_chk.setChecked(dclk and dclk_id != dclk_lbl)
        clk_id.setEnabled(clk_id_chk.isChecked())

        clock = dclk.clock
        clk_epoch = clock.epoch
        clk_ref = clock.ref
        clk_follow = clock.follow
        clk_rate = clock.rate

        view.epoch.set_values(clk_epoch)
        ref = view.ref
        if ref:
            ref.set_values(clk_ref)
            self.update_epoch_label(clk_ref is not None)

        follow_chk = view.follow_chk
        follow = view.follow
        if follow_chk:
            follow_chk.setChecked(clk_follow is not None)
            follow.qtobj.setEnabled(follow_chk.isChecked())
            follow.set_clock(clk_follow)

        rate_chk = view.rate_chk
        rate = view.rate
        if rate_chk:
            rate_chk.setChecked(clk_rate is not None)
            view.rate.qtobj.setEnabled(rate_chk.isChecked())
            rate.set_rate(clk_rate if clk_rate else BaseClockRate.TAI)

        # formatter = dclk.formatter
        # fmt_color = formatter.color
        # fmt_digits = formatter.digits
        # fmt_hidden = formatter.hidden
        # fmt_tset = formatter.thresh_set
        # fmt_fmt = formatter.time_format
        # fmt_zeropad = formatter.zeropad

    def get_values(self):
        view = self.gui_view
        dclk = self.dclk

        label = view.clk_lbl.text()
        dclk.label = label

        clk_id_chk = view.clk_id_chk
        dclk.clk_id = view.clk_id.text() if clk_id_chk.isChecked() else label

        dclk_clock = dclk.clock
        dclk_clock.epoch = view.epoch.get_epoch()
        dclk_clock.ref = view.ref.get_epoch() if view.ref else None

        follow_chk = view.follow_chk
        do_follow = follow_chk.isChecked() if follow_chk else False
        follow = view.follow.get_clock() if do_follow else None
        dclk_clock.follow = follow

        rate_chk = view.rate_chk
        do_rate = rate_chk.isChecked() if rate_chk else False
        rate = view.rate.get_rate() if do_rate else None
        if not rate:
            rate = follow.rate if follow else BaseClockRate.TAI

        dclk_clock.rate = rate

        # dclk_fmt = dclk.formatter
        # dclk_fmt.color = None
        # dclk_fmt.digits = None
        # dclk_fmt.hidden = None
        # dclk_fmt.thresh_set = None
        # dclk_fmt.time_format = None
        # dclk_fmt.zeropad = None
