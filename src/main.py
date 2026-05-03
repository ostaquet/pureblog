import argparse
from pathlib import Path
import sys

from builder import BlogBuilder
from config import BlogConfig, ConfigError, load_config

DEFAULT_CONFIG_PATH: Path = Path("config/config.yml")

def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint. Loads configuration then builds the site."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Build the static blog site."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to the configuration file (default: {DEFAULT_CONFIG_PATH}).",
    )
    args: argparse.Namespace = parser.parse_args(argv)
    
    try:
        cfg: BlogConfig = load_config(args.config)
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    BlogBuilder(cfg).build_site()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
