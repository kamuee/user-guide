
.. icon 用ラベルの読み込み
.. include:: def_icon.txt

基本コンフィギュレーション
============================

kamuee で高速な経路検索とパケット転送を利用するには、ネットワークインターフェースをkamuee 用に割り当て、kamuee から各種パラメータを設定する必要があります。
それにより、iproute2 や FRRなどのサードパーティルーティングソフトウエアからでも高速な経路検索とパケット転送を利用できます。

起動時設定ファイル: kamuee.conf
------------------------------------------------------

kamuee の設定は **/etc/kamuee/kamuee.conf** に保存されています。
起動時にはこの設定ファイルを読み込んで、自動的にルーティングの転送設定を
DPDKに反映します。付属のサンプル設定（初期設定）を下記に示します。

::

    set thread 0 os
    set thread 1 os

    set thread 2 lthread_scheduler
    set thread 3 snmp_manager

    set thread 4 forwarder port 0 rx-queue 0
    set thread 5 forwarder port 0 rx-queue 1

    set thread 6 forwarder port 1 rx-queue 0
    set thread 7 forwarder port 1 rx-queue 1

    set thread 8 forwarder port 2 rx-queue 0
    set thread 9 forwarder port 2 rx-queue 1

    set thread 10 forwarder port 3 rx-queue 0
    set thread 11 forwarder port 3 rx-queue 1

    set thread 28 rib_manager
    set thread 29 tap_manager

    set thread 30 forwarder port 4 rx-queue 0
    set thread 31 forwarder port 4 rx-queue 1

    set thread 32 forwarder port 5 rx-queue 0
    set thread 33 forwarder port 5 rx-queue 1

    set thread 34 forwarder port 6 rx-queue 0
    set thread 35 forwarder port 6 rx-queue 1

    set thread 36 forwarder port 7 rx-queue 0
    set thread 37 forwarder port 7 rx-queue 1

..

kamuee.conf に記載されるのは、kamuee CLI で実行可能な
コマンドに過ぎません。各コマンドは、以降の節で個別に説明します。

CPU coremap および スレッドの NIC port への割り当て
------------------------------------------------------

CPU coremap およびスレッドのNIC port への割り当ては、
基本的に設定ファイル kamuee.conf で行われます。
動的な coremap やスレッドの NIC port への割り当て変更は、
未だサポートされていません。
以降のコマンドは、kamuee.conf に記述し、kamuee 起動時の初期に
実行されるようにしてください。

ここでは、前節の kamuee.conf を例に取り、各コマンドを順に
説明します。

set thread X os コマンドは、オペレーティングシステム（OS）用に
core X を確保し、何も動作させないためのダミーコマンドです。
オペレーティングシステム用には、2〜4コアほど残しておけば良いでしょう。

kamuee では、native thread で動作させる必要のある thread が
いくつかあります。それらは、lthread_scheduler、snmp_manager、
rib_manager、tap_manager です。lthread_scheduler は、
バーチャルターミナル（VTY）や netlink 受信 thread を含む、
多数の重要 thread を仮想的に動作する thread です。
lthread_scheduler によってこれらの重要 thread が lthread として
実行されます。snmp_manager は、Net-SNMP への送受信を処理する
thread であり、SNMP を動作させるのでなければ、設定する必要は
ありません。rib_manager および tap_manager はそれぞれ、
routing socket および TUN/TAP I/F とのデータ送受信を処理する thread であり、
パフォーマンスバランスのために、native thread として実行する必要が
あります。これらの4つの thread は、NUMA に関係なく設定することができます。

set thread X forwarder port Y rx-queue Z は、
port Y 用の forwarder を core X に設定するコマンドです。
port には任意の数の forwarder を設定でき、これらの thread が
port 向けトラフィックの受信を並列分散処理します。
port Y 用の複数 forwarder は異なる rx-queue に設定する必要があります。
rx-queue 番号 Z は、0 から連続で順番に設定する必要があります。
コア番号が昇順で飛ぶ（間隔を開ける）ことは問題ありませんが、
コア番号が戻ることは許されていません（テストされておらず、問題が出ます）。
forwarder の設定は、NUMA に関係なく設定することもできますが、
NUMA 的に非効率な設定をすると、10%ほど性能が低下すると思われます。

