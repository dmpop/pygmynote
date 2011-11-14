= PYGMYNOTE =

Pygmynote is a command-line tool for storing and managing heterogeneous bit of data, including notes, tasks, links, and file attachments.Pygmynote is written in Python and uses a SQLite database as its back end

Copyright 2010, 2011 Dmitri Popov


This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,MA 02110-1301, USA.

Source code:
https://github.com/dmpop/pygmynote

==CHANGELOG==

VERSION 0.7.9 2011-11-14
  * Minor fixes and cosmetic tweaks.

VERSION 0.7.7 2011-07-09
  * Minor tweaks
  * Source code is now hosted at GitHub

VERSION 0.7.5 2010-11-09
  * Error handling added
  * Cosmetic tweaks
  * Open URL command removed
  * Show records with attachments command added

VERSION 0.7.1 2010-08-03
  * Added support for records with attachement
  * Various tweaks and fixes

VERSION 0.5.3 2010-07-29
  * "help" command replaces "h". "h" command shows hidden records. "a" command shows active records
  * Minor tweaks and fixes
  * Added a pinch of color

VERSION 0.5.1 2010-07-17
  * Minor tweaks and a lot of fixes
  * Added the ability to mark records as hidden and display only active records (useful when using Pygmynote to track tasks)
  * Added the ability to import notes from text files
  * Added the ability to specify deadlines
  * The script displays current deadlines at the startup
  * SQL queries tweaked
  * Email functionality removed

VERSION 0.3.1 2009-09-27
  * Pygmynote now uses an SQLite database
  * i18 support and Spanish translation added
  * Export to text command removed

VERSION 0.2.0 2008-08-14
  * Email reminders feature added
  * Update command now allows to update tags
  * Calendar command displays current date

VERSION 0.1.0 2008-08-10
  * The script now treats " and ' correctly when inserting and updating notes
  * Calendar feature added
  * Email reminders feature added

VERSION 0.0.1 2008-08-07
  * The very first public release
