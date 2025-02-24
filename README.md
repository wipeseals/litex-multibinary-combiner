# LiteX Multibinary Combiner

このプロジェクトは、複数のバイナリファイルを 1 つに結合するためのツールです。
LiteX の `Uploading multiple binaries with a JSON description file` 非対応の Loader で使用する目的に実装されました。
<https://github.com/enjoy-digital/litex/wiki/Load-Application-Code-To-CPU>

## 使用方法

以下のコマンドを使用して、複数のバイナリファイルを結合できます。

```sh
usage: main.py [-h] [--output-dir OUTPUT_DIR] [--start-addr START_ADDR] [--initial-value INITIAL_VALUE] boot_json

Process boot.json location and output directory.

positional arguments:
  boot_json             Path to the boot.json file

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Path to the output directory (default: None)
  --initial-value INITIAL_VALUE
                        Initial value (default: None)
```

### 引数

- `boot_json`: 結合するバイナリファイルの情報を記述した JSON ファイルのパス
- `--output-dir`: 結合されたバイナリファイルの出力先ディレクトリのパス
  - 未指定の場合、 `boot_json` と同じディレクトリに出力されます
- `--initial-value`: バイナリファイルの初期値
  - `boot.json` で定義されたエントリが存在しない場合に使用されます。デフォルトは 0

### 実行例

```sh
$ python main.py /path/to/boot.json

>python main.py  D:\Data\Downloads\linux_2022_03_23\boot.json
[17:52:18] INFO     Boot JSON Path: D:\Data\Downloads\linux_2022_03_23\boot.json                                                         main.py:68
           INFO     Output File: D:\Data\Downloads\linux_2022_03_23\Combined.bin                                                         main.py:69
           INFO     Initial Value: 0                                                                                                     main.py:70
           INFO     Start Address: 0x0000000040000000                                                                                    main.py:71
           INFO     End Address: 0x000000004139b400                                                                                      main.py:72
           INFO     Total Size: 20558848 bytes                                                                                           main.py:73
           INFO     0x0000000040000000 - 0x000000004072ebcc: 7531468 bytes  Image                                                        main.py:89
           INFO     0x000000004072ebcc - 0x0000000040ef0000: 8131636 bytes  Fill with 0x00                                               main.py:83
           INFO     0x0000000040ef0000 - 0x0000000040ef07cf: 1999 bytes     rv32.dtb                                                     main.py:89
           INFO     0x0000000040ef07cf - 0x0000000040f00000: 63537 bytes    Fill with 0x00                                               main.py:83
           INFO     0x0000000040f00000 - 0x0000000040f0d188: 53640 bytes    opensbi.bin                                                  main.py:89
           INFO     0x0000000040f0d188 - 0x0000000041000000: 994936 bytes   Fill with 0x00                                               main.py:83
           INFO     0x0000000041000000 - 0x000000004139b400: 3781632 bytes  rootfs.cpio                                                  main.py:89
           INFO     Done. Output: D:\Data\Downloads\linux_2022_03_23\Combined.bin                                                        main.py:95
```
