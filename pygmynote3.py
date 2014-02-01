#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pygmynote is a command-line tool for storing and managing heterogeneous bit of data like notes, tasks, links, file attachments, etc. Pygmynote is written in Python and uses an SQLite database as its back end.

Thanks to Luis Cabrera Sauco for implementing SQLite and i18 support.
"""

__author__ = "Dmitri Popov [dmpop@linux.com]"
__copyright__ = "Copyleft 2011-2014 Dmitri Popov"
__license__ = "GPLv3"
__version__ = "0.9.01"
__URL__ = "http://www.github.com/dmpop/pygmynote"

import sys
import datetime
import os
import time
import calendar
import gettext
import sqlite3 as sqlite
import tempfile
import subprocess
import shutil
import codecs
import webbrowser

### Settings ###

EDITOR = 'nano'
DB = 'pygmynote.sqlite'
BACKUP = 'pygmynotebackup/' # Note the trailing slash
EXPORT_FILE = 'pygmynote.tsv'
HTML_FILE = 'pygmynote.html'
HTML_FILE_TITLE = 'Pygmynote'

ENC = "UTF-8"
DOMAIN = "pygmynote"

# Terminal colors

class termcolor:
	GREEN = '\033[1;32m'
	BLUE = '\033[1;34m'
	GRAY = '\033[1;30m'
	YELLOW = '\033[1;33m'
	RED = '\033[1;31m'
	END = '\033[1;m'

	def disable(self):
		self.GREEN = ''
		self.BLUE = ''
		self.GRAY = ''
		self.YELLOW = ''
		self.RED = ''
		self.END = ''

try:
	TRANSLATION = gettext.translation(DOMAIN, "./locale")
	_ = TRANSLATION.ugettext
except IOError:
	_ = gettext.gettext


if os.path.exists(DB):
	CREATE = False
else:
	CREATE = True

try:
	conn = sqlite.connect(DB)
	cursor = conn.cursor()
except:
	sys.exit(_("Connection to the SQLite database failed!"))

today = time.strftime("%Y-%m-%d")
command = ""
counter = 0

print (termcolor.GREEN + _("""
           ( 0)
          (( *))
            ||
==========="=="=============
Pygmynote is ready. Pile up!
============================""") + termcolor.END)

print (termcolor.BLUE + _("""\nType \"h\" and press ENTER""") + termcolor.END)

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

print (_("""
-------------------------------------
Pinned records and today's deadlines:
-------------------------------------"""))

cursor.execute ("SELECT id, note, tags FROM notes WHERE type = '3' ORDER BY id ASC")
for row in cursor:
	print ('\n' + termcolor.GREEN + str(row[0]) + termcolor.END + ' ' + unicode(row[1]) + termcolor.GRAY + ' [' + unicode(row[2]) + ']' + termcolor.END)

cursor.execute ("SELECT due, id, note, tags FROM notes WHERE due = '" + today + "' AND type <> '0' ORDER BY id ASC")
for row in cursor:
	print ('\n' + str(row[0]) + ' -- ' + termcolor.GREEN +str(row[1]) + ' ' + termcolor.END + unicode(row[2]) + termcolor.GRAY + ' [' + unicode(row[3]) + ']' + termcolor.END)

while command != "q":

	try:

		command = input('\n>')

		if command == 'h':
			print (termcolor.GREEN + _("""
===================
Pygmynote commands:
===================

i	Insert a new record
l	Insert a new long record
f	Insert a new record with an attachment
s	Save an attachment
u	Update a record
p	Pin a record
x	Unpin a record
n	Search records by note
t	Search records by tag
a	Show active records
ar	Show archived records
tl	Show tasks
at	Show records with attachments
sql	Run a user-defined SQL query
e	Export records as CSV file
g	Generate HTML page with records containing a certain tag
d	Delete a record by its ID
b Backup the database
q	Quit""") + termcolor.END)

		elif command == "i":