thread の設定は、kamuee 管理コンソール（CLI）にて、
show thread info で確認することができます。
（CLIへのアクセス方法は、次節で説明します。）

    ::

        kamuee[vty0]> show thread info
        core[id]: v thread name        lcpu pcpu port  rxq funcp
        core[0]:  1 OS                    0    0    0    0 (nil)
        core[1]:  1 OS                    0   --   --   -- (nil)
        core[2]:  1 lthread_scheduler     0   --   --   -- 0x55555588fe8e
        core[3]:  1 snmp_manager          0   --   --   -- (nil)
        core[4]:  1 forwarder             0    0    0    0 0x5555556b429a
        core[5]:  1 forwarder             0    0    0    1 0x5555556b429a
        core[6]:  1 forwarder             0    0    0    2 0x5555556b429a
        core[7]:  1 forwarder             0    0    0    3 0x5555556b429a
        core[8]:  1 forwarder             0    0    0    4 0x5555556b429a
        core[9]:  1 forwarder             0    0    0    5 0x5555556b429a
        core[10]: 1 forwarder             0    0    0    6 0x5555556b429a
        core[11]: 1 forwarder             0    0    0    7 0x5555556b429a
        core[12]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[13]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[14]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[15]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[16]: 1 forwarder             0    0    2    0 0x5555556b429a
        core[17]: 1 forwarder             0    0    2    1 0x5555556b429a
        core[18]: 1 forwarder             0    0    2    2 0x5555556b429a
        core[19]: 1 forwarder             0    0    2    3 0x5555556b429a
        core[20]: 1 forwarder             0    0    2    4 0x5555556b429a
        core[21]: 1 forwarder             0    0    2    5 0x5555556b429a
        core[22]: 1 forwarder             0    0    2    6 0x5555556b429a
        core[23]: 1 forwarder             0    0    2    7 0x5555556b429a
        core[24]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[25]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[26]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[27]: 1 forwarder             0   --   --   -- 0x5555556b429a
        core[28]: 1 rib_manager           1   --   --   -- 0x5555556385d4
        core[29]: 1 tap_manager           1   --   --   -- 0x5555557d33c1
        core[30]: 1 forwarder             1    1    4    0 0x5555556b429a
        core[31]: 1 forwarder             1    1    4    1 0x5555556b429a
        core[32]: 1 forwarder             1    1    4    2 0x5555556b429a
        core[33]: 1 forwarder             1    1    4    3 0x5555556b429a

        （略）

    ..

CPUスレッドの統計情報を確認したい場合は、下記のコマンドで確認できます。

    ::

        kamuee-vty[0] >  show thread statistics pps

    ..


kamuee 設定ファイル（kamuee.conf）は、kamuee CLI のコマンドの羅列に
過ぎません。後述の、vlan 関連や jumbo-frame、mtu 関連のコマンドも、
設定ファイルに記述しておくことによって、起動時に自動で
設定されるようになります。

 |ic02| |la02|

    mirror コマンド（set port X mirror X）だけは、kamuee 設定ファイルでは
    有効化になりません。起動してから kamuee CLI で実行してください。


管理コンソール / コマンドラインインターフェイス (CLI)
------------------------------------------------------

CLI へのアクセス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

kamuee ではコマンドラインインターフェイスでデーモンを操作します。
コマンドラインインターフェイスは、kamuee デーモンをフォラグラウンドで
実行した際のコンソール（標準入出力端末（stdin/stdout））に現れるほか、
telnet で接続することもできます。

コマンドを実行する場合は、実行デーモン（kamuee デーモン）にログインして
コマンドを入力します。kamuee デーモンへのログイン方法は、コンソール
または ssh コマンドなどでアプライアンスにログインした後、
下記のように **telnet** コマンドを実行します。

    ::

        kamuee@kamuee:~$ telnet localhost 9077

    ..


ログインすると次のようにコマンドプロンプトが表示されます。

    ::

        kamuee-vty[0]>

    ..


CLIからのログアウトは、 **logout**, **exit**, **quit**, いずれかの
コマンドで行えます。次は **logout** を入力した場合の出力例です。

    ::

        kamuee[vty0]> logout
        vty exit !
        Connection closed by foreign host.
        kamuee@kamuee:~$

    ..


|ic01| |la01|

    kamuee には、ログイン時のパスワード入力はありません。
    また、特権モードやコンフィグモードなどもありません。ご注意ください。


コマンドヘルプ、コマンド候補の表示、コマンドの補完
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コマンド入力で次に続くパラメータがわからない場合、 
<?> キーを入力すると、パラメータの候補が表示されます。


    ::

        kamuee[vty0]> show port

    ..

と表示されている状態で ? キーを入力すると、


    ::

        kamuee[vty0]> show port
          <cr>             Port information
          <0-127>          Specify the port ID.
          all              Show all ports.
          statistics       Port statistics
        kamuee[vty0]> show port

    ..

と、**show port** に続くパラメータ候補が表示されます。


