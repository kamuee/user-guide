
Feature / Support
=================

Feature
--------

Supported

- IPv4/IPv6 packet forwarding
- IPv4/IPv6 neighbor protocol (ARP/NDP)
- IPv4/IPv6 ICMP handling
- IPv4 Routing Protocols (RIP2/OSPFv2/BGP4)
- IPv6 Routing Protocols (RIPng/OSPFv3/BGP4+)
- IEEE802.1Q tagged VLAN
- SNMP
- Port Mirroring
- VRRP
- Proxy-arp
- VRF
- ACL
- CLI
- Port mirror
- LLDP
- DHCP
- MTU 1500-9000
- Segment Routing IPv6
- Multipath (ECMP)
- Multicast
- BFD

Soon will be Supported

- EVPN/VXLAN
- pcap/tcpdump

Not Supported (TODO)

- MPLS
- Segment Routing MPLS
- L2 Switching
- Spanning Tree Protocol
- GRE
- LAG
- sFlow/Netflow
- NAT
- Policy Based Routing
- GTP (5G)
- IPsec
- BGP Flowspec
- REST API

Support
--------

Network Interfaces

- IXGBE (Intel 10GbE): X540, X550
- I40E (Intel 40GbE): X710 XL710
- MLX5 (Mellanox 100GbE): ConnectX-4, ConnectX-5
- Virtio-net (indirect-txq)
- Vhost-net (indirect-txq)
- Vhost-user (indirect-txq)

CPUs

- Intel Xeon Skylake-sp
- Intel Xeon Broadwell

Hardware Requirement
--------------------

- CPU: >= 8 cores
- NIC: DPDK Supported NIC
- Memory: >= 16GB