# Insert a new record

			rtxt = escapechar(input(_('Note: ')))
			rtags = escapechar(input(_('Tags: ')))
			rdue = input(_('Due date (yyyy-mm-dd). Press ENTER to skip: '))
			rtype = '1'
			sqlquery = "INSERT INTO notes (note, due, tags, type) VALUES ('%s', '%s', '%s', '%s')" % (rtxt, rdue, rtags, rtype)
			cursor.execute(sqlquery)
			conn.commit()
			print (termcolor.GREEN + _('\nRecord has been added.') + termcolor.END)
		elif command == 'l':

# Insert a new long record
# http://stackoverflow.com/questions/3076798/start-nano-as-a-subprocess-from-python-capture-input

			f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
			n = f.name
			f.close()
			subprocess.call([EDITOR, n])
			with open(n) as f:
				rtxt = escapechar(f.read())
			rtags = escapechar(input('Tags: '))
			rdue = input(_('Due date (yyyy-mm-dd). Press Enter to skip: '))
			rtype = '1'
			sqlquery = "INSERT INTO notes (note, due, tags, type) VALUES ('%s', '%s', '%s', '%s')" % (rtxt, rdue, rtags, rtype)
			cursor.execute(sqlquery)
			conn.commit()
			print (termcolor.GREEN + _('\nRecord has been added.') + termcolor.END)
		elif command == 'f':

# Insert a new record with file

			rtxt = escapechar(input(_('Note: ')))
			rtags = escapechar(input(_('Tags: ')))
			rfile = escapechar(input(_('Enter path to file (e.g., /home/user/foo.png): ')))
			rtype='1'
			f=open(rfile.rstrip(), 'rb')
			ablob = f.read()
			f.close()
			cursor.execute("INSERT INTO notes (note, tags, type, ext, file) VALUES('" + rtxt + "', '" + rtags + "', '" + rtype + "', '"  + rfile[-3:] + "', ?)", [sqlite.Binary(ablob)])
			conn.commit()
			print (termcolor.GREEN + _('\nRecord has been added.') + termoclor.END)
		elif command == 's':

# Save file

			recid = input(_('Record id: '))
			outfile=input(_('Specify full path and file name (e.g., /home/user/foo.png): '))
			f=open(outfile, 'wb')
			cursor.execute ("SELECT file FROM notes WHERE id='"  +  recid  +  "'")
			ablob = cursor.fetchone()
			f.write(ablob[0])
			f.close()
			cursor.close()
			conn.commit()
			print (termcolor.GREEN + _('\nFile has been saved.') +termcolor.END)
		elif command == 'n':

# Search records by note

			rtxt = input(_('Search notes for: '))
			cursor.execute("SELECT id, note, tags FROM notes WHERE note LIKE '%"
							 +  rtxt  +  "%'ORDER BY id ASC")
			print ("\n-----")
			for row in cursor:
				print (termcolor.GREEN + '\n' +str(row[0]) + ' ' + termcolor.END + unicode(row[1]) + termcolor.GRAY + ' [' + unicode(row[2]) + ']' + termcolor.END)
				counter = counter + 1
			print ("\n-----")
			print (termcolor.BLUE + _('Record count: ') + termcolor.END + str(counter))
			counter = 0
		elif command == 't':

# Search records by tag

			stag = input (_('Search by tag: '))
			cursor.execute("SELECT id, note, tags FROM notes WHERE tags LIKE '%" + stag + "%' AND type='1' ORDER BY id ASC")
			print ('\n-----')
			for row in cursor:
				print (termcolor.GREEN + '\n' +str(row[0]) + ' ' + termcolor.END + unicode(row[1]) + termcolor.GRAY + ' [' + unicode(row[2]) + ']' + termcolor.END)
				counter = counter + 1
			print ('\n-----')
			print (termcolor.BLUE + _('Record count: ') + termcolor.END + str(counter))
			counter = 0
		elif command == 'a':

# Show active records

			cursor.execute("SELECT id, note, tags FROM notes WHERE type='1' ORDER BY id ASC")
			print ("\n-----")
			for row in cursor:
				print (termcolor.GREEN + '\n' +str(row[0]) + ' ' + termcolor.END + unicode(row[1]) + termcolor.GRAY + ' [' + unicode(row[2]) + ']' + termcolor.END)
				counter = counter + 1
			print ('\n-----')
			print (termcolor.BLUE + _('Record count: ') + termcolor.END + str(counter))
			counter = 0
		elif command == 'ar':