kamuee では、コマンドが一意に定まる場合、TABキーにより補完できます。


    ::

        kamuee[vty0]> show th

    ..

と入力した状態で TABキーを押すと補完され

    ::

        kamuee[vty0]> show thread

    ..

と入力された状態になります。




物理インターフェイスの確認と設定
------------------------------------------------------

kamuee 側で物理インターフェース情報を確認する場合は、下記のコマンドを実行します。

    ::

        kamuee[vty0]> show port
        port        id c if tap mac-addr          drvr   speed supported
        port-3b-0-0  0 0  4 273 50:6B:4B:08:6C:56 mlx5  100000 100G/50G/40G/25G/10G/1G
        port-3b-0-1  1 0  5 274 50:6B:4B:08:6C:57 mlx5       0 40G/10G/1G
        port-5e-0-0  2 0  6 275 50:6B:4B:B6:C6:F8 mlx5  100000 100G/50G/40G/25G/10G/1G
        port-5e-0-1  3 0  7 276 50:6B:4B:B6:C6:F9 mlx5       0 40G/10G/1G
        port-86-0-0  4 1  8 277 50:6B:4B:08:61:DE mlx5  100000 100G/50G/40G/25G/10G/1G
        port-86-0-1  5 1  9 278 50:6B:4B:08:61:DF mlx5       0 40G/10G/1G
        port-af-0-0  6 1 11 279 50:6B:4B:B6:C8:E0 mlx5  100000 100G/50G/40G/25G/10G/1G
        port-af-0-1  7 1 12 280 50:6B:4B:B6:C8:E1 mlx5       0 40G/10G/1G

    ..


特定の物理ポートの詳細情報を表示する場合は、**show port** コマンドで表示する物理ポートのIDを指定します。


    ::

        kamuee-vty[0]> show port 0
        port0:
            new name: kni-3b-0-0
            valid: 1
            vrf: 1 (router)
            flags: <RUNNING|OURS-TAP>
            kni ifindex: -1
            tap ifindex: 273
            tap name: port-3b-0-0
            tap sockfd: 288
            promiscuous:       1    allmulticast:      1
            nrxq:              8    ntxq:             56
            hwaddr: 50:6B:4B:08:6C:56
            device info:
                pci_dev_name:   0000:3b:00.0
                driver_name:    net_mlx5
                if_index:            4
                min_rx_bufsize:     32    max_rx_pktlen:   65536
                max_rx_queues:   65535    max_tx_queues:   65535
                nb_rx_queues:        8    nb_tx_queues:       56
                reta_size:           8    hash_key_size:      40
                speed_capa: 100G/50G/40G/25G/10G/1G
                rx_offload_capa: <VLAN-STRIP|IPV4-CKSUM|UDP-CKSUM|TCP-CKSUM>
                tx_offload_capa: <VLAN-INSERT|IPV4-CKSUM|UDP-CKSUM|TCP-CKSUM|TCP-TSO|OUTER-IPV4-CKSUM|VXLAN-TNL-TSO|GRE-TNL-TSO>
                default_txconf:
                    tx_free_thresh: 0
            ifaddrs[ipv4]:
                192.85.2.1/24
            ifaddrs[ipv6]:
                ::/0
                2001:0:1::1/64
                fe80::526b:4bff:fe08:6c56/64
            mirror port:      none
        （略）

    ..

物理デバイス・ポートの動的設定例
-----------------------------------

kamuee では、物理デバイスは dpdk-devbind.py 等であらかじめ設定しておき、
コア・スレッドは kamuee.conf で起動時初期に設定するのが、
現状ではもっとも検証された、安全・基本的なやり方です。
この節では、それほど検証されていないが、ベータ機能として実装されている、
物理デバイス・ポートの動的設定方法を説明します。

一般的に Kamueeポートを起動してフレーム転送を開始する場合には、以下の
4つの手順が必要となります。

1. デバイスを DPDK PMDにbindする
2. デバイスに関連してポートを生成する
3. ポートのコンフィグレーションコマンドを投入する
4. ポートを実際に起動する

一方、フレーム転送を終了し、Kamueeポートを停止する場合には、以下の 3つ
の手順が必要となります。

5. ポートを実際に停止する
6. ポートを削除する
7. デバイスを DPDK PMDからunbindする

本件では、必須の新規追加 CLI として、上記手順のうち(2), (4), (5), (6)に
ついての機能を提供しています。また、オプションの新規追加 CLI として、手
順 (1), (7) についての機能を提供しています。手順 (2) については、従来の
Kemuee ポート関連 CLIコマンドをそのまま利用できるものとします。


例1: 完全初期状態からのポート起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

