#! /usr/bin/env python
#
# Creates a project directory structure based on the Autotools/check
# model for building and testing, as show in the example below.
# 
# |-- Makefile.am
# |-- README
# |-- configure.ac
# |-- src
# |   |-- Makefile.am
# |   |-- main.c
# |   |-- money.c
# |   `-- money.h
# `-- tests
#     |-- Makefile.am
#     `-- check_money.c

import argparse
import os
import re
from os.path import join, exists
from subprocess import call


parser = argparse.ArgumentParser(description='Create a project directory.')
parser.add_argument('dir', metavar='d',
	                help='name for top-level project directory',
	                default='sample')
parser.add_argument('--version',
	                help='version number of project')
parser.add_argument('--email',
	                help='e-mail for bug reports',
	                default='example@example.com')
args = parser.parse_args()


tests_makefile_am = ['## Process this file with automake to produce Makefile.in',
                     '',
                     'TESTS = check_' + args.dir,
                     'check_PROGRAMS = check_' + args.dir,
                     'check_' + args.dir + '_SOURCES = check_' + args.dir + 
                     '.c $(top_builddir)/src/' + args.dir + '.h',
                     'check_' + args.dir + '_CFLAGS = @CHECK_CFLAGS@',
                     'check_' + args.dir + '_LDADD = $(top_builddir)/src/lib' + 
                     args.dir + '.la @CHECK_LIBS@']

tests_c = ['int main(void) {',
           '',
           '\t' + 'return 0;',
           '}']

src_makefile_am = ['## Process this file with automake to produce Makefile.in',
                   '',
                   'lib_LTLIBRARIES = lib' + args.dir + '.la'
                   'lib' + args.dir + '_la_SOURCES = ' + args.dir + 
                   '.c ' + args.dir + '.h',
                   '',
                   'bin_PROGRAMS = main',
                   'main_SOURCES = main.c',
                   'main_LDADD = lib' + args.dir + '.la']

src_h = ['#ifndef ' + args.dir.upper() + '_H',
         '#define ' + args.dir.upper() + '_H',
         '',
         '#endif /* ' + args.dir.upper() + '_H */']

if not exists(args.dir):
    os.makedirs(args.dir)

f = open(join(args.dir, 'Makefile.am'), 'a')
f.write('SUBDIRS = src . tests')
f.close()
f = open(join(args.dir, 'README'), 'a')
f.close()
f = open(join(args.dir, 'configure.ac'), 'a')
old_text = open(join(join(os.environ.get('HOME'), 'scripts'), '.configure.ac')).read()
new_text = old_text.replace('PROJ', args.dir)
new_text = new_text.replace('VERS', args.version)
new_text = new_text.replace('E_MAIL', args.email)
f.write(new_text)
f.close()

try:
	os.mkdir(join(args.dir, 'tests'))
except IOError:
	print 'could not create tests directory'
else:
	f = open(join(join(args.dir, 'tests'), 'Makefile.am'), 'a')
	for line in tests_makefile_am:
		f.write(line + '\n')
	f.close()
	f = open(join(join(args.dir, 'tests'), 'check_' + args.dir + '.c'), 'a')
	for line in tests_c:
		f.write(line + '\n')
	f.close()

try:
	os.mkdir(join(args.dir, 'src'))
except IOError:
	print 'could not create src directory'
else:
	f = open(join(join(args.dir, 'src'), 'Makefile.am'), 'a')
	f.close()
	f = open(join(join(args.dir, 'src'), 'main.c'), 'a')
	f.close()
	f = open(join(join(args.dir, 'src'), args.dir + '.c'), 'a')
	f.close()
	f = open(join(join(args.dir, 'src'), args.dir + '.h'), 'a')
	for line in src_h:
		f.write(line + '\n')
	f.close()

os.chdir(args.dir)
call(['autoreconf', '--install'])
call('./configure')
call('make')