# Show archived records

			cursor.execute("SELECT id, note, tags FROM notes WHERE type='0' ORDER BY id ASC")
			print ('\n-----')
			for row in cursor:
				print (termcolor.GREEN + '\n' +str(row[0]) + ' ' + termcolor.END + unicode(row[1]) + termcolor.GRAY + ' [' + unicode(row[2]) + ']' + termcolor.END)
				counter = counter + 1
			print ('\n-----')
			print (termcolor.BLUE + _('Record count: ') + termcolor.END + str(counter))
			counter = 0
		elif command == 'sql':

# Run a user-defined SQL query

			sqlquery = raw_input ('SELECT id, note, due, tags FROM notes ')
			cursor.execute("SELECT id, note, due, tags FROM notes " + sqlquery)
			print ('\n-----')
			for row in cursor:
				print (termcolor.GREEN + '\n' +str(row[0]) + ' ' + termcolor.END  + unicode(row[1]) + termcolor.GRAY + str(row[2])+ ' [' + unicode(row[3]) + ']' + termcolor.END)
				counter = counter + 1
			print '\n-----'
			print (termcolor.BLUE + _('Record count: ') + termcolor.END + str(counter))
			counter = 0
		elif command == 'u':

# Update a record

			recid = input(_('Record id: '))
			rtype = input(_('Update note [0], tags [1], due date [2], or archive [3]: '))
			if rtype == '0':
				cursor.execute ("SELECT id, note FROM notes WHERE id='"  +  recid  +  "'")
				row = cursor.fetchone()
				f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
				n = f.name
				f.write(row[1].encode(ENC))
				f.close()
				subprocess.call([EDITOR, n])
				with open(n) as f:
					noteupd = escapechar(f.read())
				sqlstr = escapechar(noteupd)
				cursor.execute("UPDATE notes SET note='"  +  sqlstr
								 +  "' WHERE id='"  +  recid  +  "'")
			elif rtype == '1':
				tagupd = input(_('Tags: '))
				sqlstr = escapechar(tagupd)
				cursor.execute("UPDATE notes SET tags='"  +  sqlstr
								 +  "' WHERE id='"  +  recid  +  "'")
			elif rtype == '2':
				dueupd = input(_('Due date: '))
				cursor.execute("UPDATE notes SET due='"  +  dueupd
								 +  "' WHERE id='"  +  recid  +  "'")
			else:
				rtype = '0'
				cursor.execute("UPDATE notes SET type='"  +  rtype
								 +  "' WHERE id='"  +  recid  +  "'")
			conn.commit()
			print (termcolor.GREEN + _('\nRecord has been updated.') + termcolor.END)
		elif command == 'p':

# Pin a record

			recid = raw_input(_('Record id: '))
			cursor.execute("UPDATE notes SET type='3' WHERE id='"  +  recid  + "'")
			conn.commit()
			print termcolor.GREEN + _('\nRecord has been pinned.') +termcolor.END
		elif command == 'x':

# Unpin a record

			recid = raw_input(_('Record id: '))
			cursor.execute("UPDATE notes SET type='1' WHERE id='"  +  recid  + "'")
			conn.commit()
			print termcolor.GREEN + _('\nRecord has been unpinned.') +termcolor.END
		elif command == 'tl':

# Show tasks

			cursor.execute ("SELECT due, id, note, tags FROM notes WHERE due <> '' AND tags NOT LIKE '%private%' AND type = '1' ORDER BY due ASC")
			print ("\n-----")
			now = datetime.datetime.now()
			calendar.prmonth(now.year, now.month)
			for row in cursor:
				print ('\n' + str(row[0]) + ' -- ' + termcolor.GREEN +str(row[1]) + ' ' + termcolor.END + unicode(row[2]) + termcolor.GRAY + ' [' + unicode(row[3]) + ']' + termcolor.END)
				counter = counter + 1
			print ('\n-----')
			print (termcolor.BLUE + _('Record count: ') + termcolor.END + str(counter))
			counter = 0
		elif command == 'at':

