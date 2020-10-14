
.. icon 用ラベルの読み込み
.. include:: def_icon.txt

インストール
=======================


ダウンロード
-----------------------

.. code-block:: none

    % wget http://www.kamuee.net/download/kamuee_0.6.3t_amd64.deb

パッケージの種類には、以下があります。

    * kamuee_0.6.3t_amd64.deb: amd64/x86_64 アーキテクチャ用 Intel NIC 用 debian パッケージ
    * kamuee_0.6.3tm_amd64.deb: amd64/x86_64 アーキテクチャ用 Intel/Mellanox NIC 用 debian パッケージ
    * kamuee_0.6.3t_arm64.deb: arm64(armv8a) アーキテクチャ用 Intel NIC 用 debian パッケージ

インストール
-----------------------

.. code-block:: none

    # apt install ./kamuee_0.6.3t_amd64.deb

インストールの確認
-----------------------

.. code-block:: none

    # apt show kamuee
    Package: kamuee
    Version: 0.6.3t
    Status: install ok installed
    Priority: optional
    Section: non-free/net
    Maintainer: Yasuhiro Ohara <yasu@nttv6.jp>
    Installed-Size: unknown
    Depends: libc6 (>= 2.27), liburcu-dev (>= 0.10.1), pkg-config (>= 0.29.1), libjson-c-dev (>= 0.12.1), libmnl-dev (>= 1.0.4), libnuma-dev (>= 2.0.11)
    Download-Size: unknown
    APT-Manual-Installed: yes
    APT-Sources: /var/lib/dpkg/status
    Description: Kamuee software router

kamuee の停止
-----------------------

.. code-block:: none

    # systemctl stop kamuee

アップグレード
-----------------------

.. code-block:: none

    # apt remove kamuee
    # apt install ./kamuee_0.6.3t_amd64.deb

kamuee の起動
-----------------------

.. code-block:: none

    # systemctl start kamuee

kamuee の起動の確認
-----------------------

.. code-block:: none

    # systemctl status kamuee

.. code-block:: none

    # ps ax | grep kamuee

.. code-block:: none

    # tail -f /var/log/syslog

.. code-block:: none

    # telnet localhost 9077

（オプション）FRRouting のインストール
----------------------------------------------

.. code-block:: text

  wget https://github.com/FRRouting/frr/releases/download/frr-6.0.2/frr_6.0.2-0.ubuntu18.04.1_amd64.deb
  apt install -y ./frr_6.0.2-0.ubuntu18.04.1_amd64.deb
  systemctl start frr


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

