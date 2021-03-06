"""Markdown filters
This file contains a collection of utility filters for dealing with 
markdown within Jinja templates.
"""
#-----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import print_function

# Stdlib imports
import os
import subprocess
from io import TextIOWrapper, BytesIO

# IPython imports
from IPython.nbconvert.utils.pandoc import pandoc
from IPython.nbconvert.utils.exceptions import ConversionException
from IPython.utils.process import find_cmd, FindCmdError
from IPython.utils.py3compat import cast_bytes

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------
marked = os.path.join(os.path.dirname(__file__), "marked.js")

__all__ = [
    'markdown2html',
    'markdown2html_pandoc',
    'markdown2html_marked',
    'markdown2latex',
    'markdown2rst',
]

class NodeJSMissing(ConversionException):
    """Exception raised when node.js is missing."""
    pass

def markdown2latex(source):
    """Convert a markdown string to LaTeX via pandoc.

    This function will raise an error if pandoc is not installed.
    Any error messages generated by pandoc are printed to stderr.

    Parameters
    ----------
    source : string
      Input string, assumed to be valid markdown.

    Returns
    -------
    out : string
      Output as returned by pandoc.
    """
    return pandoc(source, 'markdown', 'latex')

def markdown2html_pandoc(source):
    """Convert a markdown string to HTML via pandoc"""
    return pandoc(source, 'markdown', 'html', extra_args=['--mathjax'])

def markdown2html_marked(source, encoding='utf-8'):
    """Convert a markdown string to HTML via marked"""
    command = ['node', marked]
    try:
        p = subprocess.Popen(command,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
    except OSError as e:
        raise NodeJSMissing(
            "The command '%s' returned an error: %s.\n" % (" ".join(command), e) +
            "Please check that Node.js is installed."
        )
    out, _ = p.communicate(cast_bytes(source, encoding))
    out = TextIOWrapper(BytesIO(out), encoding, 'replace').read()
    return out.rstrip('\n')

def markdown2rst(source):
    """Convert a markdown string to LaTeX via pandoc.

    This function will raise an error if pandoc is not installed.
    Any error messages generated by pandoc are printed to stderr.

    Parameters
    ----------
    source : string
      Input string, assumed to be valid markdown.

    Returns
    -------
    out : string
      Output as returned by pandoc.
    """
    return pandoc(source, 'markdown', 'rst')

try:
    find_cmd('node')
except FindCmdError:
    markdown2html = markdown2html_pandoc
else:
    markdown2html = markdown2html_marked
