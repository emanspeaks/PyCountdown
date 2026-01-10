from typing import TYPE_CHECKING

from ....logging import log_func_call
from pyrandyos.gui.qt import (
    QVBoxLayout, QHBoxLayout, QDialogButtonBox, Qt, QKeySequence, QShortcut,
    QLabel,
    # QLineEdit,
    # QCheckBox, QRadioButton,
)
from PySide2.QtWidgets import QCheckBox
from pyrandyos.gui.dialogs import GuiDialogView
from pyrandyos.gui.callback import qt_callback

from ...widgets.epoch import EpochWidget
from ...widgets.clocklist import ClockListWidget
from ...widgets.ratelist import RateListWidget
from ...widgets.ctrl_shift_z_lineedit import CtrlShiftZLineEdit

if TYPE_CHECKING:
    from .pres import ClockEditorDialog


class ClockEditorDialogView(GuiDialogView['ClockEditorDialog']):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'ClockEditorDialog' = None,
                 *qtobj_args, **qtobj_kwargs):
        GuiDialogView.__init__(self, basetitle, presenter, *qtobj_args,
                               **qtobj_kwargs)
        qtobj = self.qtobj
        pres = self.gui_pres
        timer = pres.timer

        qtobj.setFixedSize(600, 200 if timer else 400)
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
        clk_lbl = CtrlShiftZLineEdit(block_ctrl_y=True)
        self.clk_lbl = clk_lbl

        hbox_lbl = QHBoxLayout()
        hbox_lbl.addWidget(QLabel('Label:'))
        hbox_lbl.addWidget(clk_lbl)
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

    @log_func_call
    def set_tab_order(self):
        qtobj = self.qtobj
        qtobj.setTabOrder(self.clk_lbl, self.clk_id_chk)
        qtobj.setTabOrder(self.clk_id_chk, self.clk_id)

        ref = self.ref
        follow_chk = self.follow_chk
        rate_chk = self.rate_chk
        nxt = (follow_chk if follow_chk else (rate_chk if rate_chk
                                              else self.dlgbuttons))
        if ref:
            self.epoch.set_tab_order(qtobj, self.clk_id, self.ref)
            ref.set_tab_order(qtobj, self.epoch, nxt)

        else:
            self.epoch.set_tab_order(qtobj, self.clk_id, nxt)

        nxt = rate_chk if rate_chk else self.dlgbuttons
        if follow_chk:
            qtobj.setTabOrder(follow_chk, self.follow.qtobj)
            qtobj.setTabOrder(self.follow.qtobj, nxt)

        if rate_chk:
            qtobj.setTabOrder(rate_chk, self.rate.qtobj)
            qtobj.setTabOrder(self.rate.qtobj, self.dlgbuttons)

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
        self.layout.addLayout(hbox_follow)
