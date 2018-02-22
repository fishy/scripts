A collection of my various scripts.

## onepwd.py

A desktop companion for the chrome extension
[One Password](https://chrome.google.com/webstore/detail/pahmlghhaoabdlhnkmmjbkcmdamjccjj).

## fix-epub.py

A script to add "xml:lang" parameter to html tags within a epub file.

https://wang.yuxuan.org/blog/item/2011/01/fix-epubs

## columbus.py

A script for Columbus V-900 GPS.

https://wang.yuxuan.org/blog/item/2009/04/a-script-for-columbus-v-900-gps

## convertip.py

A script to convert a line contains start and end IP into IP mask format. 

https://wang.yuxuan.org/blog/item/2009/04/python-script-to-convert-from-ip-range-to-ip-mask

## ga-rss.php

A RSS generator for Garfield daily comic.

https://fishy.buddie5.com/item/438

## UsePhoneticName.py

A script to use Phonetic Name fields in Apple Address Book to replace the Name fields.

https://fishy.buddie5.com/item/727

## torrent.py

A script to add tracker(s) to a torrent.

## unlink.sh

A script to unlink symbolic links under current directory that matches a regexp.

Useful for uninstalling softwares, like TeXLive.

https://wang.yuxuan.org/blog/item/2007/01/selective-unlink-script-to-uninstall-texlive

## resize-for-picasa.sh

A script to resize all jpegs on current directory for Picasa Web Album.

## refresh-applications.sh

A script to put a random file under /Applications and then remove it.

Useful for putting /Applications stack onto your Mac OS X dock.

## update-buckversion.sh

A script to update the .buckversion file at current directory.

## rssplus.py

A python cgi to get RSS from someone's public Google+ posts.

## doorcode.py

A script to generate a random code (to be used on smart locks).

## pinentry-local.sh

A selector for pinentry on Mac,
auto chooses `pinentry-curses` inside ssh sessions and chooses `pinentry-mac`
outside of ssh sessions.
It can be set as your `pinentry-program` inside your `gpg-agent.conf` file.

## reload-gpg-agent.sh

Kills gpg-agent and then reload it.
This helps use the different pinentry when you are switching between GUI and
TTY. (ssh and local, see pinentry-local.sh above)

## LICENSE

All scripts licensed under
[BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause),
refer to the LICENSE file for more details.

## projtags.vim

To make it compatiable with
[pathogen.vim](https://github.com/tpope/vim-pathogen)
(or any other vim plugin manager), projtags.vim now has its own repository at:

https://github.com/fishy/projtags-vim
