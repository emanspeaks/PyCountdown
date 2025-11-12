from pyrandyos.gui.icons.iconfont import IconSpec
from pyrandyos.gui.icons.thirdparty.codicons import Codicons
from pyrandyos.gui.icons.thirdparty.codicons import names as codicon_names
from pyrandyos.gui.icons.thirdparty.fluentui import FluentUI
from pyrandyos.gui.icons.thirdparty.fluentui import names as fluentui_names  # noqa: E501

ProgramIcon = IconSpec.generate_iconspec(FluentUI, glyph=fluentui_names.ic_fluent_text_bullet_list_square_clock_20_regular)  # noqa: E501
ConfigIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.json)
# CopyCodeIcon = IconSpec.generate_iconspec(FluentUI_Resize, glyph=fluentui_r_names.ic_fluent_clipboard_code_20_regular)  # noqa: E501
# CopyNameIcon = IconSpec.generate_iconspec(FluentUI_Resize, glyph=fluentui_r_names.ic_fluent_clipboard_letter_20_regular)  # noqa: E501
