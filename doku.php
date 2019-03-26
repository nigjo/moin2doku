#!/usr/bin/php
<?php
# -*- coding: utf-8 -*-
# Setup VIM: ex: noet ts=2 sw=2 :
#
# PHP side Bridge of accessing DokuWiki functions from Python.
# See README for details.
#
# Author: Elan Ruusamäe <glen@pld-linux.org>
# Version: 1.0
#
# You should probably adjust path to DOKU_INC.

if ('cli' != php_sapi_name()) die();

//add to following define of 'DOKU_INC' to your "doku.local.php" file and adjust the path:
//define('DOKU_INC', '/home/caddy/wikifarm/dokuwiki/dokuwiki/');
//define('DOKU_INC', "d:/website/wwwroot/dokuwiki/" );
require_once './doku.local.php';

require_once DOKU_INC.'inc/init.php';
require_once DOKU_INC.'inc/common.php';
require_once DOKU_INC.'inc/cli.php';

# disable gzip regardless of config, then we don't have to compress when converting
$conf['compression'] = 0; //compress old revisions: (0: off) ('gz': gnuzip) ('bz2': bzip)

# override start page, as there's currently configured temporary frontpage
$conf['start'] = 'start'; //name of start page

function strip_dir($dir, $fn) {
	global $conf;
	return end(explode($dir.'/', $fn, 2));
}

$action = $argv[1];
$argPage = $argv[2];
//filext = $argv[3];

switch ($action) {
case 'cleanID':
	echo cleanID($argPage);
	break;
case 'wikiFN':
	if ($argc > 3 && $argv[3]) {
		echo strip_dir($conf['olddir'], wikiFN($argPage, $argv[3]));
	} else {
		echo strip_dir($conf['datadir'], wikiFN($argPage));
	}
	break;
case 'mediaFN':
	echo strip_dir($conf['mediadir'], mediaFN($argPage));
	break;
case 'metaFN':
	echo strip_dir($conf['metadir'], metaFN($argPage, $argv[3]));
	break;
case 'getNS':
	echo getNS($argPage);
	break;
case 'getId':
	echo getId();
	break;
default:
	die("Unknown knob: {$action}");
}
