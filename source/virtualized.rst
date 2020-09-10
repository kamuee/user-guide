仮想環境での利用
=======================

virtio-net での動作を確認しています。

virtio-net のドライバの仕様から、
memory leak が起きて長期安定運用できない不具合が確認されています。
その場合には、以下のように、rxdesc の値を 256 固定にすると、
memory leak が解消されます。

    ::

        set port 0 nrxdesc 256
        set port 0 ntxdesc 256
        set port 1 nrxdesc 256
        set port 1 ntxdesc 256

    ..

- 物理NIC: intel 82599
- VM上。VMとはOVS-DPDK経由（vhost-user）
- ethtool -i: driver:virtio_net


