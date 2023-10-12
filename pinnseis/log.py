#!/usr/bin/env python3

import logging

__NAME__ = "pinnseis"

plain = False

################################################################################
#### Global variables ##########################################################
################################################################################

# log = None

################################################################################
#### Colours ###################################################################
################################################################################

colours_pretty = {
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "blue": "\033[0;34m",
    "cyan": "\033[0;36m",
    "magenta": "\033[0;35m",
    "white": "\033[0;37m",
    "brightred": "\033[1;31m",
    "brightgreen": "\033[1;32m",
    "brightblue": "\033[1;34m",
    "brightmagenta": "\033[1;35m",
    "brightyellow": "\033[1;33m",
    "brightcyan": "\033[1;36m",
    "yellow": "\033[0;33m",
    "bred": "\033[7;31m",
    "bcyan": "\033[7;36m",
    "bblue": "\033[7;34m",
    "bmagenta": "\033[7;35m",
    "byellow": "\033[7;33;40m",
    "bgreen": "\033[7;32m",
    "bwhite": "\033[7;37m",
    "grey": "\033[1;30m",
    "fred": "\033[5;31m",
    "end": "\033[0m",
}

colours_plain = {}
for colour in colours_pretty.keys():
    colours_plain[colour] = ""


def addcolour(dic, colourful=True):
    result = {}
    if colourful:
        result.update(colours_pretty)
    else:
        result.update(colours_plain)
    result.update(dic)
    return result


################################################################################
#### Reporting #################################################################
################################################################################


def show_traceback():
    from traceback import format_exc
    from sys import exc_info

    print("Sys exc info: {}".format(exc_info()[0]))
    backtrace = format_exc()
    if backtrace is not None:
        print("Backtrace:")
        print(backtrace)


def error(*strings, var={}, fatal=False):
    report(" ".join(strings), var=var, error=True)
    if fatal:
        show_traceback()
        from sys import exit

        exit(1)


def warning(*strings, var={}):
    report(" ".join(strings), var=var, warning=True)


def debug(*strings, var={}, indent=0):
    report(" ".join(strings), var=var, indent=indent, debug=True)


def report(
    *strings,
    var={},
    starred=False,
    indent=0,
    debug=False,
    title=False,
    warning=False,
    error=False
):
    log = getLogger()
    prefix = ""
    if error:
        prefix += "%(brightred)sError:%(red)s "
    elif warning:
        prefix += "%(brightmagenta)sWarning:%(end)s "
    # if not starred:
    #    prefix = prefix + (indent * '  ')
    if (not warning) and (not error):
        prefix += indent * "  "
    if starred:
        prefix += "%(brightyellow)s*%(end)s "

    string = prefix + " ".join(strings)
    if error:
        string = "%%(red)s%s%%(end)s" % string
    elif warning:
        string = "%%(magenta)s%s%%(end)s" % string
    elif title:
        string = "%%(brightyellow)s%s%%(end)s" % string
    try:
        string = string % addcolour(var, colourful=(not plain))
    except:
        pass
    if error:
        log.error(string)
    elif error:
        log.warn(string)
    elif debug:
        log.debug(string)
    else:
        log.info(string)


################################################################################
#### Logging setup #############################################################
################################################################################


def loggingInit(options):
    """Initiate a logging method, both to stdout and to file"""

    global plain
    plain = options.plain

    # Setup the log handlers to stdout and file.
    log = logging.getLogger(__NAME__)

    if options.debug or options.logfiledebug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    prefix = ""
    if options.timestamp:
        prefix = "%(asctime)s "
    formatter_info = logging.Formatter(
        prefix + "%(message)s", datefmt="%Y%m%d %H:%M.%S"
    )
    formatter_debug = logging.Formatter(
        prefix + "%(levelname)-5s | %(message)s", datefmt="%Y%m%d %H:%M.%S"
    )

    if options.stdout:
        from sys import stdout as _stdout

        handler_stdout = logging.StreamHandler(_stdout)
        if options.debug:
            handler_stdout.setLevel(logging.DEBUG)
            handler_stdout.setFormatter(formatter_debug)
        else:
            handler_stdout.setLevel(logging.INFO)
            handler_stdout.setFormatter(formatter_info)
        log.addHandler(handler_stdout)

    if options.logfile:
        handler_file = logging.FileHandler(
            options.logfile,
            mode="a",
            encoding="UTF-8",
        )
        if options.debug:
            handler_file.setLevel(logging.DEBUG)
            handler_file.setFormatter(formatter_debug)
        else:
            handler_file.setLevel(logging.INFO)
            handler_file.setFormatter(formatter_info)
        log.addHandler(handler_file)

    if options.logfiledebug:
        handler_file_debug = logging.FileHandler(
            options.logfiledebug,
            mode="a",
            encoding="UTF-8",
        )
        handler_file_debug.setLevel(logging.DEBUG)
        handler_file_debug.setFormatter(formatter_debug)
        log.addHandler(handler_file_debug)

    # log.info('* ' + '-' * 4 + ' Start up ' + '-' * 40)
    # log.info('\n\n* ' + '-' * 15 + ' Start up ' + '-' * 40)
    log.debug("Log enabled with debugging messages")
    if options.logfile:
        log.info("Logging to file enabled, to: {}".format(options.logfile))
    if options.logfiledebug:
        log.info(
            "Logging debug messages to file enabled, to: {}".format(
                options.logfiledebug
            )
        )

    return log


def getLogger():
    """Obtain a hangle on the logging method"""
    return logging.getLogger(__NAME__)


def isDebug():
    """Check if debugging is enabled"""
    log = getLogger()
    return log.level == logging.DEBUG
