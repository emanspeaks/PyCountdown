from pyrandyos.gui.widgets import json_edit
from pyrandyos.gui.qt import (
    QTextCharFormat, QColor, QFont, QRegularExpression, QSyntaxHighlighter,
)
from ....logging import log_func_call, DEBUGLOW2


class JsonHighlighter(json_edit.JsonHighlighter):
    rules: list[tuple[QRegularExpression, QTextCharFormat]]

    @log_func_call(DEBUGLOW2)
    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)
        # self.rules = list()  # this causes Qt to crash
        self.__dict__['rules'] = list()

        # Define styles
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#ce9178"))
        key_format.setFontWeight(QFont.Bold)
        key_regex = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"\s*(?=:)')

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#9cdcfe"))
        string_regex = QRegularExpression(r'(?<=:)\s*"[^"\\]*(\\.[^"\\]*)*"')

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8"))
        number_regex = QRegularExpression(r'\b-?\d+(\.\d+)?([eE][+-]?\d+)?\b')

        boolean_format = QTextCharFormat()
        boolean_format.setForeground(QColor("#569cd6"))
        boolean_regex = QRegularExpression(r'\b(true|false|null)\b')

        self.rules.append((key_regex, key_format))
        self.rules.append((string_regex, string_format))
        self.rules.append((number_regex, number_format))
        self.rules.append((boolean_regex, boolean_format))


json_edit.JsonHighlighter = JsonHighlighter
