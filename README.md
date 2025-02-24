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
  --start-addr START_ADDR
                        Starting address (default: None)
  --initial-value INITIAL_VALUE
                        Initial value (default: None)
```

### 引数

- `boot_json`: 結合するバイナリファイルの情報を記述した JSON ファイルのパス
- `--output-dir`: 結合されたバイナリファイルの出力先ディレクトリのパス
  - 未指定の場合、 `boot_json` と同じディレクトリに出力されます
- `--start-addr`: バイナリファイルの開始アドレス
  - 未指定の場合、 `boot.json` に記述されたアドレスの内、最小のアドレスが使用されます
- `--initial-value`: バイナリファイルの初期値
  - `boot.json` で定義されたエントリが存在しない場合に使用されます。デフォルトは 0

### 実行例

```sh
python main.py /path/to/boot.json
# /path/to/Combined.bin に結合されたバイナリファイルが出力されます。
```