物理デバイスが一切DPDK PMDに bind されておらず、kamuee.conf も存在しな
い状態から kamuee サービスを起動し、ポート利用可能とする場合のCLI設定例。

    ::

        kamuee> device bind 0000:05:00.0 igb_uio
        kamuee> port attach 0000:05:00.0
        kamuee> set thread 4 forwarder port 0 rx-queue 0
        kamuee> set thread 5 forwarder port 0 rx-queue 1
        kamuee> port start 0

    ..

例2: kamuee.conf を引き継いだポート起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

物理デバイスが一切DPDK PMDに bind されておらず、kamuee.conf に
forwarder 設定だけは記述されている状態から kamuee サービスを起動し、ポー
ト利用可能とする場合のCLI設定例。

    ::

        $ cat /etc/kamuee/kamuee.conf
        set thread 4 forwarder port 0 rx-queue 0
        set thread 5 forwarder port 0 rx-queue 1

        kamuee> device bind 0000:05:00.0 igb_uio
        kamuee> port attach 0000:05:00.0
        kamuee> port start 0

    ..

例3: kamuee.conf を無視してのポート起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

物理デバイスが一切DPDK PMDに bind されておらず、kamuee.conf に
forwarder 設定だけは記述されている状態から kamuee サービスを起動し、完
全に新規ポートとして利用可能とする場合の例。

    ::

        $ cat /etc/kamuee/kamuee.conf
        set thread 4 forwarder port 0 rx-queue 0
        set thread 5 forwarder port 0 rx-queue 1

        kamuee> device bind 0000:05:00.0 igb_uio
        kamuee> port attach 0000:05:00.0 default
        kamuee> set thread 8 forwarder port 0 rx-queue 0
        kamuee> set thread 9 forwarder port 0 rx-queue 1
        kamuee> port start 0

    ..

例4: ポート停止
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

kamuee.conf の設定、もしくは port attach/port start コマンドによって起
動中のポートを停止させ、物理デバイスのDPDK PMDを unbind する場合の例。

    ::

        kamuee> port stop 0
        kamuee> port detach 0
        kamuee> device unbind 0000:05:00.0

    ..

例5: ポート強制停止
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

kamuee.conf の設定、もしくは port attach/port start コマンドによって起
動中のポートが利用中であって停止させる場合の例。

    ::

        kamuee> port detach 0 force
        kamuee> device unbind 0000:05:00.0

    ..

例6: 物理デバイス一覧表示
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kamueeから利用可能なすべての物理デバイスの一覧を表示する場合の例。以下
の例は、物理デバイス 0000:05:00.0 が Kamuee の port 0 として利用され
る場合の表示内容です。

    ::

        kamuee> show devices
        id device       name                                          driver   unused  
         - 0000:03:00.0 Ethernet Controller 10-Gigabit X540-AT2       ixgbe    igb_uio 
         - 0000:03:00.1 Ethernet Controller 10-Gigabit X540-AT2       ixgbe    igb_uio 
         0 0000:05:00.0 Ethernet Controller 10-Gigabit X540-AT2       igb_uio  ixgbe
         - 0000:05:00.1 Ethernet Controller 10-Gigabit X540-AT2       ixgbe    igb_uio 
         - 0000:08:00.0 I350 Gigabit Network Connection               igb      igb_uio 
         - 0000:08:00.1 I350 Gigabit Network Connection               igb      igb_uio

    ..


JumboフレームとMTUの設定
------------------------------------------------------


　Jumboフレームをポートに設定するには、次のように **set port** コマンドにより MTUの値を **9140** で設定します。

    ::

        kamuee-vty[0] >   set port 0 jumbo-frame
        kamuee-vty[0] >   set port 0 mtu 9140
        kamuee-vty[0] >   set port 2 jumbo-frame
        kamuee-vty[0] >   set port 2 mtu 9140
        kamuee-vty[0] >   set port 4 jumbo-frame
        kamuee-vty[0] >   set port 4 mtu 9140

    ..


　Jumboフレームを vport （VLANインターフェース）に設定する場合は、MTUの値を **9118** で設定します。
次の例ではvport 0 と vport 1 の MTU を 9118 に設定しています。


    ::

        kamuee-vty[0] >   set vport 0 mtu 9118
        kamuee-vty[0] >   set vport 1 mtu 9118

    ..


