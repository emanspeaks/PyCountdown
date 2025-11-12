from pyrandyos.gui.icons.iconfont.icon import IconSpec


def iconstring_to_specname_iconname(iconstring: str) -> tuple[str, str]:
    """
    Convert an icon string in the format 'specname:iconname' to a tuple of
    (specname, iconname).
    """
    if ':' not in iconstring:
        raise ValueError(f"Invalid icon string format: {iconstring}")
    return tuple(iconstring.split(':', 1))


def iconstring_to_iconspec(iconstring: str) -> IconSpec:
    """
    Convert an icon string in the format 'specname:iconname' to an IconSpec
    object.
    """
    specname, iconname = iconstring_to_specname_iconname(iconstring)
    return IconSpec.generate_iconspec(specname, glyph_name=iconname)
