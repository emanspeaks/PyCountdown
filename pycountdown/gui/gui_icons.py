from pyrandyos.gui.icons.iconfont import IconSpec, IconStateSpec, IconLayer
from pyrandyos.gui.icons.thirdparty.codicons import Codicons
from pyrandyos.gui.icons.thirdparty.codicons import names as codicons_names
from pyrandyos.gui.icons.thirdparty.fluentui import FluentUI
from pyrandyos.gui.icons.thirdparty.fluentui import names as fluentui_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fa5.solid import Fa5_Solid
from pyrandyos.gui.icons.thirdparty.fa5.solid import names as fa5_s_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fa5 import Fa5
from pyrandyos.gui.icons.thirdparty.fa5 import names as fa5_names  # noqa: E501

JsonFontGlyph = (Codicons, codicons_names.json)
ClockFontGlyph = (Fa5, fa5_names.clock)
SolidSqFontGlyph = (Fa5_Solid, fa5_s_names.square_full)
BulletClockFontGlyph = (FluentUI, fluentui_names.ic_fluent_text_bullet_list_square_clock_20_regular)  # noqa: E501
JsonIconLayer = IconLayer(*JsonFontGlyph, 'white', scale=1.25)
ClockIconLayer = IconLayer(*ClockFontGlyph, 'white', scale=0.5, y=0.05)
SolidSquareIconLayer = IconLayer(*SolidSqFontGlyph, 'black')
BulletClockIconLayer = IconLayer(*BulletClockFontGlyph, 'white')

TimerIcon = IconSpec.generate_iconspec(FluentUI, glyph=fluentui_names.ic_fluent_clock_alarm_20_regular)  # noqa: E501
SaveAsIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.save_as)  # noqa: E501
ClocksJsonIcon = IconSpec(IconStateSpec([JsonIconLayer, ClockIconLayer]))  # noqa: E501
ProgramIcon = IconSpec(IconStateSpec([SolidSquareIconLayer, BulletClockIconLayer]))  # noqa: E501
ConfigIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.json)
AddClockIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.add)
RemoveClockIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.remove)  # noqa: E501
RefreshIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.refresh)  # noqa: E501
