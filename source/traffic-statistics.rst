
トラフィック統計
=======================

　ポートの転送パケット数（pps）を確認したい場合は、 **show port statistics all pps** コマンドを実行します。


    ::

		kamuee[vty0]> show port statistics all pps
		I/F          ipackets           ierrs opackets           oerrs imiss  nombuf
		port-2-0-0   0                  0     0                  0     0      0
		port-2-0-1   28                 0     0                  0     0      0
		total        28                 0     0                  0     0      0
		kamuee[vty0]>

    ..


　CPUスレッドでの転送パケット数（pps）を確認したい場合は、 **show thread sttistics pps** コマンドで確認できます。


    ::


		title            rxframes        txframes         discard
		                rxpackets       txpackets       forwarded            ours
		                     drop         noroute       malformed        filtered
		core[2]:                0               0               0
		                        0               0               0               0
		                        0               0               0               0
		core[3]:                0               0               0
		                        0               0               0               0
		                        0               0               0               0
		core[4]:                0               0               0
		                        0               0               0               0
		                        0               0               0               0

    ..



　CPUスレッドの情報を確認したい場合は、 **show thread info** コマンドで確認できます。


    ::


		kamuee[vty0]> show thread info
		core[id]: v thread name        lcpu pcpu port  rxq funcp
		core[0]:  1 (null)                0    0    0    0 (nil)
		core[1]:  1 OS                    0   --   --   -- (nil)
		core[2]:  1 lthread_scheduler     0   --   --   -- 0x55da75882840
		core[3]:  1 forwarder             0   --   --   -- 0x55da757a5540
		core[4]:  1 forwarder             0    0    0    0 0x55da757a5540
		core[5]:  1 forwarder             0    0    0    1 0x55da757a5540
		core[6]:  1 rib_manager           1   --   --   -- 0x55da7577c640
		core[7]:  1 tap_manager           1   --   --   -- 0x55da75817a50
		core[8]:  1 forwarder             1    0    0    2 0x55da757a5540
		core[9]:  1 forwarder             1    0    0    3 0x55da757a5540
		core[10]: 1 forwarder             1    0    1    0 0x55da757a5540
		core[11]: 1 forwarder             1    0    1    1 0x55da757a5540
		core[12]: 1 forwarder             0    0    1    2 0x55da757a5540
		core[13]: 1 forwarder             0    0    1    3 0x55da757a5540
		core[14]: 1 forwarder             0   --   --   -- 0x55da757a5540
		core[15]: 1 forwarder             0   --   --   -- 0x55da757a5540
		core[16]: 1 forwarder             0   --   --   -- 0x55da757a5540
		core[17]: 1 forwarder             0   --   --   -- 0x55da757a5540
		core[18]: 1 forwarder             1   --   --   -- 0x55da757a5540
		core[19]: 1 forwarder             1   --   --   -- 0x55da757a5540
		core[20]: 1 forwarder             1   --   --   -- 0x55da757a5540
		core[21]: 1 forwarder             1   --   --   -- 0x55da757a5540
		core[22]: 1 OS                    1   --   --   -- (nil)
		core[23]: 1 OS                    1   --   --   -- (nil)
		kamuee[vty0]>

    ..



