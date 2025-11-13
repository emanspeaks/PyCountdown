from pyrandyos.gui.qt import QTimer
from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.window import GuiWindow
from pyrandyos.gui.dialogs.config import ConfigTreeDialog

from ...version import __version__
from ...logging import log_func_call, DEBUGLOW2, log_info
from ...app import PyCountdownApp
from ...lib.timeutils import unix_to_central, now_unix_sec, sec_to_ymdhms_str

from .view import MainWindowView


class MainWindow(GuiWindow[MainWindowView]):
    @log_func_call
    def __init__(self):
        super().__init__(f'{PyCountdownApp.APP_NAME} v{__version__}')
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
        log_info(f"tock: {sec_to_ymdhms_str(unix_to_central(now_unix_sec()))}")
