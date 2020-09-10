device unbind: デバイスunbind機能
--------------------------------------------------------

* *CLI形式*

.. code-block:: none

    device unbind DEVICE

* *説明*

本機能は、PMDにバインド済みの物理デバイスのドライバをバインド解除します。

* *処理*

  * 指定されたデバイスのドライバをアンバインドします
    (dpdk-devbind.py --unbind DEVICEと同等)。

* *引数*

  * 引数 DEVICE 部には物理PCIデバイスの識別子(BDF形式文字列)を指定します。

* *前提条件*

  * Kamueeポートとして利用中のデバイスは unbind しません。
  * Kernelモードポートとして利用中のデバイスも unbind しません。
  * 引数 DEVICE に指定するデバイスアドレス文字列は DPDK関数
    rte_pci_addr_parse() によって解釈可能な形式に限られます。

