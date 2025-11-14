from pyrandyos.gui.qt import QTimer, Qt
from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.window import GuiWindow
from pyrandyos.gui.dialogs.config import ConfigTreeDialog

from ...version import __version__
from ...logging import log_func_call, DEBUGLOW2, log_info
from ...app import PyCountdownApp
from ...lib.clocks import Clock
from ...lib.timeutils import now_tai_sec

from .view import MainWindowView

UserRole = Qt.UserRole


class MainWindow(GuiWindow[MainWindowView]):
    @log_func_call
    def __init__(self):
        super().__init__(f'{PyCountdownApp.APP_NAME} v{__version__}')
        self.clock_tick()
        self.create_timer()

    def create_gui_view(self, basetitle: str, *args,
                        **kwargs) -> MainWindowView:
        return MainWindowView(basetitle, self, *args, **kwargs)

    @log_func_call
    def create_timer(self):
        master_timer = QTimer(self.gui_view.qtobj)
        # master_timer.setSingleShot(True)
        master_timer.setInterval(1000)
        master_timer.timeout.connect(qt_callback(self.clock_tick))
        master_timer.start()
        self.master_timer = master_timer

    @log_func_call
    def click_config(self):
        dlg = ConfigTreeDialog(self)
        dlg.show()

    @log_func_call(DEBUGLOW2)
    def clock_tick(self):
        # timestr = sec_to_ymdhms_str(unix_to_central(now_unix_sec()))
        # log_info(f"tock: {timestr}")
        now = now_tai_sec()

        table = self.gui_view.clock_table
        for i in range(table.rowCount()):
            item = table.item(i, 1)
            clk: Clock = item.data(UserRole)
            item.setText(clk.display(now))

    @log_func_call
    def row_header_clicked(self, row: int) -> None:
        """
        Called when a row header is clicked. Copies the reconstructed
        original log line to the clipboard.
        """
        table = self.gui_view.clock_table
        items = [table.item(row, col) for col in range(table.columnCount())]
        items
        log_info(f'Row {row} clicked')
        # get_gui_app().qtobj.clipboard().setText(log_line)
