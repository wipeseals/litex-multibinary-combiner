from dataclasses import dataclass
import json
import argparse
from pathlib import Path
from typing import List
from rich.logging import RichHandler
import logging


@dataclass
class MemEntry:
    parent_dir: Path
    name: str
    start: int

    @property
    def path(self) -> Path:
        return self.parent_dir / self.name

    @property
    def size(self) -> int:
        return self.path.stat().st_size

    @property
    def end(self) -> int:
        return self.start + self.size

    def __hash__(self):
        return hash((self.parent_dir, self.name, self.start))

    def __eq__(self, other):
        if not isinstance(other, MemEntry):
            return NotImplemented
        return (self.parent_dir, self.name, self.start) == (
            other.parent_dir,
            other.name,
            other.start,
        )


def process_args(args):
    # 必要な設定を読み込む
    boot_json: Path = Path(args.boot_json)
    boot_parent_dir: Path = boot_json.parent
    output_file: str = (
        args.output_dir if args.output_dir else boot_parent_dir / "Combined.bin"
    )
    initial_value: int = args.initial_value

    # boot.jsonから対象確認
    # e.g. {"boot": "0x00000000", "boot2": "0x00040000", ...}
    boot_conf = json.loads(boot_json.read_text())
    # hex str -> int
    # bootargs: {r1: "0x00000000", r2: "0x00040000", ...} が指定されるケースは無視
    boot_conf: List[MemEntry] = {
        MemEntry(parent_dir=boot_parent_dir, name=k, start=int(v, 16))
        for k, v in boot_conf.items()
        if k != "bootargs"
    }
    # sort by value
    boot_conf: List[MemEntry] = sorted(boot_conf, key=lambda x: x.start)
    start_addr: int = (
        args.start_addr if args.start_addr is not None else boot_conf[0].start
    )
    end_addr: int = boot_conf[-1].end
    total_size: int = end_addr - start_addr
    assert total_size > 0, "Invalid total size"

    logging.info(f"Boot JSON Path: {boot_json}")
    logging.info(f"Output File: {output_file}")
    logging.info(f"Initial Value: {initial_value}")
    logging.info(f"Start Address: 0x{start_addr:016x}")
    logging.info(f"End Address: 0x{end_addr:016x}")
    logging.info(f"Total Size: {total_size} bytes")

    # boot_conf に従ってバイナリを結合
    with open(output_file, "wb") as f:
        current_addr: int = start_addr
        # 順に結合
        for entry in boot_conf:
            # エントリ間の空き領域を埋める
            if current_addr < entry.start:
                fill_bytes: int = entry.start - current_addr
                logging.info(
                    f"0x{current_addr:016x} - 0x{entry.start:016x}: {fill_bytes} bytes\tFill with 0x{initial_value:02x}"
                )
                f.write(bytes([initial_value] * (entry.start - current_addr)))
                current_addr = entry.start
            # ファイルを結合
            logging.info(
                f"0x{entry.start:016x} - 0x{entry.end:016x}: {entry.size} bytes\t{entry.name}"
            )
            f.write(entry.path.read_bytes())
            current_addr = entry.end
    # 完了
    logging.info(f"Done. Output: {output_file}")


def main():
    logging.basicConfig(
        level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )
    parser = argparse.ArgumentParser(
        description="Process boot.json location and output directory."
    )
    parser.add_argument("boot_json", type=str, help="Path to the boot.json file")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Path to the output directory (default: None)",
    )
    parser.add_argument(
        "--start-addr",
        type=int,
        default=None,
        help="Starting address (default: None)",
    )
    parser.add_argument(
        "--initial-value", type=int, default=0, help="Initial value (default: None)"
    )
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    main()
