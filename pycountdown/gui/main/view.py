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
    UpArrowIcon, DownArrowIcon, CopyIcon, ApplyThreshSetIcon, MuteIcon,
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

        add_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), qtobj)
        add_shortcut.activated.connect(qt_callback(pres.add_clock))
        self.add_shortcut = add_shortcut

        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), qtobj)
        delete_shortcut.activated.connect(qt_callback(pres.remove_clock))
        self.delete_shortcut = delete_shortcut

        copy_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C), qtobj)
        copy_shortcut.activated.connect(qt_callback(pres.copy_clock))
        self.copy_shortcut = copy_shortcut

        move_up_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Up), qtobj)
        move_up_shortcut.activated.connect(qt_callback(pres.move_up))
        self.move_up_shortcut = move_up_shortcut

        move_down_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Down), qtobj)  # noqa: E501
        move_down_shortcut.activated.connect(qt_callback(pres.move_down))
        self.move_down_shortcut = move_down_shortcut

        timer_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), qtobj)
        timer_shortcut.activated.connect(qt_callback(pres.add_timer))
        self.timer_shortcut = timer_shortcut

        hide_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_H), qtobj)
        hide_shortcut.activated.connect(qt_callback(pres.toggle_show_hidden))
        self.hide_shortcut = hide_shortcut

        mute_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), qtobj)
        mute_shortcut.activated.connect(qt_callback(pres.toggle_mute_alerts))
        self.mute_shortcut = mute_shortcut

        edit_shortcut = QShortcut(QKeySequence(Qt.Key_Return), qtobj)
        edit_shortcut.activated.connect(qt_callback(pres.edit_selected_clock))
        self.edit_shortcut = edit_shortcut

        edit_shortcut2 = QShortcut(QKeySequence(Qt.Key_Enter), qtobj)
        edit_shortcut2.activated.connect(qt_callback(pres.edit_selected_clock))
        self.edit_shortcut2 = edit_shortcut2

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
                                        pres.add_clock,
                                        tooltip="Add clock (Ctrl+T)"))
        toolbar.addAction(create_action(qtobj, "Remove clock",
                                        RemoveClockIcon.icon(),
                                        pres.remove_clock,
                                        tooltip="Remove clock (Delete)"))
        toolbar.addAction(create_action(qtobj, "Add timer",
                                        TimerIcon.icon(),
                                        pres.add_timer,
                                        tooltip="Add timer (Ctrl+R)"))
        toolbar.addAction(create_action(qtobj, "Move up",
                                        UpArrowIcon.icon(),
                                        pres.move_up,
                                        tooltip="Move up (Ctrl+Up)"))
        toolbar.addAction(create_action(qtobj, "Move down",
                                        DownArrowIcon.icon(),
                                        pres.move_down,
                                        tooltip="Move down (Ctrl+Down)"))
        toolbar.addAction(create_action(qtobj, "Duplicate",
                                        CopyIcon.icon(),
                                        pres.duplicate,
                                        tooltip="Duplicate (Ctrl+D)"))

        toolbar.addSeparator()
        show_hidden_action = create_action(qtobj, "Show hidden clocks",
                                           ShowHiddenIcon.icon(),
                                           checkable=True)
        show_hidden_action.toggled.connect(qt_callback(pres.toggle_show_hidden))  # noqa: E501
        toolbar.addAction(show_hidden_action)
        self.show_hidden_action = show_hidden_action
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
        toolbar.addAction(create_action(qtobj, "Program config",
                                        ConfigIcon.icon(),
                                        pres.click_config))
        toolbar.addAction(create_action(qtobj, "Clocks config",
                                        ClocksJsonIcon.icon(),
                                        pres.click_clocks_config))
        mute_action = create_action(qtobj, "Mute Alerts",
                                           MuteIcon.icon(),
                                           checkable=True)
        mute_action.toggled.connect(qt_callback(pres.toggle_mute_alerts))
        toolbar.addAction(mute_action)
        self.mute_action = mute_action

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