# Show records with attachments

			cursor.execute("SELECT id, note, tags, ext FROM notes WHERE ext <> 'None' AND type='1' ORDER BY id ASC")
			print ('\n-----')
			for row in cursor:
				print (termcolor.GREEN + '\n' +str(row[0]) + ' ' + termcolor.END + unicode(row[1]) + termcolor.GRAY + ' [' + unicode(row[2]) + '] ' + termcolor.END + termcolor.HIGHLIGHT + str(row[3]) + termcolor.END)
				counter = counter + 1
			print ('\n-----')
			print (termcolor.BLUE + _('Record count: ') + termcolor.END + str(counter))
			counter = 0
		elif command == 'd':

# Delete a record by its ID

			recid = input(_('Delete note ID: '))
			cursor.execute("DELETE FROM notes WHERE ID='"  +  recid  +  "'")
			print (termcolor.GREEN + _('\nRecord has been deleted.') + termcolor.END)
			conn.commit()
		elif command == 'b':

# Backup the database

			if not os.path.exists(BACKUP):
				os.makedirs(BACKUP)
			shutil.copy('pygmynote.sqlite', BACKUP)
			os.rename(BACKUP + 'pygmynote.sqlite', BACKUP + today + '-pygmynote.sql')
			print (termcolor.GREEN + _('\nBackup copy of the database has been been saved in ') + BACKUP + termcolor.END)
		elif command == 'e':

# Export records

			cursor.execute("SELECT id, note, tags, due FROM notes ORDER BY id ASC")
			if os.path.exists(EXPORT_FILE):
				os.remove(EXPORT_FILE)
			for row in cursor:
				f = EXPORT_FILE
				file = codecs.open(f, 'a', encoding=ENC)
				file.write('%s\t%s\t[%s]\t%s\n' % (row[0], row[1], row[2], row[3]))
				file.close()
			print (termcolor.GREEN + _('\nRecords have been saved in the ') + EXPORT_FILE + _(' file.') + termcolor.END)
		elif command == 'g':

# Generate an HTML file

			stag = escapechar(raw_input(_('Tag: ')))
			cursor.execute("SELECT note, tags FROM notes WHERE tags LIKE '%" + stag + "%' AND type='1' ORDER BY id ASC")
			if os.path.exists(HTML_FILE):
				os.remove(HTML_FILE)
			f = HTML_FILE
			file = codecs.open(f, 'a', encoding=ENC)
			file.write('<html>\n\t<head>\n\t<meta http-equiv="content-type" content="text/html; charset=UTF-8" />\n\t<link href="style.css" rel="stylesheet" type="text/css" media="all" />\n\t<link href="http://fonts.googleapis.com/css?family=Open+Sans:400,300,300italic,400italic,600,600italic,700,700italic,800,800italic" rel="stylesheet" type="text/css">\n\t<title>'+ HTML_FILE_TITLE + '</title>\n\t</head>\n\t<body>\n\n\t<div id="content">\n\t<p class="content"></p>\n\t<h1>Pygmynote</h1>\n\n\t<table border=0>\n')
			for row in cursor:
				file.write('\t<tr><td><p>%s</p></td></tr>\n\t<tr><td><p><small>Tags:<em> %s </small></em></p></td></tr>' % (row[0], row[1]))
			file.write('\n\t</table>\n\n\t<hr>\n\t<center><div class="footer">Generated by <a href="https://github.com/dmpop/pygmynote">Pygmynote</a></div></center>\n\n\t</body>\n</html>')
			file.close()
			print ('\n')
			print (termcolor.GREEN + HTML_FILE + _(' file has been generated.') + termcolor.END)
			webbrowser.open(HTML_FILE)

	except:
		print (_('\n\nError: ') + termcolor.RED + str(sys.exc_info()[0]) + termcolor.END + _(' Please try again.'))

		continue

print (termcolor.YELLOW + _("""
        ( 0)>
       (( *))
         ||
========"=="=========
Bye! Have a nice day.
=====================\n""") + termcolor.END)

cursor.close()
conn.close()
