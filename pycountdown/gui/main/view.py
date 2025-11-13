from typing import TYPE_CHECKING

from pyrandyos.gui.qt import (
    QVBoxLayout, Qt, QToolBar,
)
# from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.window import GuiWindowView
from pyrandyos.gui.widgets.viewbase import GuiViewBaseFrame
from pyrandyos.gui.widgets.statusbar import LoggingStatusBarWidget
from pyrandyos.gui.loadstatus import load_status_step
from pyrandyos.gui.utils import (
    create_action, create_toolbar_expanding_spacer,  # show_toolbtn_icon_and_text,  # noqa: E501
)

from ...app import PyCountdownApp
from ...logging import log_func_call
from ..gui_icons import ConfigIcon
if TYPE_CHECKING:
    from .pres import MainWindow


class MainWindowView(GuiWindowView['MainWindow', GuiViewBaseFrame]):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'MainWindow' = None):
        super().__init__(basetitle, presenter)
        qtobj = self.qtobj
        qtobj.resize(*PyCountdownApp.get_default_win_size())
        qtobj.setMinimumSize(900, 600)

        layout = QVBoxLayout()
        self.layout = layout
        self.basewidget.qtobj.setLayout(layout)

        self.status_bar = LoggingStatusBarWidget(self)

        self.create_toolbars()
        self.center_window_in_current_screen()

    @load_status_step("Creating toolbars")
    @log_func_call
    def create_toolbars(self):
        self.create_main_toolbar()

    @log_func_call
    def create_main_toolbar(self):
        qtobj = self.qtobj
        pres = self.gui_pres

        toolbar = QToolBar("Main", qtobj)
        qtobj.addToolBar(Qt.TopToolBarArea, toolbar)
        self.name_toolbar = toolbar

        toolbar.addWidget(create_toolbar_expanding_spacer())

        toolbar.addAction(create_action(qtobj, "Config", ConfigIcon.icon(),
                                        pres.click_config))

    @log_func_call
    def create_basewidget(self):
        return GuiViewBaseFrame(self)
