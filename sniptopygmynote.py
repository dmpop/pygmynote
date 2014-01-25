#!/usr/bin/env python
import pygtk, gtk, wx
import sqlite3 as sqlite
pygtk.require('2.0')

DB = 'pygmynote.sqlite'

conn = sqlite.connect(DB)
cursor = conn.cursor()

def escapechar(sel):
	sel=sel.replace("\'", "\''")
	sel=sel.replace("\"", "\"""")
	return sel

clipboard = gtk.clipboard_get()
snip = clipboard.wait_for_text()

app = wx.PySimpleApp()
tags = wx.TextEntryDialog(None, "Tags:","Add Tags", "", style=wx.OK|wx.CANCEL)
if tags.ShowModal() == wx.ID_OK:
    notetags = tags.GetValue()
tags.Destroy()

notetext = escapechar(snip)
notedue = ""
notetype = "1"
sqlquery = \
"INSERT INTO notes (note, due, tags, type) VALUES ('%s', '%s', '%s', '%s')"\
% (notetext, notedue, notetags, notetype)
cursor.execute(sqlquery)
conn.commit()

message = wx.MessageDialog(None, "Snip saved. All done!", "Done", wx.OK)
message.ShowModal()
message.Destroy()
