"""Configuration manager for the blog engine.

Reads, validates, and exposes settings from a YAML configuration file.
Centralizes all blog settings so the engine is reusable for other blogs
without changes to the source code.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml


class ConfigError(Exception):
    """Raised when the configuration file is missing or invalid."""


@dataclass(frozen=True)
class BlogConfig:
    site_title: str
    site_url: str
    author: str
    posts_dir: Path
    build_dir: Path
    assets_dir: Path
    robots_file: Path
    languages: list[str]
    reading_time_labels: dict[str, str]
    back_labels: dict[str, str]
    default_timezone: ZoneInfo
    default_publish_hour: int
    template_file: Path
    style_file: Path


def _require_section(data: dict[str, Any], section: str) -> dict[str, Any]:
    if section not in data:
        raise ConfigError(
            f"Missing section '{section}' in configuration. "
            f"Add a top-level '{section}:' block to the YAML file."
        )
    value: Any = data[section]
    if not isinstance(value, dict):
        raise ConfigError(
            f"Section '{section}' must be a mapping, got {type(value).__name__}."
        )
    return value


def _require_field(section: dict[str, Any], section_name: str, field: str) -> Any:
    if field not in section or section[field] is None:
        raise ConfigError(
            f"Missing field '{field}' in section '{section_name}'. "
            f"Add '{field}: <value>' under the '{section_name}:' block."
        )
    return section[field]


def _require_str(section: dict[str, Any], section_name: str, field: str) -> str:
    value: Any = _require_field(section, section_name, field)
    if not isinstance(value, str) or not value:
        raise ConfigError(
            f"Field '{section_name}.{field}' must be a non-empty string."
        )
    return value


def _require_int(section: dict[str, Any], section_name: str, field: str) -> int:
    value: Any = _require_field(section, section_name, field)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ConfigError(
            f"Field '{section_name}.{field}' must be an integer."
        )
    return value


def _require_lang_map(
    section: dict[str, Any],
    section_name: str,
    field: str,
    languages: list[str],
) -> dict[str, str]:
    value: Any = _require_field(section, section_name, field)
    if not isinstance(value, dict):
        raise ConfigError(
            f"Field '{section_name}.{field}' must be a mapping of language code to label."
        )
    result: dict[str, str] = {}
    for lang in languages:
        if lang not in value:
            raise ConfigError(
                f"Missing label for language '{lang}' in '{section_name}.{field}'. "
                f"Add '{lang}: <label>' under '{section_name}.{field}'."
            )
        label: Any = value[lang]
        if not isinstance(label, str) or not label:
            raise ConfigError(
                f"Label '{section_name}.{field}.{lang}' must be a non-empty string."
            )
        result[lang] = label
    return result


def _parse_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise ConfigError(
            f"Unknown timezone '{name}' in 'publish.default_timezone'. "
            f"Use an IANA timezone identifier such as 'Europe/Brussels' or 'UTC'."
        ) from exc


def load_config(config_path: Path) -> BlogConfig:
    """Read and validate a configuration file. Raises ConfigError on failure."""
    if not config_path.is_file():
        raise ConfigError(
            f"Configuration file not found: {config_path}. "
            f"Create it or pass a different path with --config."
        )
    raw_text: str = config_path.read_text(encoding="utf-8")
    try:
        data: Any = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        raise ConfigError(
            f"Could not parse YAML in {config_path}: {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise ConfigError(
            f"Configuration root in {config_path} must be a mapping."
        )

    general: dict[str, Any] = _require_section(data, "general")
    seo: dict[str, Any] = _require_section(data, "seo")
    languages_section: dict[str, Any] = _require_section(data, "languages")
    publish: dict[str, Any] = _require_section(data, "publish")
    theme: dict[str, Any] = _require_section(data, "theme")

    site_title: str = _require_str(general, "general", "site_title")
    site_url: str = _require_str(general, "general", "site_url")
    author: str = _require_str(general, "general", "author")
    posts_dir: Path = Path(_require_str(general, "general", "posts_dir"))
    build_dir: Path = Path(_require_str(general, "general", "build_dir"))
    assets_dir: Path = Path(_require_str(general, "general", "assets_dir"))

    robots_file: Path = Path(_require_str(seo, "seo", "robots_file"))

    codes_value: Any = _require_field(languages_section, "languages", "codes")
    if not isinstance(codes_value, list) or not codes_value:
        raise ConfigError(
            "Field 'languages.codes' must be a non-empty list of language codes."
        )
    languages: list[str] = []
    for entry in codes_value:
        if not isinstance(entry, str) or not entry:
            raise ConfigError(
                "Each entry in 'languages.codes' must be a non-empty string."
            )
        languages.append(entry)

    reading_time_labels: dict[str, str] = _require_lang_map(
        languages_section, "languages", "reading_time_labels", languages
    )
    back_labels: dict[str, str] = _require_lang_map(
        languages_section, "languages", "back_labels", languages
    )

    timezone_name: str = _require_str(publish, "publish", "default_timezone")
    default_timezone: ZoneInfo = _parse_timezone(timezone_name)
    default_publish_hour: int = _require_int(publish, "publish", "default_publish_hour")
    if not 0 <= default_publish_hour <= 23:
        raise ConfigError(
            "Field 'publish.default_publish_hour' must be between 0 and 23."
        )

    template_file: Path = Path(_require_str(theme, "theme", "template_file"))
    style_file: Path = Path(_require_str(theme, "theme", "style_file"))

    return BlogConfig(
        site_title=site_title,
        site_url=site_url,
        author=author,
        posts_dir=posts_dir,
        build_dir=build_dir,
        assets_dir=assets_dir,
        robots_file=robots_file,
        languages=languages,
        reading_time_labels=reading_time_labels,
        back_labels=back_labels,
        default_timezone=default_timezone,
        default_publish_hour=default_publish_hour,
        template_file=template_file,
        style_file=style_file,
    )
