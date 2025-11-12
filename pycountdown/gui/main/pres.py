# from pyrandyos.gui.qt import (
#     QTimer, QSortFilterProxyModel, Qt, QItemSelection, QModelIndex,
# )
# from pyrandyos.gui.callback import qt_callback
# from pyrandyos.gui.icons.iconfont.sources import THIRDPARTY_FONTSPEC
# from pyrandyos.gui.icons.utils import legalize_iconname
from pyrandyos.gui.window import GuiWindow
from pyrandyos.gui.dialogs.config import ConfigTreeDialog

from ...version import __version__
from ...logging import log_func_call  # , DEBUGLOW2, log_info
from ...app import PyCountdownApp
# from ..constants import AUTO_SEARCH_TIMEOUT, ALL_COLLECTIONS
# from ..utils import iconstring_to_specname_iconname

from .view import MainWindowView
# from .iconmodel import IconModel


class MainWindow(GuiWindow[MainWindowView]):
    @log_func_call
    def __init__(self):
        # need filter models before creating the view
        # self.create_filter_models()
        super().__init__(f'{PyCountdownApp.APP_NAME} v{__version__}')
        # self.create_timer()

    def create_gui_view(self, basetitle: str, *args,
                        **kwargs) -> MainWindowView:
        return MainWindowView(basetitle, self, *args, **kwargs)

    # @log_func_call
    # def create_filter_models(self):
    #     model = IconModel()
    #     model.setStringList(sorted(self.get_icon_names()))

    #     proxyModel = QSortFilterProxyModel()
    #     proxyModel.setSourceModel(model)
    #     proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
    #     self.proxyModel = proxyModel

    # @log_func_call
    # def create_timer(self):
    #     filterTimer = QTimer(self.gui_view.qtobj)
    #     filterTimer.setSingleShot(True)
    #     filterTimer.setInterval(AUTO_SEARCH_TIMEOUT)
    #     filterTimer.timeout.connect(qt_callback(self.updateFilter))
    #     self.filterTimer = filterTimer

    @log_func_call
    def click_config(self):
        dlg = ConfigTreeDialog(self)
        dlg.show()

    # @log_func_call(DEBUGLOW2)
    # def get_icon_names(self):
    #     iconNames = []
    #     for k, v in THIRDPARTY_FONTSPEC.items():
    #         iconNames += [f'{k}:{icon}' for icon in v.charmap.keys()]

    #     return iconNames

    # @log_func_call(DEBUGLOW2, trace_only=True)
    # def get_font_names(self):
    #     return THIRDPARTY_FONTSPEC.keys()

    # @log_func_call(DEBUGLOW2, trace_only=True)
    # def triggerImmediateUpdate(self):
    #     """
    #     Stop the timer used for committing the search term and update the
    #     proxy model immediately.
    #     """
    #     self.filterTimer.stop()
    #     self.updateFilter()

    # @log_func_call(DEBUGLOW2, trace_only=True)
    # def updateFilter(self):
    #     win = self.gui_view
    #     reString = ""

    #     group = win.comboFont.currentText()
    #     if group != ALL_COLLECTIONS:
    #         reString += rf"^{group}:"

    #     searchTerm = win.lineEditFilter.text()
    #     if searchTerm:
    #         reString += rf".*{searchTerm}.*$"

    #     # QSortFilterProxyModel.setFilterRegExp has been removed in Qt 6.
    #     # Instead, QSortFilterProxyModel.setFilterRegularExpression is
    #     # supported in Qt 5.12 or later.
    #     self.proxyModel.setFilterRegularExpression(reString)

    # @log_func_call
    # def doubleClickIcon(self, index: QModelIndex = None):
    #     self.updateNameField()
    #     self.copyIconPyRandyOSCode()

    # @log_func_call
    # def copyIconText(self):
    #     """
    #     Copy the name of the currently selected icon to the clipboard.
    #     """
    #     indexes = self.gui_view.listView.qtobj.selectedIndexes()
    #     if not indexes:
    #         return

    #     clipboard = self.qt_app.clipboard()
    #     name = indexes[0].data()
    #     clipboard.setText(name)
    #     log_info(f'Copied {name} to clipboard')

    # @log_func_call
    # def copyIconPyRandyOSCode(self):
    #     indexes = self.gui_view.listView.qtobj.selectedIndexes()
    #     if not indexes:
    #         return

    #     iconstring = indexes[0].data()
    #     specname, iconname = iconstring_to_specname_iconname(iconstring)
    #     spec = THIRDPARTY_FONTSPEC[specname]
    #     fontmod = spec.module_qualname()
    #     fontclass = spec.classname
    #     shortname = spec.shortname
    #     legalname = legalize_iconname(iconname)

    #     code = ("from pyrandyos.gui.icons.iconfont import IconSpec\n"
    #             f"from {fontmod} import {fontclass}\n"
    #             f"from {fontmod} import names as {shortname}_names  # noqa: E501\n"
    #             # f"{shortname}_{legalname}_ispec = IconSpec.generate_iconspec({fontclass}, glyph_name={iconname!r})  # noqa: E501\n")
    #             f"{shortname}_{legalname}_ispec = IconSpec.generate_iconspec({fontclass}, glyph={shortname}_names.{legalname})  # noqa: E501\n")

    #     clipboard = self.qt_app.clipboard()
    #     clipboard.setText(code)
    #     log_info(f'Copied {iconstring} PyRandyOS code to clipboard')

    # @log_func_call
    # def updateNameField(self, selected: QItemSelection = None,
    #                     deselected: QItemSelection = None):
    #     win = self.gui_view
    #     indexes = win.listView.qtobj.selectedIndexes()
    #     if not indexes:
    #         win.nameField.setText("")
    #         win.copyButton.setDisabled(True)
    #         win.copyPyRandyOSButton.setDisabled(True)
    #         return

    #     win.nameField.setText(indexes[0].data())
    #     win.copyButton.setDisabled(False)
    #     win.copyPyRandyOSButton.setDisabled(False)

    # @log_func_call(DEBUGLOW2, trace_only=True)
    # def triggerDelayedUpdate(self):
    #     self.filterTimer.stop()
    #     self.filterTimer.start()

    # @log_func_call(DEBUGLOW2, trace_only=True)
    # def filter_text_changed(self, text: str):
    #     self.style_placeholder_text()
    #     self.triggerDelayedUpdate()

    # @log_func_call
    # def updateStyle(self, text: str):
    #     # qtawesome.reset_cache()
    #     self.gui_app.set_theme(text)

    # @log_func_call
    # def updateColumns(self):
    #     win = self.gui_view
    #     win.listView.setColumns(win.comboColumns.currentData())

    # @log_func_call(DEBUGLOW2, trace_only=True)
    # def style_placeholder_text(self):
    #     win = self.gui_view
    #     txtbox = win.lineEditFilter
    #     txtbox.style().polish(txtbox)
