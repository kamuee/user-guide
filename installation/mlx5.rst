
Setup Mellanox ConnectX-5
==========================

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


Quick Setup Script
------------------

.. code-block:: text

  #!/bin/sh
  set -ue
  PREF=$HOME/mlnx

  mkdir -p $PREF
  sudo apt update && sudo apt install --yes \
          unzip quilt debhelper libnl-route-3-200 \
          chrpath python-libxml2 dkms libltdl-dev \
          swig dpatch graphviz
  OFED_VER=4.5-1.0.1.0
  OFED_URL=http://content.mellanox.com/ofed/MLNX_OFED-${OFED_VER}
  OFED_FILE=MLNX_OFED_LINUX-${OFED_VER}-ubuntu18.04-x86_64.tgz
  OFED_FILE_BASE=${OFED_FILE%.*}
  wget --quiet ${OFED_URL}/${OFED_FILE} -O $PREF/${OFED_FILE}
  tar xvf $PREF/${OFED_FILE} -C $PREF
  cd $PREF/${OFED_FILE_BASE}/
  sudo ./mlnxofedinstall --force --upstream-libs --dpdk

.. MFT_VER=4.9.0-38
.. MFT_URL=http://www.mellanox.com/downloads/MFT
.. MFT_FILE=mft-${MFT_VER}-x86_64-deb.tgz
.. MFT_FILE_BASE=${MFT_FILE%.*}
.. wget --quiet ${MFT_URL}/${MFT_FILE} -O $PREF/${MFT_FILE}
.. tar xvf $PREF/${MFT_FILE} -C $PREF
.. cd $PREF/${MFT_FILE_BASE}/
.. sudo ./install.sh
.. sudo rm -f /boot/initrd.img-*.old-dkms
