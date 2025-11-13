from pyrandyos.gui.icons.iconfont import IconSpec, IconStateSpec, IconLayer
from pyrandyos.gui.icons.thirdparty.codicons import Codicons
from pyrandyos.gui.icons.thirdparty.codicons import names as codicon_names
from pyrandyos.gui.icons.thirdparty.fluentui import FluentUI
from pyrandyos.gui.icons.thirdparty.fluentui import names as fluentui_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fa5.solid import Fa5_Solid
from pyrandyos.gui.icons.thirdparty.fa5.solid import names as fa5_s_names  # noqa: E501

SolidSqFontGlyph = (Fa5_Solid, fa5_s_names.square_full)
BulletClockFontGlyph = (FluentUI, fluentui_names.ic_fluent_text_bullet_list_square_clock_20_regular)  # noqa: E501
SolidSquareIconLayer = IconLayer(*SolidSqFontGlyph, 'black')
BulletClockIconLayer = IconLayer(*BulletClockFontGlyph, 'white')

ProgramIcon = IconSpec(IconStateSpec([SolidSquareIconLayer, BulletClockIconLayer]))  # noqa: E501
ConfigIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.json)
# CopyCodeIcon = IconSpec.generate_iconspec(FluentUI_Resize, glyph=fluentui_r_names.ic_fluent_clipboard_code_20_regular)  # noqa: E501
# CopyNameIcon = IconSpec.generate_iconspec(FluentUI_Resize, glyph=fluentui_r_names.ic_fluent_clipboard_letter_20_regular)  # noqa: E501
