from functools import partial

from pyrandyos.gui.qt import (
    QGroupBox, QHBoxLayout, QLineEdit, QIntValidator, QPushButton, QLabel,
    QDoubleValidator, QShortcut, QKeySequence, Qt,
)
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType
from pyrandyos.gui.callback import qt_callback

from ...logging import log_func_call


class DhmsWidget(QtWidgetWrapper[QGroupBox]):
    def __init__(self, gui_parent: GuiWidgetParentType = None,
                 d: int = 0, h: int = 0, m: int = 0, s: int = 0, sign: int = 1,
                 *qtobj_args, **qtobj_kwargs):
        self.set_dhms(d, h, m, s, sign, False)
        super().__init__(gui_parent, *qtobj_args, **qtobj_kwargs)

    @log_func_call
    def create_qtobj(self):
        parent_qtobj: GuiWidgetParentType = self.gui_parent.qtobj

        frame = QGroupBox(parent_qtobj)
        frame.setTitle('DHMS')
        frame.setMaximumWidth(275)
        frame.setMaximumHeight(60)
        self.frame = frame

        layout = QHBoxLayout()
        frame.setLayout(layout)
        self.layout = layout

        sign_btn = QPushButton(frame)
        sign_btn.setFixedWidth(20)
        sign_btn.setCheckable(True)
        sign_btn.toggled.connect(qt_callback(self.on_sign_toggle))
        layout.addWidget(sign_btn)
        self.sign_btn = sign_btn

        d_txt = QLineEdit(frame)
        d_txt.setValidator(QIntValidator(bottom=0))
        d_txt.setFixedWidth(40)
        layout.addWidget(d_txt)
        self.d_txt = d_txt

        layout.addWidget(QLabel('/'))

        h_txt = QLineEdit(frame)
        h_txt.setValidator(QIntValidator(0, 23))
        h_txt.setMaxLength(2)
        h_txt.setFixedWidth(35)
        layout.addWidget(h_txt)
        self.h_txt = h_txt

        layout.addWidget(QLabel(':'))

        m_txt = QLineEdit(frame)
        m_txt.setValidator(QIntValidator(0, 59))
        m_txt.setMaxLength(2)
        m_txt.setFixedWidth(35)
        layout.addWidget(m_txt)
        self.m_txt = m_txt

        layout.addWidget(QLabel(':'))

        s_txt = QLineEdit(frame)
        s_txt.setValidator(QDoubleValidator(0.0, 61.0, 3))
        s_txt.setMaxLength(6)
        s_txt.setFixedWidth(55)
        layout.addWidget(s_txt)
        self.s_txt = s_txt

        self.update_text()
        self.create_shortcuts()
        return frame

    @log_func_call
    def create_shortcuts(self):
        # gui_parent = self.gui_parent
        # qtwin: QDialog = gui_parent.qtobj
        frame = self.frame
        sign_btn = self.sign_btn

        plus_shortcut = QShortcut(QKeySequence(Qt.Key_Plus), sign_btn)
        plus_shortcut.activated.connect(qt_callback(partial(self.set_sign,
                                                            False)))
        self.plus_shortcut = plus_shortcut

        minus_shortcut = QShortcut(QKeySequence(Qt.Key_Minus), sign_btn)
        minus_shortcut.activated.connect(qt_callback(partial(self.set_sign,
                                                             True)))
        self.minus_shortcut = minus_shortcut

        slash_shortcut = QShortcut(QKeySequence(Qt.Key_Slash), frame)
        slash_shortcut.activated.connect(qt_callback(frame.nextInFocusChain))
        self.slash_shortcut = slash_shortcut

    @log_func_call
    def on_sign_toggle(self, checked: bool):
        if checked:
            self.sign = -1
            self.sign_btn.setText('-')

        else:
            self.sign = 1
            self.sign_btn.setText('+')

    def get_dhms(self):
        return [int(self.d_txt.text()),
                int(self.h_txt.text()),
                int(self.m_txt.text()),
                float(self.s_txt.text()),
                self.sign]

    def set_dhms(self, d: int, h: int, m: int, s: float, sign: int,
                 update_text: bool = True):
        self.d = d
        self.h = h
        self.m = m
        self.s = s
        self.sign = sign
        if update_text:
            self.update_text()

    def set_sign(self, minus: bool):
        self.sign = 1 - 2*minus
        self.sign_btn.setChecked(minus)
        self.on_sign_toggle(minus)

    def update_text(self):
        self.d_txt.setText(str(self.d))
        self.h_txt.setText(str(self.h))
        self.m_txt.setText(str(self.m))
        self.s_txt.setText(str(self.s))
        self.set_sign(self.sign < 0)
