from pyrandyos.gui.icons.iconfont import IconSpec, IconStateSpec, IconLayer
from pyrandyos.gui.icons.thirdparty.codicons import Codicons
from pyrandyos.gui.icons.thirdparty.codicons import names as codicons_names
from pyrandyos.gui.icons.thirdparty.fluentui import FluentUI
from pyrandyos.gui.icons.thirdparty.fluentui import names as fluentui_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fa5.solid import Fa5_Solid
from pyrandyos.gui.icons.thirdparty.fa5.solid import names as fa5_s_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fa5 import Fa5
from pyrandyos.gui.icons.thirdparty.fa5 import names as fa5_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.phosphor import Phosphor
from pyrandyos.gui.icons.thirdparty.phosphor import names as phosphor_names  # noqa: E501
from pyrandyos.gui.icons.thirdparty.fluentui.resize import FluentUI_Resize
from pyrandyos.gui.icons.thirdparty.fluentui.resize import names as fluentui_r_names  # noqa: E501

JsonFontGlyph = (Codicons, codicons_names.json)
ClockFontGlyph = (Fa5, fa5_names.clock)
SolidSqFontGlyph = (Fa5_Solid, fa5_s_names.square_full)
BulletClockFontGlyph = (FluentUI, fluentui_names.ic_fluent_text_bullet_list_square_clock_20_regular)  # noqa: E501
GhostFontGlyph = (Phosphor, phosphor_names.ghost_fill)
NoGhostFontGlyph = (Phosphor, phosphor_names.ghost_light)
UnmuteGlyph = (FluentUI, fluentui_names.ic_fluent_speaker_2_20_regular)
MuteGlyph = (FluentUI, fluentui_names.ic_fluent_speaker_off_20_regular)

JsonIconLayer = IconLayer(*JsonFontGlyph, 'white', scale=1.25)
ClockIconLayer = IconLayer(*ClockFontGlyph, 'white', scale=0.5, y=0.05)
SolidSquareIconLayer = IconLayer(*SolidSqFontGlyph, 'black')
BulletClockIconLayer = IconLayer(*BulletClockFontGlyph, 'white')
GhostIconLayer = IconLayer(*GhostFontGlyph, 'white')
NoGhostIconLayer = IconLayer(*NoGhostFontGlyph, 'white')
UnmuteIconLayer = IconLayer(*UnmuteGlyph, 'white')
MuteIconLayer = IconLayer(*MuteGlyph, 'white')

TimerIcon = IconSpec.generate_iconspec(FluentUI, glyph=fluentui_names.ic_fluent_clock_alarm_20_regular)  # noqa: E501
SaveAsIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.save_as)  # noqa: E501
NewIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.new_file)  # noqa: E501
OpenIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.folder_opened)  # noqa: E501
ClocksJsonIcon = IconSpec(IconStateSpec([JsonIconLayer, ClockIconLayer]))  # noqa: E501
ProgramIcon = IconSpec(IconStateSpec([SolidSquareIconLayer, BulletClockIconLayer]))  # noqa: E501
ShowHiddenIcon = IconSpec(IconStateSpec(NoGhostIconLayer), IconStateSpec(GhostIconLayer))  # noqa: E501
MuteIcon = IconSpec(IconStateSpec(UnmuteIconLayer), IconStateSpec(MuteIconLayer))  # noqa: E501
ConfigIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.json)
AddClockIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.add)
RemoveClockIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.remove)  # noqa: E501
RefreshIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.refresh)  # noqa: E501
# LabelIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.symbol_text)  # noqa: E501
UpArrowIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.arrow_up)  # noqa: E501
DownArrowIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.arrow_down)  # noqa: E501
CopyIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.copy)  # noqa: E501
ThresholdSetIcon = IconSpec.generate_iconspec(FluentUI_Resize, glyph=fluentui_r_names.ic_fluent_task_list_square_settings_20_regular)  # noqa: E501
ApplyThreshSetIcon = IconSpec.generate_iconspec(Codicons, glyph=codicons_names.checklist)  # noqa: E501