設定したMTU値は **ip link** コマンドでベースOS側でも確認できます。

    ::

		kamuee@kamuee:~$ ip link
		1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
		    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
		3: eno1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether 70:e2:84:09:f1:0c brd ff:ff:ff:ff:ff:ff
		4: eno2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
		    link/ether 70:e2:84:09:f1:0d brd ff:ff:ff:ff:ff:ff
		6: port-2-0-0: <BROADCAST,MULTICAST> mtu 9140 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether a0:36:9f:ba:3b:9c brd ff:ff:ff:ff:ff:ff
		7: port-2-0-1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether a0:36:9f:ba:3b:9d brd ff:ff:ff:ff:ff:ff
		8: vlan0040: <BROADCAST,MULTICAST> mtu 9118 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether b2:cd:8a:d8:c3:ae brd ff:ff:ff:ff:ff:ff
		9: vlan0041: <BROADCAST,MULTICAST> mtu 9118 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether 4a:fa:2f:f8:fb:3e brd ff:ff:ff:ff:ff:ff
		kamuee@kamuee:~$

    ..


論理インターフェイスの確認と設定
-----------------------------------
論理インターフェイス（vport）を確認するには **show vport** コマンドを
実行します。


    ::

		kamuee[vty0]> show vport
		vport       id tap mac-addr          drvr  phy-name    phy vlan
		vlan0040     0   8 B2:CD:8A:D8:C3:AE vlan  port-2-0-0    0   40
		kamuee[vty0]>

    ..


特定の vport の詳細を確認するには **show vport** コマンドで vport ID を指定します。


    ::

		kamuee[vty0]> show vport 0
		vport0:
		    name: vlan0040
		    new name: vlan0040
		    vrf: 0 (vrf0)
		    flags: <OURS-TAP|MACADDR-RANDOM>
		    kni ifindex: -1
		    tap ifindex: 8
		    tap sockfd: 120
		    tx_ol_flags: <>
		    hwaddr: B2:CD:8A:D8:C3:AE
		    vlan-id:            40
		    physical port:       0
		    ifaddrs[ipv4]:
		    ifaddrs[ipv6]:
		    mirror port:      none
		    tapmirror-rx:       no
		    tapmirror-tx:       no
		kamuee[vty0]>

    ..


全ての vport の詳細を確認するには **show vport all** コマンドを実行します。

    ::


		kamuee[vty0]> show vport all
		vport0:
		    name: vlan0040
		    new name: vlan0040
		    vrf: 0 (vrf0)
		    flags: <OURS-TAP|MACADDR-RANDOM>
		    kni ifindex: -1
		    tap ifindex: 8
		    tap sockfd: 120
		    tx_ol_flags: <>
		    hwaddr: B2:CD:8A:D8:C3:AE
		    vlan-id:            40
		    physical port:       0
		    ifaddrs[ipv4]:
		    ifaddrs[ipv6]:
		    mirror port:      none
		    tapmirror-rx:       no
		    tapmirror-tx:       no
		vport1:
		    name: vlan0041
		    new name: vlan0041
		    vrf: 0 (vrf0)
		    flags: <OURS-TAP|MACADDR-RANDOM>
		    kni ifindex: -1
		    tap ifindex: 9
		    tap sockfd: 121
		    tx_ol_flags: <>
		    hwaddr: 4A:FA:2F:F8:FB:3E
		    vlan-id:            41
		    physical port:       0
		    ifaddrs[ipv4]:
		    ifaddrs[ipv6]:
		    mirror port:      none
		    tapmirror-rx:       no
		    tapmirror-tx:       no
		kamuee[vty0]>


    ..


VLAN インターフェースの設定
-----------------------------------

kamueeではパケットフォワーディングにDPDKを利用しているため、VLANの設定も Linux 標準の設定ではなく DPDK 側の設定を行う必要があります。
kamueeではDPDKのVLAN設定を行うためのインターフェイスを提供しています。ここでは、この設定について解説します。

　kamuee 上では VLAN インターフェースは **vport** として扱われます。
vport へのVLAN 番号割り当ては **set vport** コマンドで設定します。
次の例では、ポート **0** 番に対して、VLAN番号 **40** を認識する vport ID **0** 番の vport を作成しています。


    ::

        kamuee[vty0]> set vport 0 physical-port 0 vlan 40

    ..



設定した vport は **ip link** コマンドでベースOS側でも VLAN インターフェースとして確認できます。
次の出力例では **vlan0040** 、 **vlan0041** というインターフェース名で表示されています。

    ::

		kamuee@kamuee:~$ ip link
		1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
		    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
		3: eno1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether 70:e2:84:09:f1:0c brd ff:ff:ff:ff:ff:ff
		4: eno2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
		    link/ether 70:e2:84:09:f1:0d brd ff:ff:ff:ff:ff:ff
		6: port-2-0-0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether a0:36:9f:ba:3b:9c brd ff:ff:ff:ff:ff:ff
		7: port-2-0-1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether a0:36:9f:ba:3b:9d brd ff:ff:ff:ff:ff:ff
		8: vlan0040: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether b2:cd:8a:d8:c3:ae brd ff:ff:ff:ff:ff:ff
		9: vlan0041: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		    link/ether 4a:fa:2f:f8:fb:3e brd ff:ff:ff:ff:ff:ff
		kamuee@kamuee:~$

    ..

