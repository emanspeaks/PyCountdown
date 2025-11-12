from pyrandyos.gui.qt import QPixmap, Qt
from pyrandyos.gui.splash import GuiSplashScreen

from ..app import PyCountdownApp


class SplashScreen(GuiSplashScreen):
    def __init__(self):
        splash_path = PyCountdownApp.get_assets_dir()/'SMPTE_Color_Bars.png'
        pm = QPixmap(splash_path.as_posix())
        super().__init__(pm.scaled(pm.width() * 2,
                                   pm.height() * 2,
                                   Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation))
        self.set_progress(message="Loading PyCountdown...")
