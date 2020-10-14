
.. icon 用ラベルの読み込み
.. include:: def_icon.txt

前提条件
=======================

テスト済みハードウェア一覧
-----------------------------------------------------

Tested NICs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Intel Ethernet Converged Network Adapter X550-T2 (10G-T)
* Intel Ethernet Converged Network Adapter X540-T2 (10G-T)
* Intel Ethernet Converged Network Adapter X710 DA-2/DA-4 (10G)
* Intel Ethernet Converged Network Adapter XL710 (40G)
* Mellanox ConnectX-5 VPI (MCX556A-ECAT) (100G)

Tested Server Hardware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Supermicro SYS-7049GP-TRT (4U)
    + Motherboard: X11DPG-QT
    + CPU: Intel Xeon Platinum 8180 (2.5GHz, 28 cores/56 threads) x 2
    + Mem: 192GB (DDR4-2666 16GB x 12)
    + NIC: Intel X710 DA-4, Intel X550/540-T2, Mellanox ConnectX-5 VPI

* Supermicro SYS-2028R-TXR (2U)
    + Motherboard: X11DRX
    + CPU: Intel Xeon E5-2699A v4 (22 cores/44 threads) x 2
    + Mem: 128GB (DDR4-2400 8GB x 16)
    + NIC: Intel XL710, Intel X710 DA-4

..
    * Supermicro SC836BA-R920B (3U)
    + Motherboard: X10DAX
    + CPU: Intel Xeon E5-2687W v3 x 2
    + Mem: 256GB (DDR4-2133 16GB x 16)

* Fujitsu Primergy RX200 S8 (1U)
    + CPU: Intel Xeon E5-2620 v2 (6 cores/12 threads) x 2
    + Mem: 32GB
* Fujitsu Primergy RX2530 M2 (1U)
    + CPU: Intel Xeon E5-2683 v4 (16 cores/32 threads) x 2
    + Mem: 256GB

* LANNER NCA-5710C (1U)
    + CPU: Intel Xeon Scalable Processor x 2
    + NIC: NC2S-MXH01 (Mellanox ConnectX-4)

* Ampere Computing eMAG 8180 server (2U)
    + CPU: eMAG 8180 ARMv8 CPU (32 cores) x 1
    + Mem: 64GB
    + NIC: Intel X710 DA-4

CPUアーキテクチャとオペレーティングシステム
-----------------------------------------------------

kamuee は、以下の環境で動作することが確認されています。

* PC アーキテクチャ: amd64/x86_64
* ARM アーキテクチャ: arm64(armv8a)

以下のオペレーティングシステムがテストされています。

+ Ubuntu 18.04.2 LTS

本パッケージに付属の DPDK/igb_uioドライバを使う場合には、
以下の Linux カーネルを利用する必要があります。

- Linux kernel: linux-image-4.15.0-50-generic

本パッケージに含まれる関連ソフトウェア
-----------------------------------------------------

+ DPDK 18.11.2 (x86_64-nehalem-linuxapp-gcc)
+ DPDK 19.02.0 (arm64-armv8a-linuxapp-gcc)

本パッケージが前提とする関連ソフトウェア
-----------------------------------------------------

debian パッケージ（dpkg）で提供される本パッケージでは、
必要なソフトウェアは自動でインストールされますので、
特別な準備は必要ありません。

.. code-block:: text

    libc6 (>= 2.27), liburcu-dev (>= 0.10.1), pkg-config (>= 0.29.1), libjson-c-dev (>= 0.12.1), libmnl-dev (>= 1.0.4), libnuma-dev (>= 2.0.11)


事前準備: hugepage 設定
-----------------------------------------------------

DPDK のアプリケーションを動かすためには、Hugepage の設定が必要となります。
本マニュアルでは、1GB Hugepage の設定を推奨しています。

本パッケージに付属のシェルスクリプト(dpdk-hugepage-1G.sh)を利用して、
1GB Hugepageを設定できます。

* /usr/local/share/kamuee/dpdk-hugepage-1G.sh

.. code-block:: text

  sh dpdk-hugepages-1G.sh
  reboot

.. note::

  You can check the hugepages are configured with
  ``cat /proc/meminfo | grep -i huge``.

Intel NIC
-----------------------------------------------------