OS 側に公開された VLAN インターフェイスは、iproute2 コマンドや
FRR の論理インターフェイスとして利用可能です。



IPアドレスの設定と確認
----------------------------------------


IP経路の設定と変更
----------------------------------------

kamuee 側で DPDK の RIB, FIB に直接経路設定を書き込むことで、
ベースOSのカーネルやルーティングデーモンには届かない形で、
経路設定を強制的に変更できます。
緊急避難的なブラックホールルーティングの設定に利用できます。

経路変更を設定する場合は、**ip route** コマンドを実行します。
下記は、10.0.0.0/24 の経路を /dev/null に設定するブラックホール
ルーティングの例です。

    ::

        kamuee-vty[0] >  ipv4 route 10.0.0.0/24 ???? （要確認）

    ..


経路変更を解除する場合は、下記のコマンドを実行します。

    ::

        kamuee-vty[0] >  no ipv4 route 10.0.0.0/24 ???? （要確認）

    ..

ECMP (Equal Cost Multipath) を確認したい場合は、次のコマンドで表示できます。


    ::

        kamuee-vty[0] >  show ipv4 route multipath

    ..


IPv6 の場合は次のようになります。

    ::

        kamuee-vty[0] >  show ipv6 route multipath

    ..


マルチキャストの経路を確認したい場合は、次のコマンドで表示できます。


    ::

        kamuee-vty[0] >  show ipv4 route type multicast

    ..


    ::

        kamuee-vty[0] >  show ipv6 route type multicast

    ..


　IPアドレス設定と経路設定は、基本的には **ip** コマンドやサードパーティの経路制御ソフトウエアから行います。基本的には kamuee が自動的にOSに設定された経路情報を読み込み kamuee 側の経路テーブルにも利用します。すなわち、ここまでの設定が完了していれば、ip route や quagga FRR 等の経路制御ソフトを普通のLinuxルータ同様に設定するだけで、kamueeの高速ルーティングは動作します。
　本節では例としてiproute2を利用した方法と、kamueeに入力された経路の確認方法を解説します。

.. スタティックルートの設定例（iproute2）

　はじめに **ip** コマンドを使ったスタティックルートに対する kamuee の状態を説明します。
まず、ベースOS側で **ip** コマンドでインターフェースの IPv4 アドレスと スタティックルートを設定します。

    ::

        kamuee@kamuee:~# ip addr add 192.168.10.1/24 dev port-2-0-0
        kamuee@kamuee:~# ip route add 172.16.20.0/24 via 192.168.10.1

    ..


　上記のコマンドをUbuntu上で実行すると同時に kamuee 側でも設定された経路が確認できます。 **show ipv4 route** コマンドで設定した経路情報を確認できます。このように経路情報が確認できていればkamuee占有として割り当てたポートに入力されたパケットは、経路表に従い転送されます。

    ::

        kamuee[vty0]> show ipv4 route
        vrf[0]: vrf0
        Destination        Nexthop         MAC-address       I/F         <Flags>
        127.0.0.0/8        0.0.0.0         00:00:00:00:00:00 port-2-0-0  <OURS>
        127.0.0.0/32       0.0.0.0         00:00:00:00:00:00 port-2-0-0  <BLACKHOLE>
        127.0.0.1/32       0.0.0.0         00:00:00:00:00:00 port-2-0-0  <OURS>
        127.255.255.255/32 0.0.0.0         00:00:00:00:00:00 port-2-0-0  <BLACKHOLE>
        172.16.20.0/24     192.168.10.1    00:00:00:00:00:00 port-2-0-0  <>
        192.168.1.0/24     0.0.0.0         00:00:00:00:00:00 port-2-0-1  <CONNECTED>
        192.168.1.0/32     0.0.0.0         00:00:00:00:00:00 port-2-0-1  <BLACKHOLE>
        192.168.1.228/32   0.0.0.0         00:00:00:00:00:00 port-2-0-1  <OURS>
        192.168.1.255/32   0.0.0.0         00:00:00:00:00:00 port-2-0-1  <BLACKHOLE>
        192.168.10.0/24    0.0.0.0         00:00:00:00:00:00 port-2-0-0  <CONNECTED>
        192.168.10.0/32    0.0.0.0         00:00:00:00:00:00 port-2-0-0  <BLACKHOLE>
        192.168.10.1/32    0.0.0.0         00:00:00:00:00:00 port-2-0-0  <OURS>
        192.168.10.2/32    192.168.10.2    80:2A:A8:9C:AE:99 port-2-0-0  <>
        192.168.10.255/32  0.0.0.0         00:00:00:00:00:00 port-2-0-0  <BLACKHOLE>
        vrf[0]: vrf0: routes: 19 from 19
        kamuee[vty0]>

    ..


