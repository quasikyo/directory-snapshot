from pathlib import Path

TIMESTAMP_FORMAT: str = "%Y-%m-%d %H-%M-%S"
TARGET_ARG: str = "target"
CONFIG_ARG: str = "config"
VERBOSE_ARG: str = "verbose"
DEFAULT_CONFIG_PATH: Path = Path(Path(__file__).parent, "targets.toml")
TARGETS_CONFIG: str = "targets"
GLOBAL_DESTINATION_CONFIG: str = "global_destination"
SOURCE_CONFIG: str = "source"
