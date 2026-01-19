from functools import partial
from PySide2.QtWidgets import QCheckBox, QRadioButton

from pyrandyos.gui.qt import (
    QFrame, QVBoxLayout, QHBoxLayout, Qt, QShortcut, QKeySequence, QLabel,
    QWidget,
    # QCheckBox, QRadioButton,
)
from pyrandyos.gui.widgets import QtWidgetWrapper, GuiWidgetParentType
from pyrandyos.gui.callback import qt_callback
from pyrandyos.utils.time.fmt import FLOAT_FMTS, TimeFormat
from pyrandyos.utils.time.now import now_tai_sec

from ...logging import log_func_call, log_warning, log_info
from ...lib.clocks.epoch import Epoch
from ...lib.clocks.displayclocks import NOW_ID, DisplayClock
# from pyrandyos.gui.widgets.time_edit.dhms import DhmsWidget
# from pyrandyos.gui.widgets.time_edit.ymdhms import YmdhmsWidget
# from pyrandyos.gui.widgets.time_edit.y_doy_hms import YDoyHmsWidget
from .time_edit import (
    DhmsWidget, YmdhmsWidget, YDoyHmsWidget, BaseTimeEditorWidget,
)
from .clocklist import ClockListWidget


class EpochWidget(QtWidgetWrapper[QFrame]):
    def __init__(self, gui_parent: GuiWidgetParentType, label: str = 'Epoch:',
                 timer: bool = False, keybd_shortcuts: bool = False,
                 show_clocklist: bool = True,
                 *qtobj_args, **qtobj_kwargs):
        self.label = label
        self.timer = timer
        self.keybd_shortcuts = keybd_shortcuts
        self.epoch_sec = 0
        self.input_fmt = TimeFormat.DHMS
        self.last_clock_id = None
        self.show_clocklist = show_clocklist
        super().__init__(gui_parent, *qtobj_args, **qtobj_kwargs)
        self.create_widget()

    def set_label(self, label: str):
        self.label = label
        if self.epoch_lbl:
            self.epoch_lbl.setText(label)

        if self.epoch_chk:
            self.epoch_chk.setText(label)

    @log_func_call
    def create_qtobj(self, *args, **kwargs):
        parent_qtobj: GuiWidgetParentType = self.gui_parent.qtobj
        qtobj = QFrame(parent_qtobj)
        return qtobj

    def create_convert_chk(self):
        clocklist = self.clocklist
        cb = qt_callback(partial(self.do_convert, False))
        clocklist.qtobj.currentIndexChanged.connect(cb)

        convert = QCheckBox("Convert")
        convert.setVisible(not self.timer)
        convert.setChecked(True)
        cb = qt_callback(partial(self.do_convert, True))
        convert.stateChanged.connect(cb)
        self.convert = convert
        return convert

    def create_widget(self):
        qtobj = self.qtobj
        layout = QVBoxLayout(qtobj)
        qtobj.setLayout(layout)
        self.layout = layout

        dhms, ymdhms, y_doy_hms = self.create_time_editors()
        dhms_opt, ymdhms_opt, y_doy_hms_opt = self.create_input_format_radios()
        fold_known, is_fold = self.create_fold_options()

        self.clocklist = None
        self.convert = None
        show_clocklist = self.show_clocklist
        if show_clocklist:
            clocklist = ClockListWidget(self, True)
            self.clocklist = clocklist
            convert = self.create_convert_chk()

        hbox_input_fmt = QHBoxLayout()
        hbox_input_fmt.addWidget(dhms_opt)
        hbox_input_fmt.addWidget(ymdhms_opt)
        hbox_input_fmt.addWidget(y_doy_hms_opt)

        hbox_fold = QHBoxLayout()
        # hbox_fold.addWidget(QLabel('Fold:'))
        hbox_fold.addWidget(fold_known)
        hbox_fold.addWidget(is_fold)

        hbox_epoch_meta = QHBoxLayout()
        if self.timer:
            hbox_epoch_meta.addWidget(self.create_epoch_lbl())
            self.epoch_chk = None

        else:
            hbox_epoch_meta.addWidget(self.create_epoch_chk())
            self.epoch_lbl = None

        hbox_epoch_meta.addLayout(hbox_input_fmt)
        hbox_epoch_meta.addStretch()
        hbox_epoch_meta.addLayout(hbox_fold)
        layout.addLayout(hbox_epoch_meta)

        hbox_epoch = QHBoxLayout()
        hbox_epoch.addWidget(dhms.qtobj)
        hbox_epoch.addWidget(ymdhms.qtobj)
        hbox_epoch.addWidget(y_doy_hms.qtobj)
        if show_clocklist:
            hbox_epoch.addWidget(clocklist.qtobj)
            hbox_epoch.addWidget(convert)

        self.hbox_epoch = hbox_epoch

        layout.addLayout(hbox_epoch)

        self.create_shortcuts()

        return qtobj

    def create_shortcuts(self):
        qtobj = self.qtobj
        timer = self.timer

        self.dhms_shortcut = None
        self.ymdhms_shortcut = None
        self.y_doy_hms_shortcut = None
        if not timer and self.keybd_shortcuts:
            dhms_shortcut = QShortcut(QKeySequence(Qt.CTRL+Qt.Key_D), qtobj)
            dhms_shortcut.activated.connect(qt_callback(self.set_format_dhms))
            dhms_shortcut.setContext(Qt.WindowShortcut)
            self.dhms_shortcut = dhms_shortcut

            ymdhms_shortcut = QShortcut(QKeySequence(Qt.CTRL+Qt.Key_Y), qtobj)
            ymdhms_shortcut.activated.connect(qt_callback(self.set_format_ymdhms))  # noqa: E501
            ymdhms_shortcut.setContext(Qt.WindowShortcut)
            self.ymdhms_shortcut = ymdhms_shortcut

            y_doy_hms_shortcut = QShortcut(QKeySequence(Qt.CTRL+Qt.Key_G), qtobj)  # noqa: E501
            y_doy_hms_shortcut.activated.connect(qt_callback(self.set_format_y_doy_hms))  # noqa: E501
            y_doy_hms_shortcut.setContext(Qt.WindowShortcut)
            self.y_doy_hms_shortcut = y_doy_hms_shortcut

    def create_fold_options(self):
        timer = self.timer

        fold_known = QCheckBox("Fold known")
        fold_known.setVisible(not timer)
        self.fold_known = fold_known

        is_fold = QCheckBox("Folded")
        is_fold.setVisible(not timer)
        self.is_fold = is_fold

        fold_known.stateChanged.connect(
            lambda state: is_fold.setEnabled(state == Qt.Checked)
        )

        # Ensure starts in correct state
        is_fold.setEnabled(fold_known.isChecked())

        return fold_known, is_fold

    def create_time_editors(self):
        dhms = DhmsWidget(self, edit_callback=self.update_epoch_sec)
        dhms.qtobj.setVisible(False)
        self.dhms = dhms

        ymdhms = YmdhmsWidget(self, edit_callback=self.update_epoch_sec)
        ymdhms.qtobj.setVisible(False)
        self.ymdhms = ymdhms

        y_doy_hms = YDoyHmsWidget(self, edit_callback=self.update_epoch_sec)
        y_doy_hms.qtobj.setVisible(False)
        self.y_doy_hms = y_doy_hms

        return dhms, ymdhms, y_doy_hms

    def create_input_format_radios(self):
        timer = self.timer
        keybd_shortcuts = self.keybd_shortcuts

        dhms_opt = QRadioButton("DHMS")
        dhms_tt = "Days, Hours, Minutes, Seconds"
        if keybd_shortcuts:
            dhms_tt += " (Ctrl + D)"

        dhms_opt.setToolTip(dhms_tt)
        dhms_opt.setVisible(not timer)
        dhms_opt.toggled.connect(qt_callback(self.set_format_dhms))
        self.dhms_radio = dhms_opt

        ymdhms_opt = QRadioButton("YMDHMS")
        ymdhms_tt = "Year, Month, Day, Hour, Minute, Second"
        if keybd_shortcuts:
            ymdhms_tt += " (Ctrl + Y)"

        ymdhms_opt.setToolTip(ymdhms_tt)  # noqa: E501
        ymdhms_opt.setVisible(not timer)
        ymdhms_opt.toggled.connect(qt_callback(self.set_format_ymdhms))
        self.ymdhms_radio = ymdhms_opt

        y_doy_hms_opt = QRadioButton("Y:DOY:HMS")
        y_doy_hms_tt = "Year, Day Of Year, Hour, Minute, Second"
        if keybd_shortcuts:
            y_doy_hms_tt += " (Ctrl + G)"

        y_doy_hms_opt.setToolTip(y_doy_hms_tt)  # noqa: E501
        y_doy_hms_opt.setVisible(not timer)
        y_doy_hms_opt.toggled.connect(qt_callback(self.set_format_y_doy_hms))
        self.y_doy_hms_radio = y_doy_hms_opt

        return dhms_opt, ymdhms_opt, y_doy_hms_opt

    def set_format_dhms(self, checked: bool | Qt.CheckState = True):
        if not isinstance(checked, bool):
            checked = checked == Qt.Checked

        self.dhms_radio.setChecked(checked)
        self.dhms.qtobj.setVisible(checked)
        if checked:
            self.input_fmt = TimeFormat.DHMS

    def set_format_ymdhms(self, checked: bool | Qt.CheckState = True):
        if not isinstance(checked, bool):
            checked = checked == Qt.Checked

        self.ymdhms_radio.setChecked(checked)
        self.ymdhms.qtobj.setVisible(checked)
        if checked:
            self.input_fmt = TimeFormat.YMDHMS

    def set_format_y_doy_hms(self, checked: bool | Qt.CheckState = True):
        if not isinstance(checked, bool):
            checked = checked == Qt.Checked

        self.y_doy_hms_radio.setChecked(checked)
        self.y_doy_hms.qtobj.setVisible(checked)
        if checked:
            self.input_fmt = TimeFormat.Y_DOY_HMS

    def create_epoch_chk(self):
        epoch_chk = QCheckBox(self.label)
        epoch_chk.setChecked(True)
        epoch_chk.stateChanged.connect(qt_callback(self.set_epoch_enabled))
        self.epoch_chk = epoch_chk
        return epoch_chk

    def create_epoch_lbl(self):
        epoch_lbl = QLabel(self.label)
        self.epoch_lbl = epoch_lbl
        return epoch_lbl

    def set_epoch_enabled(self, state: bool | Qt.CheckState):
        epoch_chk = self.epoch_chk
        if isinstance(state, bool) or not epoch_chk:
            checked = state
            if epoch_chk:
                epoch_chk.setChecked(checked)

        else:
            checked = state == Qt.Checked

        self.dhms.qtobj.setEnabled(checked)
        self.ymdhms.qtobj.setEnabled(checked)
        self.y_doy_hms.qtobj.setEnabled(checked)
        self.dhms_radio.setEnabled(checked)
        self.ymdhms_radio.setEnabled(checked)
        self.y_doy_hms_radio.setEnabled(checked)
        if self.show_clocklist:
            self.clocklist.qtobj.setEnabled(checked)
            self.convert.setEnabled(checked)

        self.fold_known.setEnabled(checked)
        self.is_fold.setEnabled(checked and self.fold_known.isChecked())

    def set_tab_order(self, parent: QWidget, prev: 'QWidget | EpochWidget',
                      nxt: 'QWidget | EpochWidget'):
        if not isinstance(prev, QWidget):
            prev = prev.is_fold

        if not isinstance(nxt, QWidget):
            next_chk = nxt.epoch_chk
            nxt = next_chk if next_chk else nxt.dhms_radio

        epoch_chk = self.epoch_chk
        if epoch_chk:
            parent.setTabOrder(prev, epoch_chk)
            prev = epoch_chk

        parent.setTabOrder(prev, self.dhms_radio)
        parent.setTabOrder(self.dhms_radio, self.ymdhms_radio)
        parent.setTabOrder(self.ymdhms_radio, self.y_doy_hms_radio)
        parent.setTabOrder(self.y_doy_hms_radio, self.dhms.qtobj)
        parent.setTabOrder(self.dhms.qtobj, self.ymdhms.qtobj)
        parent.setTabOrder(self.ymdhms.qtobj, self.y_doy_hms.qtobj)

        show_clocklist = self.show_clocklist
        tmp = self.clocklist.qtobj if show_clocklist else self.fold_known
        parent.setTabOrder(self.y_doy_hms.qtobj, tmp)
        if show_clocklist:
            parent.setTabOrder(self.clocklist.qtobj, self.convert)
            parent.setTabOrder(self.convert, self.fold_known)

        parent.setTabOrder(self.fold_known, self.is_fold)
        parent.setTabOrder(self.is_fold, nxt)

    def set_values(self, data: Epoch = None):
        self.set_epoch_enabled(data is not None)
        if data is None:
            epoch_sec = 0

        else:
            epoch_sec = data.epoch_sec

        self.epoch_sec = epoch_sec
        self.update_epoch_sec(None, epoch_sec)
        clocklist = self.clocklist
        if data is None:
            self.dhms_radio.setChecked(True)
            self.dhms.qtobj.setVisible(True)
            if clocklist:
                clocklist.qtobj.setCurrentIndex(0)

            return

        fold_known_chk = self.fold_known
        fold_known_chk.setChecked(data.fold_known)

        is_fold_chk = self.is_fold
        is_fold_chk.setChecked(data.fold)
        is_fold_chk.setEnabled(fold_known_chk.isChecked())

        input_fmt = data.input_fmt
        if input_fmt in FLOAT_FMTS:
            input_fmt = TimeFormat.DHMS

        is_dhms = input_fmt == TimeFormat.DHMS
        self.dhms_radio.setChecked(is_dhms)
        self.dhms.qtobj.setVisible(is_dhms)

        is_ymdhms = input_fmt == TimeFormat.YMDHMS
        self.ymdhms_radio.setChecked(is_ymdhms)
        self.ymdhms.qtobj.setVisible(is_ymdhms)

        is_y_doy_hms = input_fmt == TimeFormat.Y_DOY_HMS
        self.y_doy_hms_radio.setChecked(is_y_doy_hms)
        self.y_doy_hms.qtobj.setVisible(is_y_doy_hms)

        if clocklist:
            if self.timer:
                clocklist.set_clock_id(NOW_ID)
                clocklist.qtobj.setEnabled(False)

            else:
                clocklist.set_clock(data.clock)

    def update_epoch_sec(self, widget: BaseTimeEditorWidget, sec: float):
        # widget_name = widget.get_title() if widget else ""
        # msg = f"Updating {self.label} {sec}"
        # if widget_name:
        #     msg += f" from widget {widget_name}"

        # log_info(msg)

        if sec is not None:
            self.epoch_sec = sec
            editors = (self.dhms, self.ymdhms, self.y_doy_hms)
            for editor in editors:
                if editor is not widget:
                    editor.set_from_sec(sec)

    def get_epoch(self):
        epoch_chk = self.epoch_chk
        epoch_enabled = True if not epoch_chk else epoch_chk.isChecked()
        if not epoch_enabled:
            return

        clklst = self.clocklist
        epoch_sec = self.epoch_sec
        if clklst:
            clkid = clklst.get_clock_id()
            if clkid == NOW_ID:
                clkid = 'TAI'
                epoch_sec += now_tai_sec()

            epoch_clock = DisplayClock.get_clock_for_id(clkid)

        else:
            epoch_clock = None

        return Epoch(epoch_clock, epoch_sec,
                     self.fold_known.isChecked(), self.is_fold.isChecked(),
                     self.input_fmt)

    def do_convert(self, chkbox: bool, state: int | Qt.CheckState = None):
        "this is the handler for changing the selected clock"
        checked = self.convert.isChecked()
        clocklist = self.clocklist
        new_id = clocklist.get_clock_id()
        old_id = self.last_clock_id
        if checked and old_id is not None and old_id != new_id:
            if NOW_ID in (new_id, old_id):
                log_info('Note: Conversions with (now) reset epoch to zero')
                checked = False  # pretend it's not checked
                self.update_epoch_sec(None, 0)

            else:
                old_clk = DisplayClock.get_clock_for_id(old_id)
                new_clk = DisplayClock.get_clock_for_id(new_id)
                epoch = self.get_epoch()
                epoch.clock = old_clk
                epoch_tai = epoch.to_tai().epoch_sec
                try:
                    new_epoch = new_clk.tai_to_clock_time(epoch_tai)
                except NotImplementedError:
                    log_warning('Converting between clocks of different tick '
                                'rates that are not absolute clocks is '
                                'currently unsupported; '
                                'conversion not performed.')
                else:
                    self.update_epoch_sec(None, new_epoch.epoch_sec)

        # always do this, even if we don't convert
        self.last_clock_id = new_id
