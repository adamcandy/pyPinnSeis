#!/usr/bin/env python3

################################################################################
#### Options ###################################################################
################################################################################

options = None


class OptionsError(Exception):
    """Cleanly report when provided options are not valid"""

    pass


def checkOptions():
    """Return stored options, if available, otherwise return a new options class"""
    global options
    if options is None:
        options = Options()
    return options


def getOptions():
    """Return the initiated options store"""
    global options
    return options


class Options:
    """A class to process and store provided options"""

    def __init__(self):
        """Create an options class to process and store options"""
        self.data = []

        self.usage_show = False
        self.stdout = True
        self.debug = False
        self.logfile = None
        self.logfiledebug = None
        self.plain = True
        self._plain = False
        self.timestamp = False
        self.showplot = False

        self.read()
        self.validate()
        self.process()

    def getVersion(self):
        """Return the version number of the library"""
        from .version import __version__

        return __version__

    def showVersion(self):
        """Print the version number directly to stdout"""
        from sys import exit

        print("Version: {}".format(self.getVersion()))
        exit(0)

    def usage(self, unknown=None):
        """Show usage information for the library executable"""
        from os.path import basename
        from sys import argv, exit
        from re import sub
        from .log import addcolour

        if unknown:
            print(
                "%(red)sUnknown option%(grey)s: %(end)s%(unknown)s"
                % addcolour({"unknown": unknown})
            )
        content = """%(blue)sUsage for %(yellow)s%(cmdname)s%(end)s
 %(cmdname)s [options]
%(grey)s-- %(blue)sOptions%(grey)s ---\%(end)s 
              |___________________________________________________________________
 -showplot    | Show plots
              |___________________________________________________________________
 -v           | Verbose to stdout (--log file, to file; --plain for plain output)
 -q           | Quiet
 -h           | Display help
 --debug      | Debugging messages (--logd file, to file & enforce --debug)
 --version    | Show library version: %(green)s%(version)s%(end)s
              \___________________________________________________________________"""
        content = sub(r"( )(\|)( )", r"\1%(grey)s\2%(end)s\3", content)
        content = sub(r"( )(\|_+) *(\n)", r"\1%(grey)s\2%(end)s\3", content)
        content = sub(r"( )(\\_+) *$", r"\1%(grey)s\2%(end)s", content)
        content = content % addcolour(
            {"cmdname": basename(argv[0]), "version": self.getVersion()}
        )
        print(content)
        # self.useful()
        exit(0)

    def useful(self):
        from .log import addcolour

        content = """%(blue)sUseful%(grey)s:%(end)s
"""
        content = content % addcolour({})
        print(content)

    def read(self):
        """Read options provided and store"""
        from sys import argv
        from os.path import exists

        args = argv[1:]
        while len(args) > 0:
            argument = args.pop(0).rstrip()
            if argument == "-h":
                self.usage_show = True
            elif argument == "--version":
                self.showVersion()
            # Creation
            elif argument == "--showplot":
                self.showplot = True
            # Logging
            elif argument == "-v":
                self.stdout = True
            elif argument == "-q":
                self.stdout = False
            elif argument == "--plain":
                self._plain = True
            elif argument == "--debug":
                self.debug = True
            elif argument == "-l":
                self.logfile = logfile_default_setup()
            elif argument == "--log":
                self.logfile = args.pop(0).rstrip()
            elif argument == "--logd":
                self.logfiledebug = args.pop(0).rstrip()
            # Other / unknown
            elif argument.startswith("-"):
                self.usage(unknown=argument)
            else:
                self.data.append(argument)

    def process(self):
        """Process derivative options"""
        if len(self.data) > 0:
            self.name = self.data[0]
        # Set plain (non-coloured) output when there is any logging to file
        self.plain = self.logfile or self.logfiledebug or self._plain
        if self.usage_show:
            self.usage()

    def validate(self):
        """Check the provided options are valid"""
        # if len(self.data) == 0:
        #    raise OptionsError('No project name provided')
        return True

def logfile_default_setup():
    from os.path import realpath, dirname, join
    from os import makedirs
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #self.logfile = "pinnseis-{}.log".format(timestamp)
    logfile = realpath(join(dirname(dirname(realpath(__file__))), "output", "log",
        "pinnseis-{}.log".format(timestamp)))
    makedirs(dirname(logfile), exist_ok = True)
    return logfile


        
