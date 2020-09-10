write file: コンフィグレーション保存機能
--------------------------------------------------------

* *CLI形式*

.. code-block:: none

   write (file|memory|terminal) (FILE|)

* *説明*

本機能は、現在実行中のポートやデバイスの状態をKamuee コマンドライン形
式で保存し、次回 Kamuee起動時に利用できるようにします。

* *処理*

  * 現在のポートコンフィグレーション状態を Kamuee CLI形式でファイ
    ルや端末に書き出します。

* *引数*

  * 第二引数が file の場合は、FILE に情報を書き出す。FILE が省略され
    た場合はデフォルトコンフィグレーションファイル
    (/etc/kamuee/kamuee.conf)に情報を書き出します。kamuee.conf がすでに
    存在する場合は、古いファイル内容が /etc/kamuee/kamuee.conf.save
    に保存されます。
  * 第二引数が memory の場合は、デフォルトコンフィグレーションファイ
    ル(/etc/kamuee/kamuee.conf) に情報を上書きします。kamuee.conf がすで
    に存在する場合でも強制的に上書きされます。
  * 第二引数が terminal の場合は、端末に情報を書き出します。

* *制限事項*

  * 現時点では device 設定、port 設定だけが情報として書き出されます。


