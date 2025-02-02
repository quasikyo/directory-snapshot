import logging as log
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import constants
import parsing


def main(args: parsing.ProgramArgs) -> None:
	log.debug(f"Called with args: {args}")
	full_config: parsing.TargetsConfig = parsing.parse_config(args.config)

	if args.target is not None:
		target = Path(args.target).stem
		log.info(f"Target specified: {target}")
		target_config: parsing.TargetConfig = full_config.targets.get(target, None)
		if target_config is None:
			log.error(f"Config for target {target} not found.")
			sys.exit(1)
		log.debug(f"Target config: {target_config}")

		now = datetime.now().strftime(constants.TIMESTAMP_FORMAT)
		source_path = Path(target_config.source)
		destination_path = Path(full_config.global_destination).joinpath(target).joinpath(source_path.name)
		destination_path = destination_path.with_name(f"{destination_path.name} {now}")
		shutil.copytree(
			src=source_path,
			dst=destination_path,
			dirs_exist_ok=True
		)
		if os.access(args.target, os.X_OK):
			log.info(f"Target of {args.target} recognized as executable. Executing...")
			subprocess.call([args.target])


if __name__ == "__main__":
	args = parsing.parse_args()
	log_level = log.DEBUG if args.verbose else log.INFO
	log.basicConfig(
		level=log_level,
		format='%(asctime)s %(levelname)-8s %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
	)
	main(args)
