
Setup FRRouting
===============

1. install required packages and frr

.. code-block:: text

  wget https://github.com/FRRouting/frr/releases/download/frr-6.0.2/frr_6.0.2-0.ubuntu18.04.1_amd64.deb
  apt install -y ./frr_6.0.2-0.ubuntu18.04.1_amd64.deb
  systemctl start frr

2. check interface and FRR's version

.. code-block:: text

  vtysh -c 'show version'
  FRRouting 6.0 (96c021364c0b).
  Copyright 1996-2005 Kunihiro Ishiguro, et al.
  configured with:
       '--build=x86_64-linux-gnu' '--prefix=/usr' \
       '--includedir=${prefix}/include' '--mandir=${prefix}/share/man' \
       '--infodir=${prefix}/share/info' '--sysconfdir=/etc' \
       '--localstatedir=/var' '--disable-silent-rules' \
       '--libexecdir=${prefix}/lib/frr' '--disable-maintainer-mode' \
       '--disable-dependency-tracking' \
       '--enable-exampledir=/usr/share/doc/frr/examples/' \
       '--localstatedir=/var/run/frr' '--sbindir=/usr/lib/frr' \
       '--sysconfdir=/etc/frr' '--disable-snmp' '--enable-ospfapi=yes' \
       '--enable-multipath=256' '--enable-ldpd' '--enable-fpm' \
       '--enable-user=frr' '--enable-group=frr' '--enable-vty-group=frrvty' \
       '--enable-configfile-mask=0640' '--enable-logfile-mask=0640' \
       '--enable-werror' '--with-libpam' '--enable-systemd=yes' \
       '--enable-poll=yes' '--enable-cumulus=no' '--enable-pimd' \
       '--enable-dependency-tracking' '--enable-bgp-vnc=yes' \
       '--disable-rpki' '--enable-bfdd' \
       'CFLAGS=-g -O2 -fdebug-prefix-map=/home/ci/cibuild.6/debwork/frr-6.0=. \
       -fstack-protector-strong -Wformat -Werror=format-security' \
       'CPPFLAGS=-Wdate-time -D_FORTIFY_SOURCE=2' 'CXXFLAGS=-g -O2 \
       -fdebug-prefix-map=/home/ci/cibuild.6/debwork/frr-6.0=. \
       -fstack-protector-strong -Wformat -Werror=format-security' \
       'FCFLAGS=-g -O2 -fdebug-prefix-map=/home/ci/cibuild.6/debwork/frr-6.0=. \
       -fstack-protector-strong' 'FFLAGS=-g -O2 \
       -fdebug-prefix-map=/home/ci/cibuild.6/debwork/frr-6.0=. \
       -fstack-protector-strong' 'GCJFLAGS=-g -O2 \
       -fdebug-prefix-map=/home/ci/cibuild.6/debwork/frr-6.0=. \
       -fstack-protector-strong' 'LDFLAGS=-Wl,-Bsymbolic-functions \
       -Wl,-z,relro -Wl,-z,now' 'OBJCFLAGS=-g -O2 \
       -fdebug-prefix-map=/home/ci/cibuild.6/debwork/frr-6.0=. \
       -fstack-protector-strong -Wformat -Werror=format-security' \
       'OBJCXXFLAGS=-g -O2 -fdebug-prefix-map=/home/ci/cibuild.6/debwork/frr-6.0=. \
       -fstack-protector-strong -Wformat -Werror=format-security' \
       'build_alias=x86_64-linux-gnu'

