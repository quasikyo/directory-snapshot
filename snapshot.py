import argparse
from datetime import datetime
import logging as log
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib as toml
from typing import Any


TIMESTAMP_FORMAT: str = "%Y-%m-%d %H-%M-%S"
TARGET_ARG: str = "target"
CONFIG_ARG: str = "config"
VERBOSE_ARG: str = "verbose"
DEFAULT_CONFIG_PATH: Path = Path(Path(__file__).parent, "targets.toml")
TARGETS_CONFIG: str = "targets"
GLOBAL_DESTINATION_CONFIG: str = "global_destination"
SOURCE_CONFIG: str = "source"


def parse_args() -> dict[str, Any]:
	parser = argparse.ArgumentParser(
		prog="Backup Creator",
		description="Creates snapshots of directories."
	)
	parser.add_argument(
		f"-{TARGET_ARG[0]}", f"--{TARGET_ARG}",
		# 2025-JAN-25: TODO: Snapshots all directories if not provded.
		help="""
			Target that corresponds to a config.
			If a path to a file, parses file name without the extension.
			If an executable, executes it.
		""",
		type=str,
		required=True
	)
	parser.add_argument(
		f"-{CONFIG_ARG[0]}", f"--{CONFIG_ARG}",
		help="Path to a .toml config file.",
		required=False,
		type=str,
		default=str(DEFAULT_CONFIG_PATH)
	)
	parser.add_argument(
		f"--{VERBOSE_ARG}", "--debug",
		help="Enables DEBUG logs.",
		required=False,
		action="store_true"
	)
	return vars(parser.parse_args())


def parse_config(config_path: str) -> dict[str, Any]:
	parsed_config = None
	log.info(f"Parsing config from: {config_path}")
	with open(config_path, "rb") as config_file:
		parsed_config = toml.load(config_file)
		log.debug(f"Parsed config: {parsed_config}")
	return parsed_config


def main(args: dict[str, Any]) -> None:
	log.debug(f"Called with args: {args}")
	config_path = args.get(CONFIG_ARG, str(DEFAULT_CONFIG_PATH))
	full_config = parse_config(config_path)

	if args.get(TARGET_ARG, None) is not None:
		target = Path(args.get(TARGET_ARG, "")).stem
		log.info(f"Target specified: {target}")
		target_config = full_config.get(TARGETS_CONFIG, {}).get(target, None)
		if target_config is None:
			log.error(f"Config for target {target} not found.")
			sys.exit(1)
		log.debug(f"Target config: {target_config}")

		now = datetime.now().strftime(TIMESTAMP_FORMAT)
		source_path = Path(target_config[SOURCE_CONFIG])
		destination_path = Path(full_config[GLOBAL_DESTINATION_CONFIG]).joinpath(source_path.name)
		destination_path = destination_path.with_name(f"{destination_path.name} {now}")
		shutil.copytree(
			src=source_path,
			dst=destination_path,
			dirs_exist_ok=True
		)
		subprocess.call([args[TARGET_ARG]])


if __name__ == "__main__":
	args = parse_args()
	log_level = log.DEBUG if args["verbose"] else log.INFO
	log.basicConfig(
		level=log_level,
		format='%(asctime)s %(levelname)-8s %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
	)
	main(args)
