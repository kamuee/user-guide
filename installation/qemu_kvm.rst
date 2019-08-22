
Running Kamuee on Virtulization Environment
=============================================

KVM
-----

About setup is documented at [here](setup.md).
Tested VM configuration is bellow.

.. code-block:: text

  <domain type='kvm' id='3'>
    <name>kamuee</name>
    <uuid>e1066f6a-04b1-47db-b454-180b32b4371c</uuid>
    <memory unit='KiB'>16384000</memory>
    <currentMemory unit='KiB'>16384000</currentMemory>
    <memoryBacking>
      <hugepages/>
    </memoryBacking>
    <vcpu placement='static'>16</vcpu>
    <resource>
      <partition>/machine</partition>
    </resource>
    <os>
      <type arch='x86_64' machine='pc-i440fx-xenial'>hvm</type>
      <boot dev='hd'/>
    </os>
    <features>
      <acpi/>
      <apic/>
    </features>
    <cpu mode='host-passthrough'>
      <topology sockets='1' cores='16' threads='1'/>
      <feature policy='require' name='avx512cd'/>
      <feature policy='require' name='avx512f'/>
      <feature policy='require' name='mpx'/>
      <feature policy='require' name='abm'/>
      <feature policy='require' name='pdpe1gb'/>
      <feature policy='require' name='rdrand'/>
      <feature policy='require' name='f16c'/>
      <feature policy='require' name='osxsave'/>
      <feature policy='require' name='dca'/>
      <feature policy='require' name='pdcm'/>
      <feature policy='require' name='xtpr'/>
      <feature policy='require' name='tm2'/>
      <feature policy='require' name='est'/>
      <feature policy='require' name='smx'/>
      <feature policy='require' name='vmx'/>
      <feature policy='require' name='ds_cpl'/>
      <feature policy='require' name='monitor'/>
      <feature policy='require' name='dtes64'/>
      <feature policy='require' name='pbe'/>
      <feature policy='require' name='tm'/>
      <feature policy='require' name='ht'/>
      <feature policy='require' name='ss'/>
      <feature policy='require' name='acpi'/>
      <feature policy='require' name='ds'/>
      <feature policy='require' name='vme'/>
    </cpu>
    <clock offset='utc'>
      <timer name='rtc' tickpolicy='catchup'/>
      <timer name='pit' tickpolicy='delay'/>
      <timer name='hpet' present='no'/>
    </clock>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>restart</on_crash>
    <pm>
      <suspend-to-mem enabled='no'/>
      <suspend-to-disk enabled='no'/>
    </pm>
    <devices>
      <emulator>/usr/bin/kvm-spice</emulator>
      <disk type='file' device='disk'>
        <driver name='qemu' type='qcow2'/>
        <source file='/var/lib/libvirt/images/kamuee-ubuntu.img'/>
        <backingStore/>
        <target dev='hda' bus='ide'/>
        <alias name='ide0-0-0'/>
        <address type='drive' controller='0' bus='0' target='0' unit='0'/>
      </disk>
      <disk type='file' device='cdrom'>
        <driver name='qemu' type='raw'/>
        <backingStore/>
        <target dev='hdb' bus='ide'/>
        <readonly/>
        <alias name='ide0-0-1'/>
        <address type='drive' controller='0' bus='0' target='0' unit='1'/>
      </disk>
      <controller type='usb' index='0' model='ich9-ehci1'>
        <alias name='usb'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x7'/>
      </controller>
      <controller type='usb' index='0' model='ich9-uhci1'>
        <alias name='usb'/>
        <master startport='0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0' multifunction='on'/>
      </controller>
      <controller type='usb' index='0' model='ich9-uhci2'>
        <alias name='usb'/>
        <master startport='2'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x1'/>
      </controller>
      <controller type='usb' index='0' model='ich9-uhci3'>
        <alias name='usb'/>
        <master startport='4'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x2'/>
      </controller>
      <controller type='ide' index='0'>
        <alias name='ide'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
      </controller>
      <controller type='pci' index='0' model='pci-root'>
        <alias name='pci.0'/>
      </controller>
      <interface type='network'>
        <mac address='52:54:00:94:cc:a2'/>
        <source network='default' bridge='virbr0'/>
        <target dev='vnet0'/>
        <model type='virtio'/>
        <alias name='net0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
      </interface>
      <interface type='bridge'>
        <mac address='52:54:00:66:66:66'/>
        <source bridge='ovs0'/>
        <virtualport type='openvswitch'>
          <parameters interfaceid='e905484e-d447-49a5-9971-457e343ce6af'/>
        </virtualport>
        <target dev='vnet1'/>
        <model type='virtio'/>
        <driver name='vhost'/>
        <alias name='net1'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
      </interface>
      <interface type='bridge'>
        <mac address='52:54:00:77:77:77'/>
        <source bridge='ovs0'/>
        <virtualport type='openvswitch'>
          <parameters interfaceid='0b060c88-7d7e-4ebb-b41b-22b85970186b'/>
        </virtualport>
        <target dev='vnet2'/>
        <model type='virtio'/>
        <driver name='vhost'/>
        <alias name='net2'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
      </interface>
      <serial type='pty'>
        <source path='/dev/pts/3'/>
        <target port='0'/>
        <alias name='serial0'/>
      </serial>
      <console type='pty' tty='/dev/pts/3'>
        <source path='/dev/pts/3'/>
        <target type='serial' port='0'/>
        <alias name='serial0'/>
      </console>
      <input type='mouse' bus='ps2'/>
      <input type='keyboard' bus='ps2'/>
      <graphics type='vnc' port='5900' autoport='yes' listen='0.0.0.0' keymap='en-us'>
        <listen type='address' address='0.0.0.0'/>
      </graphics>
      <video>
        <model type='cirrus' vram='16384' heads='1'/>
        <alias name='video0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
      </video>
      <memballoon model='virtio'>
        <alias name='balloon0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
      </memballoon>
    </devices>
    <seclabel type='dynamic' model='apparmor' relabel='yes'>
      <label>libvirt-e1066f6a-04b1-47db-b454-180b32b4371c</label>
      <imagelabel>libvirt-e1066f6a-04b1-47db-b454-180b32b4371c</imagelabel>
    </seclabel>
  </domain>


QEMU with PCI-passthrough
--------------------------

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
----------------

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