uio_pci_generic の利用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

  # lshw -class net -businfo

  Bus info          Device      Class          Description
  ========================================================
  pci@0000:01:00.0  eno1        network        Ethernet Controller 10G X550T
  pci@0000:01:00.1  eno2        network        Ethernet Controller 10G X550T
  pci@0000:18:00.0  enp24s0f0   network        Ethernet Controller 10-Gigabit X540-AT2
  pci@0000:18:00.1  enp24s0f1   network        Ethernet Controller 10-Gigabit X540-AT2

  # modprobe uio_pci_generic
  # /usr/local/share/dpdk/usertools/dpdk-devbind.py -b uio_pci_generic 18:00.0
  # /usr/local/share/dpdk/usertools/dpdk-devbind.py -b uio_pci_generic 18:00.1
  # /usr/local/share/dpdk/usertools/dpdk-devbind.py -s
  ..(snip)
  Network devices using DPDK-compatible driver
  ============================================
  0000:18:00.0 'Ethernet Controller 10-Gigabit X540-AT2' drv=uio_pci_generic unused=ixgbe
  0000:18:00.1 'Ethernet Controller 10-Gigabit X540-AT2' drv=uio_pci_generic unused=ixgbe

  Network devices using kernel driver
  ===================================
  ..(snip)

igb_uio.ko
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

  # modprobe uio
  # insmod /usr/local/share/dpdk/$(RTE_TARGET)/kmod/igb_uio.ko
  # /usr/local/share/dpdk/usertools/dpdk-devbind.py -b igb_uio 18:00.0
  # /usr/local/share/dpdk/usertools/dpdk-devbind.py -b igb_uio 18:00.1

Mellanox NIC
-----------------------------------------------------

Install MLX OFED

ofed-version: 4.5-1.0.1.0

.. code-block:: text

  $ sudo apt update && sudo apt install --yes \
          unzip quilt debhelper libnl-route-3-200 \
          chrpath python-libxml2 dkms libltdl-dev \
          swig dpatch graphviz
  $ mkdir $HOME/mlnx
  $ OFED_VER=4.5-1.0.1.0
  $ OFED_URL=http://content.mellanox.com/ofed/MLNX_OFED-${OFED_VER}
  $ OFED_FILE=MLNX_OFED_LINUX-${OFED_VER}-ubuntu18.04-x86_64.tgz
  $ OFED_FILE_BASE=${OFED_FILE%.*}
  $ wget --quiet ${OFED_URL}/${OFED_FILE} -O $HOME/${OFED_FILE}
  $ tar xvf $HOME/${OFED_FILE} -C $HOME/mlnx
  $ cd $HOME/mlnx/${OFED_FILE_BASE}/
  $ sudo ./mlnxofedinstall --force --upstream-libs --dpdk

HardwareのFWをresetして再起動.

.. code-block:: text

  $ sudo /etc/init.d/openibd restart
  $ sudo mlxconfig -d 3b:00.0 reset
  $ sudo reboot


（オプション）KVM/QEMU
-----------------------------------------------------


QEMU with PCI-passthrough
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

  echo 1 > /sys/class/net/enp0s1f0/devices/sriov_numvfs
  echo 1 > /sys/class/net/enp0s1f1/devices/sriov_numvfs
  dpdk_nic_bind -b vfio-pci 01:00.2
  dpdk_nic_bind -b vfio-pci 01:00.3
  qemu-system-x86_64 \
    -cpu host -enable-kvm \
    -smp 8 -m 8000 -hda $IMAGE \
    -net nic,macaddr=52:54:00:22:22:22 \
    -net tap,script=ifup.sh,downscript=ifdown.sh \
    -vnc :1,password -monitor stdio \
         -device vfio-pci,host=01:00.2 \
         -device vfio-pci,host=01:00.3


QEMU with SR-IOV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

  linux cmdline
  “intel_iommu=on pci=assign-busses pci=realloc”

  sudo mst start   ## start mst daemon, this enables us to check mlx5 config and registers
  sudo mlxconfig -d /dev/mst/mtXXXX_pciconf0 q | grep SRIOV   ## check sriov is enabled on mlx5
  sudo  mlxconfig -d /dev/mst/mt4119_pciconf0 q | grep -e "NUM_OF_VFS" -e "SRIOV"
  sudo  mlxconfig -y -d /dev/mst/mt4119_pciconf4 set SRIOV_EN=1 NUM_OF_VFS=16


- PROS:
	- Good Performance
- CONS:
	- Slow to start VM
	- Difficult to migrat VM
	- Need restart when sriov-config is changed


