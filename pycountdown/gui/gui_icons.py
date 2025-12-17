from pyrandyos.gui.icons.iconfont import IconSpec, IconStateSpec, IconLayer
from pyrandyos.gui.icons.thirdparty.codicons import Codicons
from pyrandyos.gui.icons.thirdparty.codicons import names as codicon_names
from pyrandyos.gui.icons.thirdparty.fluentui import FluentUI
from pyrandyos.gui.icons.thirdparty.fluentui import names as fluentui_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fa5.solid import Fa5_Solid
from pyrandyos.gui.icons.thirdparty.fa5.solid import names as fa5_s_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fa5 import Fa5
from pyrandyos.gui.icons.thirdparty.fa5 import names as fa5_names  # noqa: E501

JsonFontGlyph = (Codicons, codicon_names.json)
ClockFontGlyph = (Fa5, fa5_names.clock)
SolidSqFontGlyph = (Fa5_Solid, fa5_s_names.square_full)
BulletClockFontGlyph = (FluentUI, fluentui_names.ic_fluent_text_bullet_list_square_clock_20_regular)  # noqa: E501
JsonIconLayer = IconLayer(*JsonFontGlyph, 'white', scale=1.25)
ClockIconLayer = IconLayer(*ClockFontGlyph, 'white', scale=0.5, y=0.05)
SolidSquareIconLayer = IconLayer(*SolidSqFontGlyph, 'black')
BulletClockIconLayer = IconLayer(*BulletClockFontGlyph, 'white')

ClocksJsonIcon = IconSpec(IconStateSpec([JsonIconLayer, ClockIconLayer]))  # noqa: E501
ProgramIcon = IconSpec(IconStateSpec([SolidSquareIconLayer, BulletClockIconLayer]))  # noqa: E501
ConfigIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.json)
AddClockIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.add)
RemoveClockIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.remove)  # noqa: E501
RefreshIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.refresh)
# CopyCodeIcon = IconSpec.generate_iconspec(FluentUI_Resize, glyph=fluentui_r_names.ic_fluent_clipboard_code_20_regular)  # noqa: E501
# CopyNameIcon = IconSpec.generate_iconspec(FluentUI_Resize, glyph=fluentui_r_names.ic_fluent_clipboard_letter_20_regular)  # noqa: E501
