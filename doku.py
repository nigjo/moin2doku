#!/usr/bin/python
# -*- coding: utf-8 -*-
# Setup VIM: ex: noet ts=2 sw=2 :
#
# Python side Bridge of accessing DokuWiki functions from Python.
# See README for details.
#
# Author: Elan Ruusamäe <glen@pld-linux.org>
# Version: 1.0

import sys
import subprocess

from MoinMoin import log
logging = log.getLogger(__name__)

class DokuWiki:
	def __init__(self):
		self.callcache = {}

	def __getattr__(self, method):
		def wrap(method):
			def wrapped(*args):
				return self.__call(method, *args)
			return wrapped
		return wrap(method)

	def __call(self, method, *args):
		args = list(args)
		uargs = []
		for arg in args:
			try:
				arg.decode('utf-8')
				#already UTF-8 ready
				uargs.append(arg)
			except UnicodeError:
				uargs.append(arg.encode('utf-8'))
		key = "%s:%s" % (method, ",".join(uargs))
		if not self.callcache.has_key(key):
			cmd = ['php', './doku.php', method ] + uargs
			res = subprocess.Popen(cmd, stdin = None, stdout = subprocess.PIPE, stderr = sys.stderr, close_fds = False).communicate()
			self.callcache[key] = unicode(res[0].decode('utf-8'))
			print "%s->%s" % (cmd, self.callcache[key])
		return self.callcache[key]
