#!/usr/bin/python
# -*- coding: utf-8 -*-
# Setup VIM: ex: noet ts=2 sw=2 :
#
# Module for doing DokuWiki output conversion.
# See README for details.
#
# Author: Elan Ruusamäe <glen@pld-linux.org>
# Version: 1.0

from MoinMoin import wikimacro, wikiutil
from MoinMoin.Page import Page
from MoinMoin.parser.wiki import Parser

from text_dokuwiki import Formatter
from MoinMoin.request import RequestCLI

import sys
import StringIO

def moin2doku(pagename, text):
	parser = Parser(text, request)

	# this needed for macros
	request.formatter = formatter

	p = Page(request, pagename)
	formatter.setPage(p)

	output = StringIO.StringIO()

	# wrap sys.stdout as RequestCLI has no interface to say where to output
	stdout = sys.stdout
	sys.stdout = output
	parser.format(formatter)
	sys.stdout = stdout

	return unicode(output.getvalue().decode('utf-8'))

request = RequestCLI()
formatter = Formatter(request)

if __name__ == "__main__":
	# pages/playground\(2f\)SyntaxReference/revisions/00000001
	if len(sys.argv) > 1:
		inputfile = sys.argv[1]
	else:
		inputfile = 'syntaxreference.txt'

	with open(inputfile, 'r') as f:
		text = f.read()
	print moin2doku('test', text)
