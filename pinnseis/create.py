#!/usr/bin/env python3

from .log import report, debug, warning, error


class FileNotFound(Exception):
    """Cleanly handle when a file cannot be found"""

    pass


class Create:
    """The core class of the library"""

    _default_name = "Default"

    def __init__(self, name=None):
        """Initiate a new instance of this class object"""
        self._name = None
        self._index = None
        self._total = None
        self.setName(name)

    def __str__(self):
        """Presents the object represented by a string"""
        if self._index is None:
            return "{}".format(self._name)
        elif self._total is None:
            return "{}: {}".format(self._index, self._name)
        elif self._total == 1:
            return "{}".format(self._name)
        else:
            return "{1:{0}}/{2:{0}}: {3}".format(
                len(str(self._total)), self._index, self._total, self._name
            )

    def addNumbering(self, index=None, total=None):
        """Mark this object with an index relative to others"""
        self._index = index
        self._total = total

    def setName(self, name=None, refresh=False):
        """Set the name of this class object"""
        if refresh or self._name is None:
            if name:
                self._name = name
            else:
                self._name = _default_name
        return self._name

    def show(self):
        """Show the current state of this class object"""
        report("{}".format(self))

    def process(self, show=False):
        """Process this object"""
        report("%(blue)sProcessing%(grey)s: %(yellow)s{}%(end)s".format(self))

        return True
