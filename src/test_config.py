"""Unit tests for the configuration manager."""

from pathlib import Path

import pytest

import config


VALID_CONFIG: str = """\
general:
  site_title: "Test Blog"
  site_url: "https://test.example"
  posts_dir: "posts"
  build_dir: "build"
languages:
  codes: [en, fr]
  reading_time_labels:
    en: "min read"
    fr: "min de lecture"
  back_labels:
    en: "Back"
    fr: "Retour"
publish:
  default_timezone: "Europe/Brussels"
  default_publish_hour: 13
theme:
  theme_dir: "theme"
  template_file: "template.html"
  style_file: "style.css"
"""


def _write(tmp_path: Path, content: str) -> Path:
    cfg_path: Path = tmp_path / "config.yml"
    cfg_path.write_text(content)
    return cfg_path


def test_load_valid_config(tmp_path: Path) -> None:
    cfg: config.BlogConfig = config.load_config(_write(tmp_path, VALID_CONFIG))
    assert cfg.site_title == "Test Blog"
    assert cfg.site_url == "https://test.example"
    assert cfg.posts_dir == Path("posts")
    assert cfg.build_dir == Path("build")
    assert cfg.languages == ["en", "fr"]
    assert cfg.reading_time_labels == {"en": "min read", "fr": "min de lecture"}
    assert cfg.back_labels == {"en": "Back", "fr": "Retour"}
    assert str(cfg.default_timezone) == "Europe/Brussels"
    assert cfg.default_publish_hour == 13
    assert cfg.theme_dir == Path("theme")
    assert cfg.template_file == Path("theme/template.html")
    assert cfg.style_file == Path("theme/style.css")


def test_load_missing_file(tmp_path: Path) -> None:
    with pytest.raises(config.ConfigError, match="not found"):
        config.load_config(tmp_path / "missing.yml")


def test_load_missing_section(tmp_path: Path) -> None:
    text: str = VALID_CONFIG.replace("general:", "general_oops:")
    with pytest.raises(config.ConfigError, match="Missing section 'general'"):
        config.load_config(_write(tmp_path, text))


def test_load_missing_field(tmp_path: Path) -> None:
    text: str = VALID_CONFIG.replace('  site_title: "Test Blog"\n', "")
    with pytest.raises(config.ConfigError, match="Missing field 'site_title'"):
        config.load_config(_write(tmp_path, text))


def test_load_missing_language_label(tmp_path: Path) -> None:
    text: str = VALID_CONFIG.replace('    fr: "min de lecture"\n', "")
    with pytest.raises(
        config.ConfigError, match="Missing label for language 'fr'"
    ):
        config.load_config(_write(tmp_path, text))


def test_load_missing_back_label(tmp_path: Path) -> None:
    text: str = VALID_CONFIG.replace('    fr: "Retour"\n', "")
    with pytest.raises(
        config.ConfigError, match="Missing label for language 'fr'"
    ):
        config.load_config(_write(tmp_path, text))


def test_load_invalid_timezone(tmp_path: Path) -> None:
    text: str = VALID_CONFIG.replace("Europe/Brussels", "Mars/Olympus")
    with pytest.raises(config.ConfigError, match="Unknown timezone"):
        config.load_config(_write(tmp_path, text))


def test_load_invalid_publish_hour(tmp_path: Path) -> None:
    text: str = VALID_CONFIG.replace("default_publish_hour: 13", "default_publish_hour: 42")
    with pytest.raises(config.ConfigError, match="between 0 and 23"):
        config.load_config(_write(tmp_path, text))


def test_load_empty_languages(tmp_path: Path) -> None:
    text: str = VALID_CONFIG.replace("codes: [en, fr]", "codes: []")
    with pytest.raises(config.ConfigError, match="non-empty list"):
        config.load_config(_write(tmp_path, text))


def test_load_invalid_yaml(tmp_path: Path) -> None:
    cfg_path: Path = tmp_path / "bad.yml"
    cfg_path.write_text("general: : :\n  - not valid")
    with pytest.raises(config.ConfigError, match="Could not parse YAML"):
        config.load_config(cfg_path)


def test_default_config_file_is_valid() -> None:
    """The shipped config/config.yml must load without errors."""
    project_root: Path = Path(__file__).resolve().parent.parent
    cfg: config.BlogConfig = config.load_config(project_root / "config" / "config.yml")
    assert cfg.languages == ["en", "fr", "nl"]
    assert cfg.site_title
