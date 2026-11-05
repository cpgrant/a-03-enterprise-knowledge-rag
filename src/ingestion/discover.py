from __future__ import annotations

import fnmatch
import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "sources.yaml"


@dataclass(frozen=True)
class SourceDocument:
    source_name: str
    repository: Path
    file_path: str
    git_commit: str
    content_hash: str
    content: str
    document_type: str


def git_output(repository: Path, *arguments: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), *arguments],
        text=True,
    ).strip()


def discover_documents() -> list[SourceDocument]:
    config = yaml.safe_load(CONFIG_PATH.read_text())

    ingestion = config["ingestion"]
    allowed = set(ingestion["include_extensions"])
    excluded_directories = set(ingestion["exclude_directories"])
    excluded_patterns = ingestion["exclude_patterns"]

    documents = []

    for source in config["sources"]:
        if not source.get("enabled", True):
            continue

        repository = (
            PROJECT_ROOT / source["repository_path"]
        ).resolve(strict=True)

        commit = git_output(repository, "rev-parse", "HEAD")

        tracked_files = subprocess.check_output(
            ["git", "-C", str(repository), "ls-files", "-z"]
        ).split(b"\0")

        for raw_path in tracked_files:
            if not raw_path:
                continue

            try:
                file_path = raw_path.decode("utf-8")
            except UnicodeDecodeError:
                continue

            relative = Path(file_path)

            if relative.is_absolute() or ".." in relative.parts:
                continue

            if relative.suffix.lower() not in allowed:
                continue

            if any(
                part in excluded_directories
                for part in relative.parts
            ):
                continue

            if any(
                fnmatch.fnmatch(relative.name, pattern)
                for pattern in excluded_patterns
            ):
                continue

            resolved = (repository / relative).resolve()

            if not resolved.is_relative_to(repository):
                continue

            if not resolved.is_file() or resolved.is_symlink():
                continue

            if resolved.stat().st_size > 1_000_000:
                continue

            try:
                content = resolved.read_text(encoding="utf-8")
            except (UnicodeError, OSError):
                continue

            if not content.strip():
                continue

            documents.append(
                SourceDocument(
                    source_name=source["name"],
                    repository=repository,
                    file_path=file_path,
                    git_commit=commit,
                    content_hash=hashlib.sha256(
                        content.encode("utf-8")
                    ).hexdigest(),
                    content=content,
                    document_type=relative.suffix.lower().lstrip("."),
                )
            )

    return documents
