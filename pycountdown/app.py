from pathlib import Path

from pyrandyos import PyRandyOSApp
from pyrandyos.utils.json import load_jsonc

from .logging import log_func_call

HERE = Path(__file__).parent


CLOCKS_MTIME_KEY = '__clocks_mtime'
CLOCKS_FILE_CHECK_SEC_KEY = 'clocks_file_check_sec'


class PyCountdownApp(PyRandyOSApp):
    APP_NAME: str = 'PyCountdown'
    APP_LOG_PREFIX = 'PyCountdown'
    APP_ASSETS_DIR = HERE/"assets"
    APP_PATH_KEYS: tuple[str] = ('clocks_file',)
    APP_GLOBAL_DEFAULTS = {
        'clocks_file': './clocks.jsonc',
        CLOCKS_MTIME_KEY: None,
        CLOCKS_FILE_CHECK_SEC_KEY: 5,
    }

    @classmethod
    @log_func_call
    def main(cls, input_data: dict | str | Path = None, *args,
             **kwargs):
        cls.init_main(input_data, True, **kwargs)

        from .gui import PyCountdownGui
        gui = PyCountdownGui(args)
        cls.gui = gui
        return gui.main(*args, **kwargs)

    @classmethod
    @log_func_call
    def preprocess_args(cls, args: list[str]):
        return args

    @classmethod
    def check_clocks_file(cls, force: bool = False):
        clocks_file: Path = cls['clocks_file']
        old_mtime: float = cls[CLOCKS_MTIME_KEY]
        if clocks_file and clocks_file.exists():
            mtime = clocks_file.stat().st_mtime
            if force or mtime != old_mtime:
                from .lib.displayclocks import DisplayClock
                cls.set(CLOCKS_MTIME_KEY, mtime)
                DisplayClock.from_jsonc(load_jsonc(clocks_file))
                return True
