from typing import TYPE_CHECKING
from copy import deepcopy

from PySide2.QtWidgets import QInputDialog

from pyrandyos.gui.widgets import GuiWindowLikeParentType
from pyrandyos.gui.dialogs import GuiDialog
from pyrandyos.gui.qt import (
    QAbstractButton, QDialogButtonBox, QMessageBox, Qt
)
from pyrandyos.utils.time.fmt import FLOAT_FMTS

from ....logging import log_func_call
from ....app import PyCountdownApp
from ....lib.clocks.fmt import ThresholdSet, ClockThreshold, DEFAULT_COLOR
from ....lib.clocks.displayclocks import DisplayClock

from .view import ThreshSetEditorDialogView

if TYPE_CHECKING:
    from ...main.pres import MainWindow


class ThreshSetEditorDialog(GuiDialog[ThreshSetEditorDialogView]):
    @log_func_call
    def __init__(self, gui_parent: GuiWindowLikeParentType):
        self.tset_idx = None
        self.thresh_idx = None
        self.working = False
        self.pool = deepcopy(ThresholdSet.pool)
        super().__init__('Edit Threshold Sets', gui_parent,
                         gui_parent.gui_view.qtobj)
        self.update_tset_list()

    @log_func_call
    def save_current_thresh(self):
        idx = self.thresh_idx
        tset = self.pool.get(self.get_tset_name())
        if not tset or idx is None:
            return
        thresh = tset.thresh_list[idx]
        view = self.gui_view
        epoch = view.epoch_widget.get_epoch()
        thresh.epoch = epoch
        thresh.color = view.color_widget.get_color()
        thresh.play_alert = view.alert_chk.isChecked()
        view.thresh_list.item(idx).setText(self.get_thresh_text(thresh))

    def save_and_reset_tset(self):
        self.save_and_reset_threshlist()
        self.gui_view.thresh_list.clear()
        self.tset_idx = None

    def save_and_reset_threshlist(self):
        self.save_current_thresh()
        view = self.gui_view
        epoch_widget = view.epoch_widget
        epoch_widget.qtobj.setVisible(False)
        epoch_widget.set_values(None)
        view.color_widget.set_color(DEFAULT_COLOR)
        self.thresh_idx = None

    def get_tset_name(self):
        tset_idx = self.tset_idx
        if tset_idx is None:
            return ''
        item = self.gui_view.tset_list.item(tset_idx)
        if item:
            return item.text()
        raise RuntimeError('tset_idx inconsistency')

    @staticmethod
    def get_thresh_text(thresh: ClockThreshold):
        epoch = thresh.epoch
        if epoch:
            txt = epoch.as_fmt_str()
            input_fmt = epoch.input_fmt
            if input_fmt in FLOAT_FMTS:
                txt += f' [{input_fmt.name.lower()}]'

        else:
            txt = '(start)'

        if thresh.play_alert:
            txt += ' <alert>'

        return txt

    @log_func_call
    def update_tset_list(self):
        self.save_and_reset_tset()
        view = self.gui_view
        tset_list = view.tset_list
        tset_list.clear()
        for tset_name in sorted(self.pool.keys()):
            tset_list.addItem(tset_name)

        # # Select first item if available
        # if tset_list.count() > 0:
        #     tset_list.setCurrentRow(0)

    @log_func_call
    def update_thresh_list(self, row: int):
        self.save_and_reset_tset()
        tset_idx = None if row < 0 else row
        if tset_idx is None:
            return
        self.tset_idx = tset_idx
        tset = self.pool.get(self.get_tset_name())
        if not tset:
            return
        view = self.gui_view
        thresh_list = view.thresh_list
        for thr in tset.thresh_list:
            thresh_list.addItem(self.get_thresh_text(thr))

        # # Select first item if available
        # if thresh_list.count() > 0:
        #     thresh_list.setCurrentRow(0)

    @log_func_call
    def update_thresh_editor(self, row: int):
        self.save_and_reset_threshlist()
        idx = None if row < 0 else row
        tset = self.pool.get(self.get_tset_name())
        if not tset or idx is None:
            return
        self.thresh_idx = idx
        thresh = tset.thresh_list[idx]
        view = self.gui_view
        epoch_widget = view.epoch_widget
        epoch_widget.qtobj.setVisible(True)
        epoch_widget.set_values(thresh.epoch)
        view.color_widget.set_color(thresh.color)
        view.alert_chk.setChecked(thresh.play_alert)

    @log_func_call
    def add_rename_tset(self, new: bool = False):
        view = self.gui_view
        qtobj = view.qtobj
        oldname = None if new else self.get_tset_name()
        title = "Add" if new else "Rename"
        name, ok = QInputDialog.getText(qtobj, f"{title} Threshold Set",
                                        "Enter set name:", text=oldname)
        if name == oldname:
            return
        if ok and name:
            if not new and self.check_clocks_for_tset(oldname, 'rename'):
                return
            pool = self.pool
            if name in pool:
                QMessageBox.warning(qtobj, "Duplicate Name",
                                    f"A threshold set named '{name}' "
                                    "already exists.")
                return

            self.save_and_reset_tset()
            oldtset = ThresholdSet(name, []) if new else pool.pop(oldname)
            pool[name] = oldtset
            self.update_tset_list()

            # Select the new set
            tset_list = view.tset_list
            items = tset_list.findItems(name, Qt.MatchExactly)
            if items:
                tset_list.setCurrentItem(items[0])

    def check_clocks_for_tset(self, name: str, action: str):
        errors: list[tuple[int, DisplayClock]] = []
        for pair in enumerate(DisplayClock.pool):
            _, dclk = pair
            if dclk.formatter.thresh_set == name:
                errors.append(pair)

        if errors:
            msg = (f'Cannot {action} threshold set {name!r} because it is '
                   'used by clocks: ')
            msg += ', '.join(f'[{i}] {dclk.clk_id!r}' for i, dclk in errors)
            msg += f'\nYou must remove all references before you may {action}.'
            QMessageBox.warning(self.gui_view.qtobj,
                                "Threshold Set In Use", msg)
            return True

    @log_func_call
    def remove_tset(self):
        if self.tset_idx is None:
            return
        view = self.gui_view
        qtobj = view.qtobj
        name = self.get_tset_name()
        if self.check_clocks_for_tset(name, 'delete'):
            return

        reply = QMessageBox.question(
            qtobj, "Remove Threshold Set",
            f"Are you sure you want to remove '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.save_and_reset_tset()
            del self.pool[name]
            self.update_tset_list()

    @log_func_call
    def add_thresh(self):
        self.save_and_reset_threshlist()
        tset = self.pool.get(self.get_tset_name())
        if not tset:
            return
        new = ClockThreshold(None, DEFAULT_COLOR)
        tlist = tset.thresh_list
        new_index = len(tlist)
        tlist.append(new)
        view = self.gui_view
        gui_threshlist = view.thresh_list
        gui_threshlist.addItem("(new)")
        gui_threshlist.setCurrentRow(new_index)

    @log_func_call
    def remove_thresh(self):
        idx = self.thresh_idx
        tset = self.pool.get(self.get_tset_name())
        if not tset or idx is None:
            return
        view = self.gui_view
        qtobj = view.qtobj
        reply = QMessageBox.question(qtobj, "Remove Threshold",
                                     "Are you sure you want to remove "
                                     "this threshold?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save_and_reset_threshlist()
            del tset.thresh_list[idx]
            view.thresh_list.takeItem(idx)

    @log_func_call
    def dlgbtn_clicked(self, btn: QAbstractButton = None):
        dlgview = self.gui_view
        buttons = dlgview.dlgbuttons
        if btn is buttons.button(QDialogButtonBox.Cancel):
            self.gui_view.qtobj.reject()
            return
        mw: 'MainWindow' = self.gui_parent
        if mw.set_save_path_if_unset():
            self.save_current_thresh()
            ThresholdSet.pool = self.pool
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
                        **kwargs) -> ThreshSetEditorDialogView:
        return ThreshSetEditorDialogView(basetitle, self, *args, **kwargs)
