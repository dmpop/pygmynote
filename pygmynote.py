#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pygmynote is a command-line tool for storing and managing heterogeneous bit of data like notes, tasks, links, file attachments, etc. Pygmynote is written in Python and uses a SQLite database as its back end.

Thanks to Luis Cabrera Sauco for implementing SQLite and i18 support.

i18:
~~~~
pygettext -k_ -o pygmynote.po pygmynote.py
msgfmt pygmynote.po -o pygmynote.mo
mkdir -p es/LC_MESSAGES
mv pygmynote.mo es/LC_MESSAGES/pygmynote.mo
mv pygmynote.po es/LC_MESSAGES/pygmynote.po

test_i18:
~~~~~~~~~
$ LANGUAGE=es python pygmynote.py
"""

__author__ = 'Dmitri Popov [dmpop@linux.com]'
__copyright__ = 'Copyleft 2011-2014 Dmitri Popov'
__license__ = 'GPLv3'
__version__ = '0.9.01'
__URL__ = 'http://www.github.com/dmpop/pygmynote'

import sys
import datetime
import os
import time
import calendar
import gettext
import tempfile
import subprocess

EDITOR = 'nano'
DB = 'pygmynote.sqlite'

ENC = 'utf-8'
DEBUG = False
DOMAIN = 'pygmynote'

try:
	TRANSLATION = gettext.translation(DOMAIN, '.')
	_ = TRANSLATION.ugettext
except IOError:
	_ = gettext.gettext

try:
	import sqlite3 as sqlite
	if DEBUG == True:
		print 'Use sqlite3, with python %s' % sys.version
except ImportError:
	from pysqlite2 import dbapi2 as sqlite
	if DEBUG == True:
		print 'Use pysqlite2, with python %s' % sys.version

if os.path.exists(DB):
	if DEBUG == True:
		print 'The database already exists.'
	CREATE = False
else:
	if DEBUG == False:
		print 'Creating a new database.'
	CREATE = True

try:
	if DEBUG == False:
		conn = sqlite.connect(DB)
	else:
		conn = sqlite.connect(DB, timeout=0.5, encoding=ENC)
	cursor = conn.cursor()
except:
	sys.exit('Connection to the SQLite database failed!')

today = time.strftime('%Y-%m-%d')
command = ''
counter = 0

print """\033[1;32m
           ( 0)>
          (( *))
            ||
==========="=="=============
Pygmynote is ready. Pile up!
============================\033[1;m\n
\033[1;36mType \"help\" and press ENTER\033[1;m"""

def escapechar(sel):
	sel=sel.replace("\'", "\''")
	sel=sel.replace("\"", "\"""")
	return sel


if CREATE == True:
	CREATE_SQL = \
		"CREATE TABLE notes (\
		id INTEGER PRIMARY KEY UNIQUE NOT NULL,\
		note VARCHAR(1024),\
		file BLOB,\
		due DATE,\
		type VARCHAR(3),\
		ext VARCHAR(3),\
		tags VARCHAR(256));"
	cursor.execute(CREATE_SQL)
	conn.commit()

print """
------------------
Today\'s deadlines:
------------------"""
cursor.execute ("SELECT due, id, note, tags FROM notes WHERE due = '" + today + "' AND type <> '0' ORDER BY id ASC")
for row in cursor:
	print '\n%s -- \033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2], row[3])

while command != 'q':

	try:

		command = raw_input('\n>')

		if command == 'help':
			print """
===================
Pygmynote commands:
===================

i	Insert new record
l	Insert long record
f	Insert new record with an attachment
s	Save attachment
u	Update record
n	Search records by note
t	Search records by tag
a	Show active records
ar	Show archived records
tl	Show tasks
at	Show records with attachments
w	Export records as CSV file
p	Generate an HTML page witt records containing a certain tag
d	Delete record by its ID
q	Quit"""

		elif command == 'i':

# Insert new record

			rtxt = escapechar(raw_input('Note: '))
			rtags = escapechar(raw_input('Tags: '))
			rdue = raw_input('Due date (yyyy-mm-dd). Press ENTER to skip: ')
			rtype = "1"
			sqlquery = \
				"INSERT INTO notes (note, due, tags, type) VALUES ('%s', '%s', '%s', '%s')"\
				% (rtxt, rdue, rtags, rtype)
			cursor.execute(sqlquery)
			conn.commit()
			print '\nRecord has been added.'
		elif command == 'l':
		
		# Insert long record
			# http://stackoverflow.com/questions/3076798/start-nano-as-a-subprocess-from-python-capture-input
			f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
			n = f.name
			f.close()
			subprocess.call([EDITOR, n])
			with open(n) as f:
				rtxt = escapechar(f.read())
			rtags = escapechar(raw_input('Tags: '))
			rdue = raw_input('Due date (yyyy-mm-dd). Press Enter to skip: ')
			rtype = "1"
			sqlquery = \
				"INSERT INTO notes (note, due, tags, type) VALUES ('%s', '%s', '%s', '%s')"\
				% (rtxt, rdue, rtags, rtype)
			cursor.execute(sqlquery)
			conn.commit()
			print '\nRecord has been added.'
		elif command == 'f':

# Insert new record with file

			rtxt = escapechar(raw_input('Note: '))
			rtags = escapechar(raw_input('Tags: '))
			rfile = escapechar(raw_input('Enter path to file: '))
			rtype="1"
			f=open(rfile.rstrip(), 'rb')
			ablob = f.read()
			f.close()
			cursor.execute("INSERT INTO notes (note, tags, type, ext, file) VALUES('" + rtxt + "', '" + rtags + "', '" + rtype + "', '"  + rfile[-3:] + "', ?)", [sqlite.Binary(ablob)])
			conn.commit()
			print '\nRecord has been added.'
		elif command == 's':

# Save file

			recid = raw_input('Record id: ')
			outfile=raw_input('Specify full path and file name (e.g., /home/user/loremipsum.odt): ')
			f=open(outfile, 'wb')
			cursor.execute ("SELECT file FROM notes WHERE id='"  +  recid  +  "'")
			ablob = cursor.fetchone()
			f.write(ablob[0])
			f.close()
			cursor.close()
			conn.commit()
			print '\nFile has been saved.'
		elif command == 'n':

# Search records by note

			rtxt = raw_input('Search notes for: ')
			cursor.execute("SELECT id, note, tags FROM notes WHERE note LIKE '%"
							 +  rtxt  +  "%'ORDER BY id ASC")
			print '\n-----'
			for row in cursor:
				print '\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2])
				counter = counter + 1
			print '\n-----'
			print '\033[1;34mRecord count:\033[1;m %s' % counter
			counter = 0
		elif command == 't':

# Search records by tag

			stag = raw_input ('Search by tag: ')
			cursor.execute("SELECT id, note, tags FROM notes WHERE tags LIKE '%" +  stag + "%' AND type='1' ORDER BY id ASC")
			print '\n-----'
			for row in cursor:
				print '\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2])
				counter = counter + 1
			print '\n-----'
			print '\033[1;34mRecord count:\033[1;m %s' % counter
			counter = 0
		elif command == 'a':

# Show active records

			cursor.execute("SELECT id, note, tags FROM notes WHERE type='1' ORDER BY id ASC")
			print '\n-----'
			for row in cursor:
				print '\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2])
				counter = counter + 1
			print '\n-----'
			print '\033[1;34mRecord count:\033[1;m %s' % counter
			counter = 0
		elif command == 'ar':

# Show archived records

			cursor.execute("SELECT id, note, tags FROM notes WHERE type='0' ORDER BY id ASC")
			print '\n-----'
			for row in cursor:
				print '\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2])
				counter = counter + 1
			print '\n-----'
			print '\033[1;34mRecord count:\033[1;m %s' % counter
			counter = 0
		elif command == 'u':

# Update record

			recid = raw_input('Record id: ')
			rtype = raw_input('Update note [0], tags [1], due date [2], or archive [3]: ')
			if rtype == '0':
				cursor.execute ("SELECT id, note FROM notes WHERE id='"  +  recid  +  "'")
				row = cursor.fetchone()
				f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
				n = f.name
				f.write('%s' % row[1])
				f.close()
				subprocess.call([EDITOR, n])
				with open(n) as f:
					noteupd = escapechar(f.read())
				sqlstr = escapechar(noteupd)
				cursor.execute("UPDATE notes SET note='"  +  sqlstr
								 +  "' WHERE id='"  +  recid  +  "'")
			elif rtype == '1':
				tagupd = raw_input('Tags: ')
				sqlstr = escapechar(tagupd)
				cursor.execute("UPDATE notes SET tags='"  +  sqlstr
								 + "' WHERE id='"  +  recid  +  "'")
			elif rtype == '2':
				dueupd = raw_input('Due date: ')
				cursor.execute("UPDATE notes SET due='"  +  dueupd
								 +  "' WHERE id='"  +  recid  +  "'")
			else:
				rtype = '0'
				cursor.execute("UPDATE notes SET type='"  +  rtype
								 +  "' WHERE id='"  +  recid  +  "'")
			conn.commit()
			print '\nRecord has been updated.'
		elif command == 'tl':

# Show tasks

			cursor.execute ("SELECT due, id, note, tags FROM notes WHERE due <> '' AND tags NOT LIKE '%private%' AND type = '1' ORDER BY due ASC")
			print '\n-----'
			now = datetime.datetime.now()
			calendar.prmonth(now.year, now.month)
			for row in cursor:
				print '\n%s -- \033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2], row[3])
				counter = counter + 1
			print '\n-----'
			print '\033[1;34mRecord count:\033[1;m %s' % counter
			counter = 0
		elif command == 'at':

# Show records with attachments

			cursor.execute("SELECT id, note, tags, ext FROM notes WHERE ext <> 'None' AND type='1' ORDER BY id ASC")
			print '\n-----'
			for row in cursor:
				print '\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m \033[1;43m%s\033[1;m' % (row[0], row[1], row[2], row[3])
				counter = counter + 1
			print '\n-----'
			print '\033[1;34mRecord count:\033[1;m %s' % counter
			counter = 0
		elif command == 'd':

# Delete record by its ID

			recid = raw_input('Delete note ID: ')
			cursor.execute("DELETE FROM notes WHERE ID='"  +  recid  +  "'")
			print '\nRecord has been deleted.'
			conn.commit()
		elif command == 'w':

# Save all records in pygmynote.txt

			cursor.execute("SELECT id, note, tags, due FROM notes ORDER BY id ASC")
			if os.path.exists('pygmynote.txt'):
				os.remove('pygmynote.txt')
			for row in cursor:
				fname = 'pygmynote.txt'
				file = open(fname, 'a')
				file.write('%s\t%s\t[%s]\t%s\n' % (row[0], row[1], row[2], row[3]))
				file.close()
			print '\nRecords have been saved in the pygmynote.txt file.'
		elif command == 'p':

# Generate pygmynote.html

			stag = escapechar(raw_input('Tag: '))
			cursor.execute("SELECT note, tags FROM notes WHERE tags LIKE '%" + stag + "%' AND type='1' ORDER BY id ASC")
			if os.path.exists('pygmynote.html'):
				os.remove('pygmynote.html')
			f = 'pygmynote.html'
			file = open(f, 'a')
			file.write('<html>\n\t<head>\n\t<meta http-equiv="content-type" content="text/html; charset=UTF-8" />\n\t<link href="style.css" rel="stylesheet" type="text/css" media="all" />\n\t<link href="http://fonts.googleapis.com/css?family=Open+Sans:400,300,300italic,400italic,600,600italic,700,700italic,800,800italic" rel="stylesheet" type="text/css">\n\t<title>Pygmynote</title>\n\t</head>\n\t<body>\n\n\t<div id="content">\n\t<p class="content"></p>\n\t<h1>Pygmynote</h1>\n\n\t<table border=0>\n')
			for row in cursor:
				file.write('\t<tr><td><hr><p>%s</p></td></tr>\n\t<tr><td><p><small>Tags:<em> %s </small></em></p></td></tr>' % (row[0], row[1]))
			file.write('\n\t</table>\n\n\t<hr>\n\n\t</body>\n</html>')
			file.close()
			print '\npygmynote.html file has been generated.'

	except:
		print '\n\nError: \033[1;31m' + str(sys.exc_info()[0]) + '\033[1;m Please try again.'

		continue

print """\033[1;33m
         ( 0)>
        (( *))
          ||
========"=="=========
Bye! Have a nice day.
=====================\033[1;m\n"""

cursor.close()
conn.close()
