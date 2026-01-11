from pathlib import Path

from pyrandyos import PyRandyOSApp
from pyrandyos.utils.json import load_jsonc, save_json
from pyrandyos.config.keys import LOCAL_CONFIG_FILE_KEY

from .logging import log_func_call
from .lib.clocks.json import parse_clocks_jsonc, export_clocks_jsonc

HERE = Path(__file__).parent


CLOCKS_MTIME_KEY = '__clocks_mtime'
CLOCKS_SCHEMA_KEY = '__clocks_schema'
SCHEMA_KEY = 'json_schema'
CLOCKS_FILE_CHECK_SEC_KEY = 'clocks_file_check_sec'
SHOW_HIDDEN_KEY = 'show_hidden'
LOCAL_SHOW_HIDDEN_KEY = f'local.{SHOW_HIDDEN_KEY}'


class PyCountdownApp(PyRandyOSApp):
    APP_NAME: str = 'PyCountdown'
    APP_LOG_PREFIX = 'PyCountdown'
    APP_ASSETS_DIR = HERE/"assets"
    APP_PATH_KEYS: tuple[str] = ('clocks_file', 'local.clocks_file')
    APP_GLOBAL_DEFAULTS = {
        'clocks_file': 'clocks.jsonc',
        CLOCKS_MTIME_KEY: None,
        CLOCKS_FILE_CHECK_SEC_KEY: 5,
        CLOCKS_SCHEMA_KEY: None,
        LOCAL_CONFIG_FILE_KEY: "~/pycountdown/.pycountdown_local_config.jsonc",
    }
    APP_LOCAL_DEFAULTS = {
        SCHEMA_KEY: "https://raw.githubusercontent.com/emanspeaks/PyCountdown/refs/heads/master/pycountdown/assets/clocks.schema.jsonc",  # noqa: E501
        SHOW_HIDDEN_KEY: False,
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
    def get_clocks_file_path(cls):
        local: dict = cls.get_local_config()
        clocks_file: Path = local.get('clocks_file')
        if not clocks_file:
            clocks_file: Path = cls.get('clocks_file')

        # if not clocks_file:
        #     raise ValueError("No clocks file configured")

        return clocks_file

    @classmethod
    def set_clocks_file_path(cls, path: Path | str = None,
                             clear: bool = False):
        clocks_file = None if clear or not path else Path(path)
        if clear or clocks_file.exists():
            local: dict = cls.get_local_config()
            local['clocks_file'] = clocks_file
            if clear:
                cls.set('clocks_file', None)

            # return cls.check_clocks_file(True)

    @classmethod
    def check_clocks_file(cls, force: bool = False):
        clocks_file = cls.get_clocks_file_path()
        old_mtime: float = cls[CLOCKS_MTIME_KEY]
        mtime = None
        if clocks_file and clocks_file.exists():
            mtime = clocks_file.stat().st_mtime

        if force or mtime != old_mtime:
            from .lib.clocks.displayclocks import DisplayClock
            from .lib.clocks.fmt import ThresholdSet
            cls.set(CLOCKS_MTIME_KEY, mtime)
            if clocks_file:
                clocks_jsonc = load_jsonc(clocks_file)
                clk_pool, thresh_pool = parse_clocks_jsonc(clocks_jsonc)

            else:
                clk_pool = []
                thresh_pool = []

            DisplayClock.pool = clk_pool
            ThresholdSet.pool = thresh_pool
            return True

    @classmethod
    def export_clocks_file(cls, clocks_file: Path | str = None):
        clocks_file = clocks_file or cls.get_clocks_file_path()
        from .lib.clocks.displayclocks import DisplayClock
        from .lib.clocks.fmt import ThresholdSet
        data = export_clocks_jsonc(DisplayClock.pool, ThresholdSet.pool)
        save_json(clocks_file, data)
