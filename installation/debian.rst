
Setup with debian package
=========================

1. install kamuee with debian-package and reboot

.. code-block:: text

  wget http://kamuee-web.nttcloud.net/download/kamuee_0.6.2o_amd64.deb
  wget http://kamuee-web.nttcloud.net/download/dpdk-hugepage-1G.sh
  apt install -y ./kamuee_0.6.2o_amd64.deb
  sh dpdk-hugepages-1G.sh
  reboot

.. note::

  You can check the hugepages are configured with
  ``cat /proc/meminfo | grep -i huge``.

2. check pci-devices and bind them as dpdk-interface. (in this example, we will choose X540 for dpdk)

.. code-block:: text

  lshw -class net -businfo

  Bus info          Device      Class          Description
  ========================================================
  pci@0000:01:00.0  eno1        network        Ethernet Controller 10G X550T
  pci@0000:01:00.1  eno2        network        Ethernet Controller 10G X550T
  pci@0000:18:00.0  enp24s0f0   network        Ethernet Controller 10-Gigabit X540-AT2
  pci@0000:18:00.1  enp24s0f1   network        Ethernet Controller 10-Gigabit X540-AT2

  modprobe uio_pci_generic
  /usr/local/share/dpdk/usertools/dpdk-devbind.py -b uio_pci_generic 18:00.0
  /usr/local/share/dpdk/usertools/dpdk-devbind.py -b uio_pci_generic 18:00.1
  /usr/local/share/dpdk/usertools/dpdk-devbind.py -s
  ..(snip)
  Network devices using DPDK-compatible driver
  ============================================
  0000:18:00.0 'Ethernet Controller 10-Gigabit X540-AT2' drv=uio_pci_generic unused=ixgbe
  0000:18:00.1 'Ethernet Controller 10-Gigabit X540-AT2' drv=uio_pci_generic unused=ixgbe

  Network devices using kernel driver
  ===================================
  ..(snip)

3. start kamuee with systemctl

.. code-block:: text

  systemctl start kamuee
  telnet localhost 9077
  Trying ::1...
  Trying 127.0.0.1...
  Connected to localhost.
  Escape character is '^]'.
  skylake-100g-8[vty0]> show port
  port-18-0-0  0 0  0 975 AC:1F:6B:89:A4:54 ixgbe       0 10G/1G
  port-18-0-1  1 0  0 976 AC:1F:6B:89:A4:55 ixgbe       0 10G/1G


