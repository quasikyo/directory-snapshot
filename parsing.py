import argparse
import logging as log
import tomllib as toml
from dataclasses import dataclass
from typing import Any

import constants


@dataclass
class ProgramArgs:
	target: str
	config: str
	verbose: bool


@dataclass
class TargetConfig:
	source: str


@dataclass
class TargetsConfig:
	global_destination: str
	targets: dict[str, TargetConfig]


def parse_args() -> ProgramArgs:
	parser = argparse.ArgumentParser(
		prog="Backup Creator",
		description="Creates snapshots of directories."
	)
	parser.add_argument(
		f"-{constants.TARGET_ARG[0]}", f"--{constants.TARGET_ARG}",
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
		f"-{constants.CONFIG_ARG[0]}", f"--{constants.CONFIG_ARG}",
		help="Path to a .toml config file.",
		required=False,
		type=str,
		default=str(constants.DEFAULT_CONFIG_PATH)
	)
	parser.add_argument(
		f"--{constants.VERBOSE_ARG}", "--debug",
		help="Enables DEBUG logs.",
		required=False,
		action="store_true"
	)
	parsed_args = vars(parser.parse_args())
	return ProgramArgs(
		target=parsed_args.get(constants.TARGET_ARG, None),
		config=parsed_args.get(constants.CONFIG_ARG, constants.DEFAULT_CONFIG_PATH),
		verbose=parsed_args.get(constants.VERBOSE_ARG, False)
	)


def parse_config(config_path: str) -> TargetsConfig:
	parsed_config: dict[str, Any] = None
	log.info(f"Parsing config from: {config_path}")
	with open(config_path, "rb") as config_file:
		parsed_config = toml.load(config_file)
		log.debug(f"Parsed config: {parsed_config}")

	full_config = TargetsConfig(
		global_destination=parsed_config[constants.GLOBAL_DESTINATION_CONFIG],
		targets={}
	)
	for key, value in parsed_config.get(constants.TARGETS_CONFIG, {}).items():
		full_config.targets[key] = TargetConfig(
			source=value[constants.SOURCE_CONFIG]
		)
	return full_config
