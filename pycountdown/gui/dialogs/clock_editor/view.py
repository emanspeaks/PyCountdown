from typing import TYPE_CHECKING

from pyrandyos.gui.qt import (
    QVBoxLayout, QHBoxLayout, QDialogButtonBox, Qt, QKeySequence, QShortcut,
    QLabel, QPushButton,
    # QCheckBox, QRadioButton,
)
from PySide2.QtWidgets import QCheckBox, QSpinBox
from pyrandyos.gui.dialogs import GuiDialogView
from pyrandyos.gui.callback import qt_callback

from ....logging import log_func_call
from ...widgets.epoch import EpochWidget
from ...widgets.clocklist import ClockListWidget
from ...widgets.ratelist import RateListWidget
from ...widgets.ctrl_shift_z_lineedit import CtrlShiftZLineEdit
from ...widgets.threshsetlist import ThreshSetListWidget
from ...widgets.timeformat import TimeFormatWidget
from ...widgets.colorbutton import ColorButtonWidget

if TYPE_CHECKING:
    from .pres import ClockEditorDialog

TIMER_HEIGHT = 240
CLOCK_HEIGHT = 450
BLANK_HEIGHT = 170


class ClockEditorDialogView(GuiDialogView['ClockEditorDialog']):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'ClockEditorDialog' = None,
                 *qtobj_args, **qtobj_kwargs):
        GuiDialogView.__init__(self, basetitle, presenter, *qtobj_args,
                               **qtobj_kwargs)
        qtobj = self.qtobj
        pres = self.gui_pres
        timer = pres.timer

        qtobj.setFixedSize(600, TIMER_HEIGHT if timer else CLOCK_HEIGHT)
        self.layout = QVBoxLayout(qtobj)
        self.create_editor()
        self.create_dialog_buttons()
        self.create_shortcuts()
        self.set_tab_order()

    @log_func_call
    def create_shortcuts(self):
        qtobj = self.qtobj
        pres = self.gui_pres

        self.save_shortcut = None
        if not pres.timer:
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

        self.delete_btn = None
        if not pres.new:
            delete_btn = QPushButton("Delete", qtobj)
            delete_btn.clicked.connect(qt_callback(pres.click_delete))
            hbox.addWidget(delete_btn)
            self.delete_btn = delete_btn

        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        # because we clear the pool when the file is reloaded, it's difficult
        # to maintain a reference to the "right" clock if we allow keeping
        # the window open during a file reload.  Rather than figure it out,
        # since it's already an edge case, just only allow Ok to save the edits
        #
        # if not pres.timer:
        #     btns |= QDialogButtonBox.Save

        dlgbuttons = QDialogButtonBox(btns, qtobj)
        dlgbuttons.rejected.connect(qtobj.reject)
        dlgbuttons.clicked.connect(qt_callback(pres.dlgbtn_clicked))
        hbox.addStretch()
        hbox.addWidget(dlgbuttons)
        self.dlgbuttons = dlgbuttons

    def create_clk_label(self):
        pres = self.gui_pres
        timer = pres.timer
        clk_lbl = CtrlShiftZLineEdit(block_ctrl_y=True)
        self.clk_lbl = clk_lbl

        if timer:
            self.blank_chk = None

        else:
            blank_chk = QCheckBox("Blank")
            blank_chk.stateChanged.connect(qt_callback(pres.toggle_blank))
            blank_chk.setChecked(False)
            self.blank_chk = blank_chk

        hbox_lbl = QHBoxLayout()
        hbox_lbl.addWidget(QLabel('Label:'))
        hbox_lbl.addWidget(clk_lbl)
        if not timer:
            hbox_lbl.addWidget(blank_chk)

        self.layout.addLayout(hbox_lbl)

    def create_clk_id(self):
        clk_id = CtrlShiftZLineEdit(block_ctrl_y=True)
        self.clk_id = clk_id

        clk_id_chk = QCheckBox("Clock ID:")
        clk_id_chk.stateChanged.connect(
            lambda state: clk_id.setEnabled(state == Qt.Checked)
        )
        clk_id_chk.setChecked(False)
        self.clk_id_chk = clk_id_chk

        # Ensure textbox starts in correct state
        clk_id.setEnabled(clk_id_chk.isChecked())

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(clk_id_chk)
        hbox_id.addWidget(clk_id)
        self.layout.addLayout(hbox_id)

    def create_epoch_editor(self):
        pres = self.gui_pres
        epoch = EpochWidget(self, "Epoch:", pres.timer, True)
        self.epoch = epoch
        self.layout.addWidget(epoch.qtobj)

    def create_ref_editor(self):
        ref = EpochWidget(self, "Real-time reference:")
        self.ref = ref
        self.layout.addWidget(ref.qtobj)

    @log_func_call
    def create_editor(self):
        pres = self.gui_pres
        self.create_clk_label()
        self.create_clk_id()
        self.create_epoch_editor()
        if pres.timer:
            self.ref = None
            self.follow_chk = None
            self.follow = None
            self.rate_chk = None
            self.rate = None

        else:
            self.create_ref_editor()
            self.ref.epoch_chk.stateChanged.connect(
                qt_callback(pres.update_epoch_label)
            )

            self.create_follow()
            self.create_rate()

        self.create_formatting_options()

    def create_formatting_options(self):
        # pres = self.gui_pres
        # dclk_fmt = dclk.formatter
        # dclk_fmt.color = None
        # dclk_fmt.digits = None
        # dclk_fmt.hidden = None
        # dclk_fmt.thresh_set = None
        # dclk_fmt.time_format = None
        # dclk_fmt.zeropad = None

        hidden_chk = QCheckBox("Hidden")
        hidden_chk.setChecked(False)
        self.hidden_chk = hidden_chk

        digits = QSpinBox()
        digits.setValue(0)
        digits.setMinimum(0)
        digits.setMaximum(20)
        digits.setFixedWidth(50)
        self.digits = digits

        zeropad = QSpinBox()
        zeropad.setValue(0)
        zeropad.setMinimum(0)
        zeropad.setMaximum(20)
        zeropad.setFixedWidth(50)
        self.zeropad = zeropad

        threshset = ThreshSetListWidget(self)
        self.threshset = threshset

        threshset_chk = QCheckBox("Threshold sets:")
        threshset_chk.stateChanged.connect(qt_callback(self.gui_pres.toggle_threshsets))  # noqa: E501
        threshset_chk.setChecked(False)
        self.threshset_chk = threshset_chk

        # Ensure textbox starts in correct state
        threshset.qtobj.setEnabled(threshset_chk.isChecked())

        color_btn = ColorButtonWidget(self, 'Default color')
        self.color_btn = color_btn

        display_fmt = TimeFormatWidget(self)
        self.display_fmt = display_fmt

        hbox_fmt1 = QHBoxLayout()
        hbox_fmt1.addWidget(hidden_chk)
        hbox_fmt1.addStretch()
        hbox_fmt1.addWidget(QLabel('Decimal digits:'))
        hbox_fmt1.addWidget(digits)
        hbox_fmt1.addWidget(QLabel('Zero-padded width:'))
        hbox_fmt1.addWidget(zeropad)
        hbox_fmt1.addWidget(QLabel('Display format:'))
        hbox_fmt1.addWidget(display_fmt.qtobj)
        self.layout.addLayout(hbox_fmt1)

        hbox_fmt2 = QHBoxLayout()
        hbox_fmt2.addWidget(threshset_chk)
        hbox_fmt2.addWidget(threshset.qtobj)
        hbox_fmt2.addWidget(color_btn.qtobj)
        hbox_fmt2.addStretch()
        self.layout.addLayout(hbox_fmt2)

    @log_func_call
    def set_tab_order(self):
        qtobj = self.qtobj

        blank_chk = self.blank_chk
        nxt = blank_chk if blank_chk else self.clk_id_chk
        qtobj.setTabOrder(self.clk_lbl, nxt)
        if blank_chk:
            qtobj.setTabOrder(blank_chk, self.clk_id_chk)

        qtobj.setTabOrder(self.clk_id_chk, self.clk_id)

        ref = self.ref
        follow_chk = self.follow_chk
        rate_chk = self.rate_chk
        nxt = (follow_chk if follow_chk else (rate_chk if rate_chk
                                              else self.hidden_chk))
        if ref:
            self.epoch.set_tab_order(qtobj, self.clk_id, self.ref)
            ref.set_tab_order(qtobj, self.epoch, nxt)

        else:
            self.epoch.set_tab_order(qtobj, self.clk_id, nxt)

        nxt = rate_chk if rate_chk else self.hidden_chk
        if follow_chk:
            qtobj.setTabOrder(follow_chk, self.follow.qtobj)
            qtobj.setTabOrder(self.follow.qtobj, nxt)

        if rate_chk:
            qtobj.setTabOrder(rate_chk, self.rate.qtobj)
            qtobj.setTabOrder(self.rate.qtobj, self.hidden_chk)

        qtobj.setTabOrder(self.hidden_chk, self.digits)
        qtobj.setTabOrder(self.digits, self.zeropad)
        qtobj.setTabOrder(self.zeropad, self.display_fmt.qtobj)
        qtobj.setTabOrder(self.display_fmt.qtobj, self.threshset_chk)
        qtobj.setTabOrder(self.threshset_chk, self.threshset.qtobj)
        qtobj.setTabOrder(self.threshset.qtobj, self.color_btn.qtobj)
        qtobj.setTabOrder(self.color_btn.qtobj, self.dlgbuttons)

    def create_rate(self):
        rate = RateListWidget(self)
        self.rate = rate

        rate_chk = QCheckBox("Tick rate:")
        rate_chk.stateChanged.connect(
            lambda state: rate.qtobj.setEnabled(state == Qt.Checked)
        )
        rate_chk.setChecked(False)
        self.rate_chk = rate_chk

        # Ensure textbox starts in correct state
        rate.qtobj.setEnabled(rate_chk.isChecked())

        hbox_rate = QHBoxLayout()
        hbox_rate.addWidget(rate_chk)
        hbox_rate.addWidget(rate.qtobj)
        hbox_rate.addStretch()
        self.layout.addLayout(hbox_rate)

    def create_follow(self):
        follow = ClockListWidget(self)
        self.follow = follow

        follow_chk = QCheckBox("Follow clock:")
        follow_chk.stateChanged.connect(
            lambda state: follow.qtobj.setEnabled(state == Qt.Checked)
        )
        follow_chk.setChecked(False)
        self.follow_chk = follow_chk

        # Ensure textbox starts in correct state
        follow.qtobj.setEnabled(follow_chk.isChecked())

        hbox_follow = QHBoxLayout()
        hbox_follow.addWidget(follow_chk)
        hbox_follow.addWidget(follow.qtobj)
        hbox_follow.addStretch()
        self.layout.addLayout(hbox_follow)
