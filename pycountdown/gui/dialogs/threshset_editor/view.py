from typing import TYPE_CHECKING
from functools import partial

from PySide2.QtWidgets import QListWidget, QCheckBox

from pyrandyos.gui.qt import (
    QVBoxLayout, QHBoxLayout, QDialogButtonBox, Qt, QKeySequence, QShortcut,
    QPushButton, QLabel
)
from pyrandyos.gui.dialogs import GuiDialogView
from pyrandyos.gui.callback import qt_callback

from ....logging import log_func_call
from ...widgets.epoch import EpochWidget
from ...widgets.colorbutton import ColorButtonWidget
if TYPE_CHECKING:
    from .pres import ThreshSetEditorDialog


class ThreshSetEditorDialogView(GuiDialogView['ThreshSetEditorDialog']):
    @log_func_call
    def __init__(self, basetitle: str,
                 presenter: 'ThreshSetEditorDialog' = None,
                 *qtobj_args, **qtobj_kwargs):
        GuiDialogView.__init__(self, basetitle, presenter, *qtobj_args,
                               **qtobj_kwargs)
        qtobj = self.qtobj

        qtobj.setFixedSize(600, 400)
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
        split = QHBoxLayout()
        split.addLayout(self.create_tset_list_panel())
        split.addLayout(self.create_thresh_list_panel())
        self.layout.addLayout(split)

        self.create_thresh_editor()

    @log_func_call
    def create_tset_list_panel(self):
        pres = self.gui_pres

        # List of threshold sets
        tset_list = QListWidget()
        cb = qt_callback(pres.update_thresh_list)
        tset_list.currentRowChanged.connect(cb)
        self.tset_list = tset_list

        # Buttons for set operations
        add_tset_btn = QPushButton("Add set")
        add_cb = partial(pres.add_rename_tset, True)
        add_tset_btn.clicked.connect(qt_callback(add_cb))
        self.add_tset_btn = add_tset_btn

        remove_tset_btn = QPushButton("Remove set")
        remove_tset_btn.clicked.connect(qt_callback(pres.remove_tset))
        self.remove_tset_btn = remove_tset_btn

        rename_tset_btn = QPushButton("Rename set")
        rename_tset_btn.clicked.connect(qt_callback(pres.add_rename_tset))
        self.rename_tset_btn = rename_tset_btn

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_tset_btn)
        btn_layout.addWidget(remove_tset_btn)
        btn_layout.addWidget(rename_tset_btn)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Threshold sets:"))
        layout.addWidget(tset_list)
        layout.addLayout(btn_layout)
        return layout

    @log_func_call
    def create_thresh_list_panel(self):
        pres = self.gui_pres

        # List of thresholds
        thresh_list = QListWidget()
        cb = qt_callback(pres.update_thresh_editor)
        thresh_list.currentRowChanged.connect(cb)
        self.thresh_list = thresh_list

        # Buttons for threshold operations
        add_thresh_btn = QPushButton("Add threshold")
        add_thresh_btn.clicked.connect(qt_callback(pres.add_thresh))
        self.add_thresh_btn = add_thresh_btn

        remove_thresh_btn = QPushButton("Remove threshold")
        remove_thresh_btn.clicked.connect(qt_callback(pres.remove_thresh))
        self.remove_thresh_btn = remove_thresh_btn

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_thresh_btn)
        btn_layout.addWidget(remove_thresh_btn)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Thresholds:"))
        layout.addWidget(thresh_list)
        layout.addLayout(btn_layout)
        return layout

    @log_func_call
    def create_thresh_editor(self):
        epoch_widget = EpochWidget(self, "Epoch:", show_clocklist=False)
        self.epoch_widget = epoch_widget

        color_widget = ColorButtonWidget(self, "Select Color")
        self.color_widget = color_widget

        alert_chk = QCheckBox('Play alert')
        alert_chk.setChecked(False)
        self.alert_chk = alert_chk

        update_thresh_btn = QPushButton("Update threshold")
        cb = self.gui_pres.save_current_thresh
        update_thresh_btn.clicked.connect(qt_callback(cb))
        self.update_thresh_btn = update_thresh_btn

        epoch_widget_hbox = epoch_widget.hbox_epoch
        epoch_widget_hbox.addWidget(color_widget.qtobj)
        epoch_widget_hbox.addWidget(alert_chk)
        epoch_widget_hbox.addWidget(update_thresh_btn)
        layout = self.layout
        layout.addWidget(epoch_widget.qtobj)
        layout.addStretch()
