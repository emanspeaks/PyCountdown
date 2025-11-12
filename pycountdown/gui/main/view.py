from typing import TYPE_CHECKING

from pyrandyos.gui.qt import (
    QVBoxLayout, Qt, QToolBar,
    # QComboBox, QListView, QLineEdit, QShortcut, QKeySequence,
)
# from pyrandyos.gui.callback import qt_callback
from pyrandyos.gui.window import GuiWindowView
from pyrandyos.gui.widgets.viewbase import GuiViewBaseFrame
from pyrandyos.gui.widgets.statusbar import LoggingStatusBarWidget
from pyrandyos.gui.loadstatus import load_status_step
from pyrandyos.gui.utils import (
    create_action, create_toolbar_expanding_spacer,
    # set_widget_sizepolicy_h_expanding, show_toolbtn_icon_and_text
)

from ...app import PyCountdownApp
from ...logging import log_func_call
from ..gui_icons import ConfigIcon  # , CopyCodeIcon, CopyNameIcon
# from ..constants import (
#     ALL_COLLECTIONS, DEFAULT_VIEW_COLUMNS, VIEW_COLUMNS_OPTIONS
# )
# from .iconlistview import IconListView
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
        # self.create_icon_list_view()
        # self.set_tab_order()
        # self.setup_shortcuts()

        # self.lineEditFilter.setFocus()
        self.center_window_in_current_screen()
        # self.gui_pres.updateStyle(self.comboStyle.currentText())

    @load_status_step("Creating toolbars")
    @log_func_call
    def create_toolbars(self):
        # self.create_filter_toolbar()
        self.create_main_toolbar()
        # self.create_view_toolbar()

    # @log_func_call
    # def create_filter_toolbar(self):
    #     qtobj = self.qtobj
    #     pres = self.gui_pres

    #     toolbar = QToolBar("Filters", qtobj)
    #     qtobj.addToolBar(Qt.TopToolBarArea, toolbar)
    #     qtobj.addToolBarBreak()
    #     self.filter_toolbar = toolbar

    #     comboFont = QComboBox()
    #     comboFont.setToolTip(
    #         "Select the font prefix whose icons will be included in "
    #         "the filtering."
    #     )
    #     comboFont.setMaximumWidth(125)
    #     comboFont.addItems([ALL_COLLECTIONS]
    #                        + sorted(pres.get_font_names()))
    #     comboFont.currentIndexChanged.connect(
    #         qt_callback(pres.triggerImmediateUpdate)
    #     )
    #     comboFont = comboFont
    #     self.comboFont = comboFont
    #     toolbar.addWidget(comboFont)

    #     lineEditFilter = QLineEdit()
    #     lineEditFilter.setToolTip("Filter icons by name")
    #     lineEditFilter.setMinimumWidth(200)
    #     # lineEditFilter.setMaximumWidth(400)
    #     set_widget_sizepolicy_h_expanding(lineEditFilter)
    #     lineEditFilter.setAlignment(Qt.AlignLeft)
    #     lineEditFilter.textChanged.connect(
    #         qt_callback(pres.filter_text_changed)
    #     )
    #     lineEditFilter.returnPressed.connect(
    #         qt_callback(pres.triggerImmediateUpdate)
    #     )
    #     lineEditFilter.setClearButtonEnabled(True)
    #     lineEditFilter.setPlaceholderText("Search icons")
    #     self.lineEditFilter = lineEditFilter
    #     toolbar.addWidget(lineEditFilter)

    @log_func_call
    def create_main_toolbar(self):
        qtobj = self.qtobj
        pres = self.gui_pres

        toolbar = QToolBar("Main", qtobj)
        qtobj.addToolBar(Qt.TopToolBarArea, toolbar)
        self.name_toolbar = toolbar

        # # Icon name section
        # nameField = QLineEdit()
        # nameField.setPlaceholderText(
        #     "(Full identifier of the currently selected icon)"
        # )
        # nameField.setAlignment(Qt.AlignCenter)
        # nameField.setReadOnly(True)
        # nameField.setFixedWidth(400)
        # fnt = nameField.font()
        # fnt.setFamily("monospace")
        # fnt.setBold(True)
        # nameField.setFont(fnt)
        # self.nameField = nameField
        # toolbar.addWidget(nameField)

        # toolbar.addSeparator()

        # copyButton = create_action(qtobj, "Copy Name", CopyNameIcon.icon(),
        #                            pres.copyIconText, enabled=False,
        #                            tooltip="Copy selected icon "
        #                            "full identifier to the clipboard")
        # self.copyButton = copyButton
        # toolbar.addAction(copyButton)
        # show_toolbtn_icon_and_text(toolbar.widgetForAction(copyButton))

        # copyPyRandyOSButton = create_action(qtobj, "Copy PyRandyOS Code",
        #                                     CopyCodeIcon.icon(),
        #                                     pres.copyIconPyRandyOSCode,
        #                                     enabled=False,
        #                                     tooltip="Copy selected icon "
        #                                     "PyRandyOS code to the "
        #                                     "clipboard")
        # self.copyPyRandyOSButton = copyPyRandyOSButton
        # toolbar.addAction(copyPyRandyOSButton)
        # widget = toolbar.widgetForAction(copyPyRandyOSButton)
        # show_toolbtn_icon_and_text(widget)

        # @log_func_call
        # def create_view_toolbar(self):
        # qtobj = self.qtobj
        # ctrl = self.controller
        # app = self.gui_app

        # toolbar = QToolBar("View", qtobj)
        # qtobj.addToolBar(Qt.TopToolBarArea, toolbar)
        # self.view_toolbar = toolbar

        toolbar.addWidget(create_toolbar_expanding_spacer())

        # # Display (columns number) section
        # comboColumns = QComboBox()
        # comboColumns.setToolTip(
        #     "Select number of columns the icons list is showing"
        # )
        # for num_columns in VIEW_COLUMNS_OPTIONS:
        #     comboColumns.addItem(str(num_columns), num_columns)
        # comboColumns.setCurrentIndex(
        #     comboColumns.findData(DEFAULT_VIEW_COLUMNS)
        # )
        # comboColumns.currentTextChanged.connect(
        #     qt_callback(pres.updateColumns)
        # )
        # comboColumns.setMinimumWidth(75)
        # self.comboColumns = comboColumns
        # toolbar.addWidget(comboColumns)

        # # Style section
        # comboStyle = QComboBox()
        # comboStyle.setToolTip(
        #     "Select color palette for the icons and the icon browser"
        # )
        # current_theme = app.get_theme()
        # theme_idx = None
        # themes = app.themes.list_themes(always_include_qdarkstyle=True)
        # for i, t in enumerate(sorted(themes)):
        #     comboStyle.addItem(t, i)
        #     if t == current_theme:
        #         theme_idx = i

        # comboStyle.setCurrentIndex(theme_idx if theme_idx is not None else 0)
        # comboStyle.currentTextChanged.connect(qt_callback(pres.updateStyle))
        # comboStyle.setMinimumWidth(100)
        # self.comboStyle = comboStyle
        # toolbar.addWidget(comboStyle)

        toolbar.addAction(create_action(qtobj, "Config", ConfigIcon.icon(),
                                        pres.click_config))

    @log_func_call
    def create_basewidget(self):
        return GuiViewBaseFrame(self)

    # @log_func_call
    # def create_icon_list_view(self):
    #     pres = self.gui_pres
    #     listview = IconListView(DEFAULT_VIEW_COLUMNS, self)
    #     self.listView = listview

    #     lvwidget = listview.qtobj
    #     lvwidget.setUniformItemSizes(True)
    #     lvwidget.setViewMode(QListView.IconMode)
    #     lvwidget.setModel(pres.proxyModel)
    #     lvwidget.setContextMenuPolicy(Qt.CustomContextMenu)
    #     lvwidget.doubleClicked.connect(qt_callback(pres.doubleClickIcon))
    #     selmodel = lvwidget.selectionModel()
    #     selmodel.selectionChanged.connect(qt_callback(pres.updateNameField))
    #     self.layout.addWidget(lvwidget)

    # @log_func_call
    # def set_tab_order(self):
    #     qtobj = self.qtobj
    #     qtobj.setTabOrder(self.comboFont, self.lineEditFilter)
    #     qtobj.setTabOrder(self.lineEditFilter, self.comboColumns)
    #     qtobj.setTabOrder(self.comboColumns, self.comboStyle)
    #     qtobj.setTabOrder(self.comboStyle, self.listView.qtobj)
    #     qtobj.setTabOrder(self.listView.qtobj, self.nameField)
    #     qtobj.setTabOrder(self.nameField, self.comboFont)

    # @log_func_call
    # def setup_shortcuts(self):
    #     # Shortcuts
    #     pres = self.gui_pres
    #     qtobj = self.qtobj
    #     QShortcut(QKeySequence(Qt.Key_Return), qtobj, pres.copyIconText)
    #     QShortcut(QKeySequence("Ctrl+F"), qtobj,
    #               self.lineEditFilter.setFocus)