　複数のIPv4 経路を設定している場合で、詳細情報が必要ない場合は、 **show ipv4 route summary** コマンドでサマリを表示できます。


    ::


		kamuee[vty0]> show ipv4 route summary
		vrf[0]: vrf0
		vrf[0]: vrf0: afi: ipv4: routes: 19 from 19
		    multipath: 0 routes
		    route_type: CONNECTED: 2 routes
		    route_type: REJECT: 0 routes
		    route_type: BLACKHOLE: 6 routes
		    route_type: DISABLE: 0 routes
		    route_type: OURS: 4 routes
		    route_type: MPATH: 0 routes
		    route_type: MCAST: 0 routes
		    route_type: NORMAL: 7 routes
		    route to port[0]: port-2-0-0: 10 routes
		    route to port[1]: port-2-0-1: 9 routes
		kamuee[vty0]>

    ..


　IPv6 のスタティックルートの設定もIPv4の場合と同様に行えます。


    ::

        kamuee@kamuee:~$ sudo ip addr add 2001:db8:0::1/64 dev port-2-0-0
        kamuee@kamuee:~$ sudo ip route add 2001:db8:20::/64 via 2001:db8:10::2 dev port-2-0-0

    ..


　上記のコマンドを実行後、kamuee 側では **show ipv6 route** コマンドで設定した経路情報を確認します。

    ::


		kamuee[vty0]> show ipv6 route
		vrf[0]: vrf0
		Destination                    Nexthop           I/F         <Flags>
		::1/128                        ::                port-2-0-0  <OURS>
		2001:db8:10::/64               ::                port-2-0-0  <CONNECTED>
		2001:db8:10::1/128             ::                port-2-0-0  <OURS>
		2001:db8:20::/64               2001:db8:10::2    port-2-0-0  <>
		fe80::2:56dd:3875:d806/128     18:F1:D8:62:46:22 port-2-0-1  <>
		fe80::80b:dbff:fe83:c12b/128   0A:0B:DB:83:C1:2B port-2-0-1  <>
		fe80::822a:a8ff:fe9c:ae99/128  80:2A:A8:9C:AE:99 port-2-0-0  <>
		fe80::822a:a8ff:fe9e:4e61/128  80:2A:A8:9E:4E:61 port-2-0-1  <>
		fe80::a236:9fff:feba:3b9c/128  00:00:00:00:00:00 port-2-0-0  <OURS>
		fe80::a236:9fff:feba:3b9d/128  00:00:00:00:00:00 port-2-0-1  <OURS>
		fe80::f452:53ff:fee3:e348/128  00:00:00:00:00:00 vlan0040    <OURS|VPORT>
		fe80::f4cc:ba15:9c8a:2498/128  E4:70:B8:E2:36:E1 port-2-0-1  <>
		fe80::f830:85ff:fe50:1b85/128  00:00:00:00:00:00 vlan0041    <OURS|VPORT>
		vrf[0]: vrf0: routes: 13 from 13
		kamuee[vty0]>

    ..


　IPv4の場合と同様に詳細情報が必要ない場合は、 **show ipv6 route summary** コマンドでサマリを表示できます。


    ::


		vrf[0]: vrf0: afi: ipv6: routes: 13 from 13
		    multipath: 0 routes
		    route_type: CONNECTED: 1 routes
		    route_type: REJECT: 0 routes
		    route_type: BLACKHOLE: 0 routes
		    route_type: DISABLE: 0 routes
		    route_type: OURS: 6 routes
		    route_type: MPATH: 0 routes
		    route_type: MCAST: 0 routes
		    route_type: NORMAL: 6 routes
		    route to port[0]: port-2-0-0: 6 routes
		    route to port[1]: port-2-0-1: 5 routes
		    route to vport[0]: vlan0040: 1 routes
		    route to vport[1]: vlan0041: 1 routes
		kamuee[vty0]>

    ..


