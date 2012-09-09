#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pygmynote is a command-line tool for storing and managing heterogeneous bit of data, including notes, tasks, links, and file attachments.Pygmynote is written in Python and uses a SQLite database as its back end.

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

__author__ = "Dmitri Popov [dmpop@linux.com]"
__copyright__ = "Copyright 2011, 2012 Dmitri Popov"
__license__ = "GPLv3"
__version__ = "0.7.13"
__URL__ = "http://www.github.com/dmpop"

import sys
import datetime
import os
import time
import calendar
import gettext
import sqlite3 as sqlite

DEBUG = False

DOMAIN = "pygmynote"

try:
	TRANSLATION = gettext.translation(DOMAIN, ".")
	_ = TRANSLATION.ugettext
except IOError:
	_ = gettext.gettext

DB = "pygmynote.db"
ENC = "utf-8"

if os.path.exists(DB):
	if DEBUG == True:
		print ("The database already exists.")
	CREATE = False
else:
	if DEBUG == False:
		print ("Creating a new database.")
	CREATE = True

try:
	if DEBUG == False:
		conn = sqlite.connect(DB)
	else:
		conn = sqlite.connect(DB, timeout=0.5, encoding=ENC)
	cursor = conn.cursor()
except:
	sys.exit("Connection to the SQLite database failed!")

today = time.strftime("%Y-%m-%d")
command = ""
counter = 0

print ("""\033[1;32m
           ( 0)>
          (( *))
            ||
==========="=="=============
Pygmynote is ready. Pile up!
============================\033[1;m\n""")

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

print ("Today\"s deadlines:")
cursor.execute ("SELECT due, id, note, tags FROM notes WHERE due = '" + today + "' AND type <> '0' ORDER BY id ASC")
for row in cursor:
	print ("\n%s -- \033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m" % (row[0], row[1], row[2], row[3]))

while command != "q":

	try:

		command = input('\n>')

		if command == 'help':
			print ("""
===================
Pygmynote commands:
===================

i	Insert new record
f	Insert new record with an attachment
s	Save attachment
u	Update record
n	Search records by note
t	Search records by tag
a	Show active records
p	Show records with the \"private" tag
h	Show archived records
tl	Show tasks
at	Show records with attachments
w	Export records as CSV file
d	Delete record by its ID
q	Quit""")

		elif command == "i":

# Insert new record

			ntext = escapechar(input('Note: '))
			ntags = escapechar(input('Tags: '))
			ndue = input('Due date (yyyy-mm-dd). Press Enter to skip: ')
			ntype = '1'
			sqlquery = \
				"INSERT INTO notes (note, due, tags, type) VALUES ('%s', '%s', '%s', '%s')"\
				% (ntext, ndue, ntags, ntype)
			cursor.execute(sqlquery)
			conn.commit()
			print ('\nRecord has been added.')
		elif command == 'f':

# Insert new record with file

			ntext = escapechar(input('Note: '))
			ntags = escapechar(input('Tags: '))
			notefile = escapechar(input('Enter path to file: '))
			ntype='1'
			f=open(notefile.rstrip(), 'rb')
			ablob = f.read()
			f.close()
			cursor.execute("INSERT INTO notes (note, tags, type, ext, file) VALUES('" + ntext + "', '" + ntags + "', '" + ntype + "', '"  + notefile[-3:] + "', ?)", [sqlite.Binary(ablob)])
			conn.commit()
			print ('\nRecord has been added.')
		elif command == 's':

# Save file

			recid = input('Record id: ')
			outfile=input('Specify full path and file name (e.g., /home/user/loremipsum.odt): ')
			f=open(outfile, 'wb')
			cursor.execute ("SELECT file FROM notes WHERE id='"  +  recid  +  "'")
			ablob = cursor.fetchone()
			f.write(ablob[0])
			f.close()
			cursor.close()
			conn.commit()
			print ('\nFile has been saved.')
		elif command == 'n':

# Search records by note

			ntext = input('Search notes for: ')
			cursor.execute("SELECT id, note, tags FROM notes WHERE note LIKE '%"
							 +  ntext  +  "%'ORDER BY id ASC")
			print ("\n-----")
			for row in cursor:
				print ("\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m" % (row[0], row[1], row[2]))
				counter = counter + 1
			print ("\n-----")
			print ("\033[1;34mRecord count:\033[1;m %s") % counter
			counter = 0
		elif command == 't':

