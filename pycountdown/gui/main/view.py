from typing import TYPE_CHECKING
from functools import partial

from pyrandyos.gui.qt import (
    QVBoxLayout, Qt, QToolBar, QTableWidget, QTableWidgetItem, QHeaderView,
    QFont, QObject, QEvent, QMainWindow
)
from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.window import GuiWindowView
from pyrandyos.gui.widgets.viewbase import GuiViewBaseFrame
from pyrandyos.gui.widgets.statusbar import LoggingStatusBarWidget
from pyrandyos.gui.loadstatus import load_status_step
from pyrandyos.gui.utils import (
    create_action, create_toolbar_expanding_spacer,  # show_toolbtn_icon_and_text,  # noqa: E501
)

from ...app import PyCountdownApp
from ...logging import log_func_call
from ...lib.clocks.displayclocks import DisplayClock
from ..gui_icons import (
    ConfigIcon, AddClockIcon, RemoveClockIcon, RefreshIcon, ClocksJsonIcon,
    SaveAsIcon, TimerIcon,
)
if TYPE_CHECKING:
    from .pres import MainWindow

UserRole = Qt.UserRole

MONO_FONT = QFont("Consolas, Monaco, monospace")
MONO_FONT.setStyleHint(QFont.Monospace)
TABLE_TPAD = 2  # one sided
TABLE_LPAD = 4  # one sided
TABLE_VPAD = TABLE_TPAD*2  # two sided
TABLE_HPAD = TABLE_LPAD*2  # two sided
TABLE_CELL_PADDING = f'padding: {TABLE_TPAD}px {TABLE_LPAD}px;'
# TABLE_CELL_DEFAULT_STYLE = 'background-color: black; color: white;'
TABLE_CELL_DEFAULT_STYLE = 'background-color: black;'
TABLE_STYLE = f"QTableWidget {{ background-color: black; }} QTableWidget::item {{ {TABLE_CELL_PADDING} {TABLE_CELL_DEFAULT_STYLE}  }}"  # noqa: E501


class MainWindowFocusFilter(QObject):
    def eventFilter(self, qtobj: QMainWindow, event: QEvent):
        if event.type() == QEvent.Type.WindowActivate:
            qtobj.setWindowOpacity(1)

        elif event.type() == QEvent.Type.WindowDeactivate:
            always_on_top = PyCountdownApp.get("local.always_on_top", False)
            if always_on_top:
                opacity = PyCountdownApp.get('local.always_on_top_opacity', 1)
                qtobj.setWindowOpacity(opacity)

        return False  # Continue standard event processing


class MainWindowView(GuiWindowView['MainWindow', GuiViewBaseFrame]):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'MainWindow' = None):
        super().__init__(basetitle, presenter)
        qtobj = self.qtobj
        qtobj.resize(*PyCountdownApp.get_default_win_size())
        qtobj.setMinimumSize(325, 140)
        qtobj.setWindowFlag(Qt.WindowStaysOnTopHint,
                            PyCountdownApp.get("local.always_on_top", False))

        focus_filter = MainWindowFocusFilter(qtobj)
        qtobj.installEventFilter(focus_filter)
        self.focus_filter = focus_filter

        layout = QVBoxLayout()
        self.layout = layout
        self.basewidget.qtobj.setLayout(layout)

        self.status_bar = LoggingStatusBarWidget(self)

        self.create_toolbars()
        self.create_clock_table()
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

        toolbar.addAction(create_action(qtobj, "Refresh from file",
                                        RefreshIcon.icon(),
                                        partial(pres.refresh_clocks_file, True)))  # noqa: E501
        toolbar.addAction(create_action(qtobj, "Add timer",
                                        TimerIcon.icon(),
                                        pres.add_timer))
        toolbar.addAction(create_action(qtobj, "Add clock",
                                        AddClockIcon.icon(),
                                        pres.add_clock, enabled=False))
        toolbar.addAction(create_action(qtobj, "Remove clock",
                                        RemoveClockIcon.icon(),
                                        pres.remove_clock, enabled=False))

        toolbar.addSeparator()
        toolbar.addAction(create_action(qtobj, "Save Clocks File As...",
                                        SaveAsIcon.icon(),
                                        pres.click_saveas))

        toolbar.addWidget(create_toolbar_expanding_spacer())

        toolbar.addAction(create_action(qtobj, "Clocks Config",
                                        ClocksJsonIcon.icon(),
                                        pres.click_clocks_config))
        toolbar.addAction(create_action(qtobj, "Program Config",
                                        ConfigIcon.icon(),
                                        pres.click_config))

    @log_func_call
    def create_basewidget(self):
        return GuiViewBaseFrame(self)

    @log_func_call
    def create_clock_table(self):
        layout = self.layout

        clock_table = QTableWidget()
        layout.addWidget(clock_table)
        self.clock_table = clock_table
        self.setup_clock_table()
        self.populate_clock_table()

    @log_func_call
    def setup_clock_table(self):
        pres = self.gui_pres
        table = self.clock_table

        header = table.horizontalHeader()

        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, QTableWidgetItem('Clock'))
        table.setHorizontalHeaderItem(1, QTableWidgetItem('Current Time'))

        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.setStretchLastSection(True)

        table.setStyleSheet(TABLE_STYLE)
        # table.setStyleSheet("")
        table.setSortingEnabled(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make readonly
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

        vheader = table.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader.sectionClicked.connect(qt_callback(pres.row_header_clicked))

    @log_func_call
    def populate_clock_table(self):
        table = self.clock_table
        clocks = [x for x in DisplayClock.pool if x is None or not x.hidden]
        rowcount = len(clocks)
        table.clearContents()
        table.setRowCount(rowcount)
        for i, row in enumerate(clocks):
            item = QTableWidgetItem(row.label if row else '')
            item.setFont(MONO_FONT)
            table.setItem(i, 0, item)

            item = QTableWidgetItem("Loading...")
            item.setData(UserRole, row)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setFont(MONO_FONT)
            table.setItem(i, 1, item)
