from pathlib import Path

from pyrandyos import PyRandyOSApp

from .logging import log_func_call

HERE = Path(__file__).parent


class PyCountdownApp(PyRandyOSApp):
    APP_NAME: str = 'PyCountdown'
    APP_LOG_PREFIX = 'PyCountdown'
    APP_ASSETS_DIR = HERE/"assets"

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