　IPv4 と IPv6 の経路情報サマリを一括で表示したい場合は、 **show ip route summary** コマンドを実行します。


    ::


		kamuee[vty0]> show ip route summary
		vrf[0]: vrf0
		vrf[0]: vrf0: afi: ipv4: routes: 19 from 19
		    multipath: 0 routes
		    route_type: CONNECTED: 2 routes
		    route_type: REJECT: 0 routes
		    route_type: BLACKHOLE: 6 routes
		    route_type: DISABLE: 0 routes
		    route_type: OURS: 4 routes
		    route_type: MPATH: 0 routes
		    route_type: MCAST: 0 routes
		    route_type: NORMAL: 7 routes
		    route to port[0]: port-2-0-0: 10 routes
		    route to port[1]: port-2-0-1: 9 routes
		vrf[0]: vrf0: afi: ipv6: routes: 13 from 13
		    multipath: 0 routes
		    route_type: CONNECTED: 1 routes
		    route_type: REJECT: 0 routes
		    route_type: BLACKHOLE: 0 routes
		    route_type: DISABLE: 0 routes
		    route_type: OURS: 6 routes
		    route_type: MPATH: 0 routes
		    route_type: MCAST: 0 routes
		    route_type: NORMAL: 6 routes
		    route to port[0]: port-2-0-0: 6 routes
		    route to port[1]: port-2-0-1: 5 routes
		    route to vport[0]: vlan0040: 1 routes
		    route to vport[1]: vlan0041: 1 routes
		kamuee[vty0]>

    ..


|ic03| |la03|

    quagga や FRR などを用いて経路設定を行った場合も、同様の手順で経路情報を kamuee 側で確認できます。


VRF 設定
---------------------

kamuee は Linux のユーザスペースプログラムとして実装されているため、
管理・マネージメント用の IP アドレス・経路設定は、Linux のデフォルト
経路設定として実現すべきです。こうしておけば、kamuee や FRR の不具合から
アドレスや経路が消えて Linux ホストにアクセスできなくなることを防げます。

また、kamuee ルータのアドレス・経路設定と、Linux のアドレス・経路設定を
分離するために、kamuee には別の VRF を割り当てるべきです。こうすることで、
kamuee がクラッシュしたときに、ルータのトラフィックが Linux OS によって
Linux ホストのマネージメント用I/Fからホスト用デフォルト経路に誤って
転送してしまうことなどを防げます。

現状では、kamuee の機能未実装などの関係から、少々複雑な起動方法・
設定の順序を取らなくてはなりません。

Linuxホストで別のユーザプログラムの経路制御に利用するため、kamuee は
物理・論理ポートに一対一対応する TUN/TAP I/F を Linux ホストに作成します。
これが、port-X-X-X の I/F や、vlanXXXX の I/F です。これらの I/F は
kamuee 起動後に kamuee が作成するため、まずは kamuee を起動しなくては
なりません。kamuee の起動は、通常通りであり、特に追加設定は必要ありません。

    ::

        # systemctl start kamuee

    ..

その後、iproute2 で VRF m3dev の作成と、
上記 kamuee 配下の TUN/TAP I/F (e.g., port-X-X-X) の
VRF への紐付け（enslave）を実行します。
これが必要になる理由は、１）kamuee にこの機能が未実装であること、
２）FRR が interface の VRF の動的変更に未対応であること、
の二つです。FRR を起動するまえに iproute2 で VRF の設定を
実行しましょう。

    ::

        # sh -x ip_vrf.sh

    ..

    ::

        # cat ip_vrf.sh
        ip link add router type vrf table 100
        ip link set router up

        ip link set port-3b-0-0 vrf router
        ip link set port-5e-0-0 vrf router
        ip link set port-86-0-0 vrf router
        ip link set port-af-0-0 vrf router

    ..

その後、FRR を実行します。

    ::

        # systemctl start frr

    ..

FRR の設定では、
interface コマンド、ip route コマンド、bgp コマンドの
それぞれに、vrf を指定する必要があります。
ip forwarding は no に設定しておいた方が安全です。
Linuxホストはパケットを転送せず、kamuee のみにパケットを
転送させるという動作が実現できます。

    ::

        # cat /etc/frr/frr.conf
        frr version 7.2
             : （略）
        no ip forwarding
             : （略）
        !
        vrf router
         ip route 0.0.0.0/0 192.85.2.4
         exit-vrf
        !
             : （略）
        interface port-3b-0-0 vrf router
         ip address 192.85.2.1/24
             : （略）
        router bgp 65000 vrf router
         bgp router-id 10.1.1.1
         neighbor 192.85.1.4 remote-as 1
         neighbor 192.85.2.4 remote-as 2
             : （略）

    ..

FRR では、show bgp vrf router summary など、
vrf を指定して情報を確認できます。

Kamuee では、show ipv4 route で、全 vrf の経路が表示されます。

iproute2 では、ip route show vrf router など、
vrf を指定する必要があります。



