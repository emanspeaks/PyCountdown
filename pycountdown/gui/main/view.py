from typing import TYPE_CHECKING

from pyrandyos.gui.qt import (
    QVBoxLayout, Qt, QToolBar, QTableWidget, QTableWidgetItem, QHeaderView,
    QFont,
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
from ...lib.clocks import Clock, DEFAULT_CLOCKS
from ...lib.timeutils import ymdhms_to_sec
from ..gui_icons import ConfigIcon
if TYPE_CHECKING:
    from .pres import MainWindow

UserRole = Qt.UserRole

MONO_FONT = QFont("Consolas, Monaco, monospace")
MONO_FONT.setStyleHint(QFont.Monospace)
TABLE_TPAD = 2  # one sided
TABLE_LPAD = 4  # one sided
TABLE_VPAD = TABLE_TPAD*2  # two sided
TABLE_HPAD = TABLE_LPAD*2  # two sided
TABLE_CELL_STYLE = f"QTableWidget {{ background-color: black; }} QTableWidget::item {{ padding: {TABLE_TPAD}px {TABLE_LPAD}px; background-color: black; }}"  # noqa: E501


class MainWindowView(GuiWindowView['MainWindow', GuiViewBaseFrame]):
    @log_func_call
    def __init__(self, basetitle: str, presenter: 'MainWindow' = None):
        super().__init__(basetitle, presenter)
        qtobj = self.qtobj
        qtobj.resize(*PyCountdownApp.get_default_win_size())
        # qtobj.setMinimumSize(900, 600)

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

        toolbar.addWidget(create_toolbar_expanding_spacer())

        toolbar.addAction(create_action(qtobj, "Config", ConfigIcon.icon(),
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
        self.populate_clock_table(defaults=True)

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

        table.setStyleSheet(TABLE_CELL_STYLE)
        table.setSortingEnabled(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make readonly
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

        vheader = table.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader.sectionClicked.connect(qt_callback(pres.row_header_clicked))

    @log_func_call
    def populate_clock_table(self, content: tuple[Clock] = None,
                             defaults: bool = False):
        table = self.clock_table

        if defaults:
            content = (
                ('UTC', DEFAULT_CLOCKS['UTC']),
                ('Central', DEFAULT_CLOCKS['US CT']),
                # ('Eastern', DEFAULT_CLOCKS['US ET']),
                # ('TDB', DEFAULT_CLOCKS['TDB']),
                # ('TDT', DEFAULT_CLOCKS['TDT']),
                # ('Unix', DEFAULT_CLOCKS['Unix']),
                ('GPST', DEFAULT_CLOCKS['GPST']),
                ('LP17 First Open',
                 Clock(DEFAULT_CLOCKS['UTC'],
                       ymdhms_to_sec(2026, 2, 7, 2, 41, 0))),
                ('Inauguration',
                 Clock(DEFAULT_CLOCKS['US ET'],
                       ymdhms_to_sec(2029, 1, 20, 12, 0, 0))),
                ('Thanksgiving',
                 Clock(DEFAULT_CLOCKS['US CT'],
                       ymdhms_to_sec(2025, 11, 27, 0, 0, 0))),
            )

        rowcount = len(content)
        table.setRowCount(rowcount)
        for i, row in enumerate(content):
            item = QTableWidgetItem(row[0])
            item.setFont(MONO_FONT)
            table.setItem(i, 0, item)

            item = QTableWidgetItem("Loading...")
            item.setData(UserRole, row[1])
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setFont(MONO_FONT)
            table.setItem(i, 1, item)
