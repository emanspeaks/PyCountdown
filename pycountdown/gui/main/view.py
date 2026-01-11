from typing import TYPE_CHECKING
from functools import partial

from pyrandyos.gui.qt import (
    QVBoxLayout, Qt, QToolBar, QTableWidget, QTableWidgetItem, QHeaderView,
    QObject, QEvent, QMainWindow, QShortcut, QKeySequence, QDialog,
)
from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.window import GuiWindowView
from pyrandyos.gui.widgets.viewbase import GuiViewBaseFrame
from pyrandyos.gui.widgets.statusbar import LoggingStatusBarWidget
from pyrandyos.gui.loadstatus import load_status_step
from pyrandyos.gui.utils import (
    create_action, create_toolbar_expanding_spacer,  # show_toolbtn_icon_and_text,  # noqa: E501
)

from ...app import PyCountdownApp, LOCAL_SHOW_HIDDEN_KEY
from ...logging import log_func_call
from ...lib.clocks.displayclocks import DisplayClock
from ..gui_icons import (
    ConfigIcon, AddClockIcon, RemoveClockIcon, RefreshIcon, ClocksJsonIcon,
    SaveAsIcon, TimerIcon, OpenIcon, NewIcon, ShowHiddenIcon, ThresholdSetIcon,
    UpArrowIcon, DownArrowIcon, CopyIcon, ApplyThreshSetIcon,
)
if TYPE_CHECKING:
    from .pres import MainWindow

UserRole = Qt.UserRole

TABLE_TPAD = 2  # one sided
TABLE_LPAD = 4  # one sided
TABLE_VPAD = TABLE_TPAD*2  # two sided
TABLE_HPAD = TABLE_LPAD*2  # two sided
TABLE_CELL_PADDING = f'padding: {TABLE_TPAD}px {TABLE_LPAD}px;'
# TABLE_CELL_DEFAULT_STYLE = 'background-color: black; color: white;'
TABLE_CELL_DEFAULT_STYLE = 'background-color: black;'
TABLE_STYLE = f"QTableWidget {{ background-color: black; }} QTableWidget::item {{ {TABLE_CELL_PADDING} {TABLE_CELL_DEFAULT_STYLE}  }}"  # noqa: E501


class MainWindowEventFilter(QObject):
    def eventFilter(self, qtobj: QMainWindow, event: QEvent):
        if event.type() == QEvent.Type.WindowActivate:
            qtobj.setWindowOpacity(1)

        elif event.type() == QEvent.Type.WindowDeactivate:
            always_on_top = PyCountdownApp.get("local.always_on_top", False)
            if always_on_top:
                opacity = PyCountdownApp.get('local.always_on_top_opacity', 1)
                qtobj.setWindowOpacity(opacity)

        elif event.type() == QEvent.Type.Close:
            # Close all child dialogs when the main window is closed
            for child in qtobj.findChildren(QDialog):
                child.close()

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

        focus_filter = MainWindowEventFilter(qtobj)
        qtobj.installEventFilter(focus_filter)
        self.focus_filter = focus_filter

        layout = QVBoxLayout()
        self.layout = layout
        self.basewidget.qtobj.setLayout(layout)

        self.status_bar = LoggingStatusBarWidget(self)

        self.create_toolbars()
        self.create_clock_table()
        # self.center_window_in_current_screen()
        self.create_shortcuts()

    def create_shortcuts(self):
        qtobj = self.qtobj
        pres = self.gui_pres
        dup_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), qtobj)
        dup_shortcut.activated.connect(qt_callback(pres.duplicate))
        self.dup_shortcut = dup_shortcut

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

        toolbar.addAction(create_action(qtobj, "Add clock",
                                        AddClockIcon.icon(),
                                        pres.add_clock))
        toolbar.addAction(create_action(qtobj, "Remove clock",
                                        RemoveClockIcon.icon(),
                                        pres.remove_clock))
        toolbar.addAction(create_action(qtobj, "Add timer",
                                        TimerIcon.icon(),
                                        pres.add_timer))
        toolbar.addAction(create_action(qtobj, "Move up",
                                        UpArrowIcon.icon(),
                                        pres.move_up))
        toolbar.addAction(create_action(qtobj, "Move down",
                                        DownArrowIcon.icon(),
                                        pres.move_down))
        toolbar.addAction(create_action(qtobj, "Duplicate",
                                        CopyIcon.icon(),
                                        pres.duplicate))

        toolbar.addSeparator()
        show_hidden_action = create_action(qtobj, "Show hidden clocks",
                                           ShowHiddenIcon.icon(),
                                           checkable=True)
        show_hidden_action.toggled.connect(qt_callback(pres.toggle_show_hidden))  # noqa: E501
        toolbar.addAction(show_hidden_action)
        toolbar.addAction(create_action(qtobj, "Threshold Sets",
                                        ThresholdSetIcon.icon(),
                                        pres.click_threshold_sets))
        toolbar.addAction(create_action(qtobj, "Apply Threshold Set...",
                                        ApplyThreshSetIcon.icon(),
                                        pres.click_apply_tset))

        toolbar.addSeparator()
        toolbar.addAction(create_action(qtobj, "Refresh from file",
                                        RefreshIcon.icon(),
                                        partial(pres.refresh_clocks_file, True)))  # noqa: E501
        toolbar.addAction(create_action(qtobj, "New Clocks file",
                                        NewIcon.icon(),
                                        pres.click_new))
        toolbar.addAction(create_action(qtobj, "Open Clocks file...",
                                        OpenIcon.icon(),
                                        pres.click_open))
        toolbar.addAction(create_action(qtobj, "Save Clocks file as...",
                                        SaveAsIcon.icon(),
                                        pres.click_saveas))

        toolbar.addWidget(create_toolbar_expanding_spacer())

        toolbar.addSeparator()
        toolbar.addAction(create_action(qtobj, "Clocks config",
                                        ClocksJsonIcon.icon(),
                                        pres.click_clocks_config))
        toolbar.addAction(create_action(qtobj, "Program config",
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
        table.cellDoubleClicked.connect(qt_callback(pres.row_header_clicked))

    @log_func_call
    def populate_clock_table(self):
        show_hidden = PyCountdownApp.get(LOCAL_SHOW_HIDDEN_KEY)
        table = self.clock_table
        clocks = [x for x in DisplayClock.pool
                  if x is None or not x.hidden or show_hidden]
        rowcount = len(clocks)
        table.clearContents()
        table.setRowCount(rowcount)
        font = self.gui_app.get_monofont()
        for i, row in enumerate(clocks):
            item = QTableWidgetItem(row.label if row else '')
            item.setFont(font)
            table.setItem(i, 0, item)

            clk = row.clock if row else None
            item = QTableWidgetItem("Loading..." if clk else "")
            item.setData(UserRole, row)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setFont(font)
            table.setItem(i, 1, item)