# Search records by tag

			stag = input ('Search by tag: ')
			cursor.execute("SELECT id, note, tags FROM notes WHERE tags LIKE '%"
							 +  stag  +  "%' AND type='1' ORDER BY id ASC")
			print ('\n-----')
			for row in cursor:
				print ('\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2]))
				counter = counter + 1
			print ('\n-----')
			print ('\033[1;34mRecord count:\033[1;m %s' % counter)
			counter = 0
		elif command == 'p':

# Show private records

			stag = 'private'
			cursor.execute("SELECT id, note, tags FROM notes WHERE tags LIKE '%"
							 +  stag  +  "%' AND type='1' ORDER BY id ASC")
			print ("\n-----")
			for row in cursor:
				print ("\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m" % (row[0], row[1], row[2]))
				counter = counter + 1
			print ('\n-----')
			print ('\033[1;34mRecord count:\033[1;m %s' % counter)
			counter = 0
		elif command == 'a':

# Show active records

			cursor.execute("SELECT id, note, tags FROM notes WHERE type='1' ORDER BY id ASC")
			print ("\n-----")
			for row in cursor:
				print ("\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m" % (row[0], row[1], row[2]))
				counter = counter + 1
			print ('\n-----')
			print ('\033[1;34mRecord count:\033[1;m %s' % counter)
			counter = 0
		elif command == 'h':

# Show hidden records

			cursor.execute("SELECT id, note, tags FROM notes WHERE type='0' ORDER BY id ASC")
			print ('\n-----')
			for row in cursor:
				print ('\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m' % (row[0], row[1], row[2]))
				counter = counter + 1
			print ('\n-----')
			print ('\033[1;34mRecord count:\033[1;m %s' % counter)
			counter = 0
		elif command == 'u':

# Update note

			recid = input('Record id: ')
			ntype = input('Update note [0], tags [1], due date [2], or archive [3]: ')
			if ntype == '0':
				cursor.execute ("SELECT id, note FROM notes WHERE id='"  +  recid  +  "'")
				row = cursor.fetchone()
				print ('Current contents: %s' % row[1])
				noteupdate = input('Note: ')
				sqlstr = escapechar(noteupdate)
				cursor.execute("UPDATE notes SET note='"  +  sqlstr
								 +  "' WHERE id='"  +  recid  +  "'")
			elif ntype == '1':
				tagupdate = input('Tags: ')
				sqlstr = escapechar(tagupdate)
				cursor.execute("UPDATE notes SET tags='"  +  sqlstr
								 +  "' WHERE id='"  +  recid  +  "'")
			elif ntype == '2':
				dueupdate = input('Due date: ')
				cursor.execute("UPDATE notes SET due='"  +  dueupdate
								 +  "' WHERE id='"  +  recid  +  "'")
			else:
				ntype = '0'
				cursor.execute("UPDATE notes SET type='"  +  ntype
								 +  "' WHERE id='"  +  recid  +  "'")
			conn.commit()
			print ('\nRecord has been updated.')
		elif command == 'tl':

# Show tasks

			cursor.execute ("SELECT due, id, note, tags FROM notes WHERE due <> '' AND tags NOT LIKE '%private%' AND type = '1' ORDER BY due ASC")
			print ("\n-----")
			now = datetime.datetime.now()
			calendar.prmonth(now.year, now.month)
			for row in cursor:
				print ("\n%s -- \033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m" % (row[0], row[1], row[2], row[3]))
				counter = counter + 1
			print ('\n-----')
			print ('\033[1;34mRecord count:\033[1;m %s' % counter)
			counter = 0
		elif command == 'at':

# Show records with attachments

			cursor.execute("SELECT id, note, tags, ext FROM notes WHERE ext <> 'None' AND type='1' ORDER BY id ASC")
			print ('\n-----')
			for row in cursor:
				print ('\n\033[1;32m%s\033[1;m %s \033[1;30m[%s]\033[1;m \033[1;43m%s\033[1;m' % (row[0], row[1], row[2], row[3]))
				counter = counter + 1
			print ('\n-----')
			print ('\033[1;34mRecord count:\033[1;m %s' % counter)
			counter = 0
		elif command == 'd':

# Delete note by its ID

			recid = input('Delete note ID: ')
			cursor.execute("DELETE FROM notes WHERE ID='"  +  recid  +  "'")
			print ('\nRecord has been deleted.')
			conn.commit()
		elif command == 'w':

# Save all notes as pygmynote.txt

			cursor.execute("SELECT id, note, tags, due FROM notes ORDER BY id ASC")
			if os.path.exists('pygmynote.txt'):
				os.remove('pygmynote.txt')
			for row in cursor:
				filename = 'pygmynote.txt'
				file = open(filename, 'a')
				file.write('%s\t%s\t[%s]\t%s\n' % (row[0], row[1], row[2], row[3]))
				file.close()
			print ('\nRecords have been saved in the pygmynote.txt file.')

	except:
		print ('\n\n\033[1;31mSomething went wrong. Try again.\033[1;m')

		continue

print ("""\033[1;33m
        ( 0)>
       (( *))
         ||
========"=="=========
Bye! Have a nice day.
=====================\033[1;m\n""")

cursor.close()
conn.close()