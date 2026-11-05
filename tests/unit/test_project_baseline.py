from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_architecture_specification_exists():
    path = PROJECT_ROOT / "docs/AI-A03-Architecture-Specification.md"
    assert path.is_file()


def test_source_configuration():
    path = PROJECT_ROOT / "config/sources.yaml"
    config = yaml.safe_load(path.read_text())

    assert config["version"] == 1
    assert len(config["sources"]) == 2

    names = {source["name"] for source in config["sources"]}
    assert names == {"AI-A01", "AI-A02"}


def test_migrations_exist():
    path = PROJECT_ROOT / "db/migrations/001_initial_schema.sql"
    assert path.is_file()


def test_architecture_diagrams_exist():
    diagrams = list((PROJECT_ROOT / "diagrams").glob("*.mmd"))
    assert len(diagrams) == 4
