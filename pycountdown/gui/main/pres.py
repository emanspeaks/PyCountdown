from pathlib import Path

from pyrandyos.gui.qt import QTimer, Qt, QFileDialog, QMessageBox
from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.window import GuiWindow
# from pyrandyos.gui.dialogs.config import ConfigTreeDialog
from pyrandyos.utils.time.now import now_tai_sec

from ...version import __version__
from ...logging import log_func_call, DEBUGLOW2, log_info, log_debuglow
from ...app import (
    PyCountdownApp, CLOCKS_FILE_CHECK_SEC_KEY, LOCAL_SHOW_HIDDEN_KEY
)
# from ...lib.clocks import DEFAULT_CLOCKS, Clock
from ...lib.clocks.displayclocks import DisplayClock
# from ...lib.clocks.fmt import ClockFormatter

from ..dialogs.clocks_config import ClocksConfigDialog
from ..dialogs.clock_editor import ClockEditorDialog
from ..dialogs.threshset_editor import ThreshSetEditorDialog
from ..dialogs.config import ConfigTreeDialog
from ..dialogs.apply_tset import ApplyTSetDialog

from .view import MainWindowView

UserRole = Qt.UserRole


class MainWindow(GuiWindow[MainWindowView]):
    @log_func_call
    def __init__(self):
        super().__init__(f'{PyCountdownApp.APP_NAME} v{__version__}')
        self.refresh_clocks_file()
        self.clock_tick()
        self.create_timers()

    def create_gui_view(self, basetitle: str, *args,
                        **kwargs) -> MainWindowView:
        return MainWindowView(basetitle, self, *args, **kwargs)

    @log_func_call
    def create_timers(self):
        qtobj = self.gui_view.qtobj

        master_timer = QTimer(qtobj)
        # master_timer.setSingleShot(True)
        master_timer.setInterval(1000)
        master_timer.timeout.connect(qt_callback(self.clock_tick))
        master_timer.start()
        self.master_timer = master_timer

        clocks_file_timer = QTimer(qtobj)
        clocks_file_timer.setInterval(PyCountdownApp[CLOCKS_FILE_CHECK_SEC_KEY]*1000)  # noqa: E501
        clocks_file_timer.timeout.connect(qt_callback(self.refresh_clocks_file))  # noqa: E501
        clocks_file_timer.start()
        self.clocks_file_timer = clocks_file_timer

    @log_func_call
    def click_config(self):
        dlg = ConfigTreeDialog(self)
        dlg.show()

    @log_func_call
    def click_clocks_config(self):
        dlg = ClocksConfigDialog(self)
        dlg.show()

    def set_save_path_if_unset(self):
        clocks_file = PyCountdownApp.get_clocks_file_path()
        if clocks_file and clocks_file.exists():
            return True
        new_pathstr, filter = QFileDialog.getSaveFileName(
            self.gui_view.qtobj, "Export Clocks File",
            '.', "*.jsonc"
        )
        if new_pathstr:
            clocks_file = Path(new_pathstr)
            clocks_file.touch(exist_ok=True)
            PyCountdownApp.set_clocks_file_path(clocks_file)
            return True

    @log_func_call
    def click_saveas(self):
        current_file = PyCountdownApp.get_clocks_file_path()
        default_dir = current_file.parent.as_posix() if current_file else "."
        new_pathstr, filter = QFileDialog.getSaveFileName(
            self.gui_view.qtobj, "Export Clocks File",
            default_dir, "*.jsonc"
        )
        if new_pathstr:
            PyCountdownApp.export_clocks_file(new_pathstr)

    @log_func_call
    def click_open(self):
        current_file = PyCountdownApp.get_clocks_file_path()
        default_dir = current_file.parent.as_posix() if current_file else "."
        open_pathstr, filter = QFileDialog.getOpenFileName(
            self.gui_view.qtobj, "Open Clocks File",
            default_dir, "*.jsonc"
        )
        if open_pathstr:
            PyCountdownApp.set_clocks_file_path(open_pathstr)
            self.refresh_clocks_file(True)

    @log_func_call
    def click_new(self):
        PyCountdownApp.set_clocks_file_path(clear=True)
        self.refresh_clocks_file(True)

    @log_func_call(DEBUGLOW2)
    def clock_tick(self):
        # timestr = sec_to_ymdhms_str(unix_to_central(now_unix_sec()))
        # log_info(f"tock: {timestr}")
        now = now_tai_sec()

        table = self.gui_view.clock_table
        for i in range(table.rowCount()):
            labelitem = table.item(i, 0)
            item = table.item(i, 1)
            clk: DisplayClock = item.data(UserRole)
            txt = ''
            if clk:
                txt = clk.display(now)
                color = clk.formatter.get_color(clk, now)
                item.setTextColor(color)
                labelitem.setTextColor(color)

            item.setText(txt)

    @log_func_call(DEBUGLOW2)
    def refresh_clocks_file(self, force: bool = False):
        logfunc = log_info if force else log_debuglow
        logfunc('checking clocks file')
        if PyCountdownApp.check_clocks_file(force):
            log_info('clocks file reloaded')
            self.update_table()

    @log_func_call(DEBUGLOW2)
    def update_table(self):
        self.gui_view.populate_clock_table()
        self.clock_tick()

    @log_func_call
    def row_header_clicked(self, row: int, col: int):
        """
        Called when a row header is clicked. Copies the reconstructed
        original log line to the clipboard.
        """
        table = self.gui_view.clock_table
        # items = [table.item(row, col) for col in range(table.columnCount())]
        dclk = table.item(row, 1).data(UserRole)
        # idx = DisplayClock.get_idx_for_visible_idx(row)
        # log_info(f'Row {row + 1} Index {idx} clicked')

        dlg = ClockEditorDialog(self, dclk)
        #                        dclk or DisplayClock(None, None, None,
        #                                             ClockFormatter(None)))
        dlg.show()

    @log_func_call
    def add_clock(self):
        dlg = ClockEditorDialog(self)
        dlg.show()
        self.update_table()

    @log_func_call
    def add_timer(self):
        # DisplayClock.add_to_pool(DisplayClock(
        #     'New clock', Clock(DEFAULT_CLOCKS['TAI'], now_tai_sec())))
        dlg = ClockEditorDialog(self, timer=True)
        dlg.show()
        self.update_table()

    @log_func_call
    def remove_clock(self, rows: int | list[int] = None):
        view = self.gui_view
        table = view.clock_table
        if rows is None:
            rows = list({item.row() for item in table.selectedItems()})

        elif isinstance(rows, int):
            rows = [rows]

        r_dclks: list[tuple[int, DisplayClock]] = [
            (r, table.item(r, 1).data(UserRole)) for r in rows
        ]
        if r_dclks:
            msg = "Are you sure you want to remove the selected clock(s)?\n"
            labels = [f"{r + 1}: {repr(dc.label) if dc.label else '(blank)'}"
                      for r, dc in r_dclks]
            msg += ", ".join(labels)
            reply = QMessageBox.warning(view.qtobj, "Remove Clock", msg,
                                        QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return

        for r, dc in r_dclks:
            log_info(f"Removing clock {dc.label!r} at row index {r}")
            DisplayClock.pool.remove(dc)

        PyCountdownApp.export_clocks_file()
        self.refresh_clocks_file(True)
        return True

    @log_func_call
    def duplicate(self, rows: int | list[int] = None):
        view = self.gui_view
        table = view.clock_table
        if rows is None:
            rows = list({item.row() for item in table.selectedItems()})

        elif isinstance(rows, int):
            rows = [rows]

        if not rows:
            return
        DisplayClock.duplicate_subpool([table.item(r, 1).data(UserRole)
                                        for r in rows])
        PyCountdownApp.export_clocks_file()
        self.refresh_clocks_file(True)

    @log_func_call
    def toggle_show_hidden(self, checked: bool):
        PyCountdownApp.set(LOCAL_SHOW_HIDDEN_KEY, checked)
        self.update_table()

    @log_func_call
    def click_threshold_sets(self):
        dlg = ThreshSetEditorDialog(self)
        dlg.show()

    @log_func_call
    def move_up(self, rows: int | list[int] = None):
        view = self.gui_view
        table = view.clock_table
        if rows is None:
            rows = list({item.row() for item in table.selectedItems()})

        elif isinstance(rows, int):
            rows = [rows]

        if not rows:
            return
        DisplayClock.move_up([table.item(r, 1).data(UserRole) for r in rows])
        PyCountdownApp.export_clocks_file()
        self.refresh_clocks_file(True)

    @log_func_call
    def move_down(self, rows: int | list[int] = None):
        view = self.gui_view
        table = view.clock_table
        if rows is None:
            rows = list({item.row() for item in table.selectedItems()})

        elif isinstance(rows, int):
            rows = [rows]

        if not rows:
            return
        DisplayClock.move_down([table.item(r, 1).data(UserRole) for r in rows])
        PyCountdownApp.export_clocks_file()
        self.refresh_clocks_file(True)

    @log_func_call
    def click_apply_tset(self, rows: int | list[int] = None):
        view = self.gui_view
        table = view.clock_table
        if rows is None:
            rows = list({item.row() for item in table.selectedItems()})

        elif isinstance(rows, int):
            rows = [rows]

        r_dclks: list[tuple[int, DisplayClock]] = [
            (r, table.item(r, 1).data(UserRole)) for r in rows
        ]
        if r_dclks:
            dlg = ApplyTSetDialog(self, r_dclks)
            dlg.show()
