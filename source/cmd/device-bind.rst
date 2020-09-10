device bind: デバイスbind機能
--------------------------------------------------------

* *CLI形式*

.. code-block:: none

    device bind DEVICE (DRIVER|none)

* *説明*

本機能は、システム内に存在する物理デバイスに対して DPDKのポールモードド
ライバ(PMD)をバインドし、Kamuee ポートとして利用できるようにします。

* *処理*

  * 指定されたデバイスにドライバをバインド/アンバインドします
    (dpdk-devbind.py --bind=DRIVER DEVICE と同等の処理を実行します)。

* *引数*

  * 引数 DEVICE 部には 物理PCIデバイスの識別子(BDF形式文字列)を指定し
    ます。
  * 引数 DRIVER 部にはドライバ名称 (典型的には igb_uio) を指定します。
  * 引数 DRIVER 部分に none を指定した場合は unbind 処理を行います。

* *前提条件*

  * Kamueeポートとして利用中のデバイスは再 bind しません。
  * すでに同じドライバにバインド済の場合は再 bind しません。
  * 指定のドライバとは違うドライバにバインド済の場合は、一旦 unbind
    した後 bind が実行されます。
  * 引数 DEVICE に指定するデバイスアドレス文字列は DPDK関数
    rte_pci_addr_parse() によって解釈可能な形式に限られます。



