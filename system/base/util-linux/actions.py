#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

pisitools.cflags.add("-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64")
pisitools.cflags.sub("-O[\d]", "-Os")
shelltools.export("PYTHON", "/usr/bin/python3")

def setup():
    shelltools.export("SUID_CFLAGS", "-fpie")
    shelltools.export("SUID_LDFLAGS", "-pie -Wl,-z,relro -Wl,-z,now")
    shelltools.export("AUTOPOINT", "/bin/true")

    options = "\
               --disable-rpath \
               --disable-silent-rules \
               --disable-use-tty-group \
               --disable-su  \
               --disable-last \
               --disable-mesg \
               --disable-vipw \
               --disable-wall \
               --disable-login \
               --disable-newgrp \
               --disable-nologin \
               --disable-runuser \
               --disable-sulogin \
               --disable-utmpdump \
               --disable-chfn-chsh \
               --without-systemd \
               --without-selinux \
               --enable-gtk-doc-html=no \
               --disable-makeinstall-chown \
               --disable-socket-activation \
               --without-systemdsystemunitdir \
              "

    if get.buildTYPE() == "emul32":
        options += "\
                     --prefix=/emul32 \
                     --bindir=/emul32/bin \
                     --sbindir=/emul32/sbin \
                     --libdir=/usr/lib32 \
                     --without-ncurses \
                     --disable-static \
                     --disable-partx \
                     --disable-raw \
                     --disable-write \
                     --disable-mount \
                     --disable-fsck \
                     --disable-libmount \
                     --disable-mountpoint \
                     --with-audit=no \
                   "
    else:
        options += "\
                     --bindir=/bin \
                     --sbindir=/sbin \
                     --enable-partx \
                     --disable-raw \
                     --enable-write \
                     --enable-tunelp \
                     --enable-runuser \
                     --without-audit \
                     --with-udev \
                     --enable-mountpoint \
                     --without-utempter \
                   "
    shelltools.system("NOCONFIGURE=1 ./autogen.sh")
    #autotools.autoreconf("-fi")
    autotools.configure(options)
    pisitools.dosed("libtool", "( -shared )", r" -Wl,--as-needed\1")

    # Extra fedora switches:
    # --enable-login-utils will enable some utilities we ship in shadow
    # --enable-kill will enable the kill utility we ship in coreutils

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    #pisitools.doman("sys-utils/klogconsole.man")
    pisitools.remove("/usr/share/man/man1/kill.1")
    #pisitools.remove("/usr/share/bash-completion/completions/rfkill")

    if get.buildTYPE() == "emul32": return

    #pisitools.removeDir("/usr/lib32/pkgconfig")

    pisitools.dodoc("ABOUT-NLS", "AUTHORS", "ChangeLog", "COPYING", "README*")
    pisitools.insinto("/%s/%s" % (get.docDIR(), get.srcNAME()), "Documentation")
