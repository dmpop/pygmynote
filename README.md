#Pygmynote

Pygmynote is a command-line tool for storing and managing heterogeneous bit of data like notes, tasks, links, file attachments, etc. Pygmynote is written in Python and uses an SQLite database as its back end.

##Dependencies

- Python 2.x or 3.x
- nano or any other text editor

##Installation

Clone the repository using the `git clone https://github.com/dmpop/pygmynote.git` command. Done! By default, Pygmynote is configured to use the nano text editor, bu you can change that by changing the *EDITOR* variable in the script.

##Usage

Open terminal, switch to the *pygmynote* directory and run the _pygmynote.py_ script in the terminal. Type __help__ and press `Enter` to list the available commands.

###Pygmysnip

The Pygmysnip part of Pygmynote can be used to publish records in the *pygmynote.sqlite* database containing *snip* tag. Pygmysnip requires a machine running Apache (or another web server) and PHP. To install Pygmysnip, copy the *pygmynote.sqlite* database into the the *pygmysnip* directory, and move the latter to the root of your server. To access Pygmysnip, point a browser to http://127.0.0.1/pygmysnip (replace *127.0.0.1* with the actual IP address or domain name of your server).

##License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,MA 02110-1301, USA.

_Copyleft 2010-2014 Dmitri Popov_

Source code: [https://github.com/dmpop/pygmynote](https://github.com/dmpop/pygmynote)
