#!/usr/bin/env python3

from .log import debug, report, error

_found_fonts = {}


class FontNotFound(Exception):
    """Cleanly report that a font cannot be found on the system"""

    pass


class ResourceNotFound(Exception):
    """Cleanly handle the case when a resource cannot be found"""

    pass

class FileNotFound(Exception):
    """Cleanly handle when a file cannot be found"""

    pass


def bytes2human(num, suffix="B"):
    """Convert raw number of bytes to a human-readable form"""
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def execute(cmd, wait=True):
    from subprocess import Popen, PIPE, DEVNULL
    from os.path import exists, expanduser

    debug("Running system command: " + (" ".join(cmd)).replace(expanduser("~"), "~", 1))
    if wait:
        s = Popen(cmd, stderr=DEVNULL, stdout=PIPE)
        s.wait()
        return [s.returncode, s.communicate()[0]]
    else:
        s = Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        return [0, b""]

def unique_folder(folder):
    from os.path import dirname, join, realpath, expanduser, exists, splitext
    from re import search
    if not exists(folder):
        return folder
    if folder.endswith("/"):
        folder = folder[:-1]
    if not search("_[0-9]*[0-9]$", folder):
        base = folder
        number = 0
    else:
        parts = folder.split("_")
        number = parts[-1]
        base = '_'.join(parts[:-1])
    while exists(folder):
        number += 1
        if number > 100:
            error("Creation of new unique folder for {} has gone past the max number limit {}".format(base, number), fatal=True)
        folder = "{}_{}".format(base, number)
        #print("Repeat:", folder)
    return folder

def concise_folder(folder):
    from os.path import expanduser, realpath
    from re import sub
    home = realpath(expanduser('~'))
    current = realpath(".")
    folder = sub("^"+current, ".", folder)
    folder = sub("^"+home, "~", folder)
    return folder

def camel_case(s):
    from re import sub
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])

def fontname_filter(name):
    """Filter for consistently simplifying font names"""
    from os.path import splitext

    _name = splitext(name)[0]
    return _name.replace("-", "").lower()


def find_font_path(name):
    """Search for a font with the name 'name' on the system and return its path"""
    from os import listdir
    from os.path import realpath, expanduser, join, exists

    global _found_fonts
    if name in _found_fonts:
        return _found_fonts[name]
    key_request = fontname_filter(name)
    if key_request not in _found_fonts:
        _search_paths = [
            "/System/Library/Fonts/",
            "/Library/Fonts/",
            "~/Library/Fonts/",
        ]
        _all = {}
        for folder in _search_paths:
            _folder = realpath(expanduser(folder))
            if not exists(_folder):
                continue
            for filename in listdir(_folder):
                fullpath = join(_folder, filename)
                key = fontname_filter(filename)
                _all[key] = fullpath
        # if isDebug():
        #     for key, value in sorted(_all.items()):
        #         debug('{}: {}'.format(key, value))
        if key_request in _all:
            _found_fonts[key_request] = _all[key_request]

    if key_request in _found_fonts:
        return _found_fonts[key_request]
    else:
        raise FontNotFound("{}, with short key {}".format(name, key_request))


def locate_resource(filename):
    """Search for a resource file and return its fullpath"""
    from os.path import dirname, join, realpath, expanduser, exists, splitext

    # _default_extension = "png"
    # if extension is None:
    #     _extension = _default_extension
    # else:
    #     _extension = extension
    # base, ext = splitext(filename)

    # if len(ext) == 0:
    #     _filename = "{}.{}".format(filename, _extension)
    # else:
    #     _filename = filename
    _filename = filename
    resourcefolder = realpath(join(dirname(dirname(realpath(__file__))), "data"))
    # debug('Resource folder: {}'.format(resourcefolder))

    if _filename.startswith("/"):
        fullpath = realpath(_filename)
    elif exists(join(resourcefolder, _filename)):
        fullpath = join(resourcefolder, _filename)
    else:
        fullpath = realpath(expanduser(_filename))
    if not exists(fullpath):
        raise ResourceNotFound(fullpath)
    return fullpath


# def load_resource(filename, extension=None):
#     """ Load the raw contents of a resource on the system """
#     fullpath = locate_resource(filename, extension=extension)
#     from os.path import splitext
#     from PIL import Image
#     if splitext(fullpath)[1][1:].lower() == 'svg':
#         return read_svg(fullpath)
#     else:
#         return Image.open(fullpath)
