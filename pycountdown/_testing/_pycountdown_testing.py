from os import environ

from pyrandyos._testing import _is_running_in_ci, _is_pyrandyos_unittest  # noqa: F401, E501

# these constants are only relevant to testing, do not add to constants
ENV_PYCOUNTDOWN_UNITTEST_ACTIVE = 'ICONBROWSER_UNITTEST_ACTIVE'


def _is_pycountdown_unittest():
    return bool(environ.get(ENV_PYCOUNTDOWN_UNITTEST_ACTIVE))
