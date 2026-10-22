"""Preflight checks for publishing the LT-Nodes ComfyUI package."""

import ast
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
NODE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"Registry preflight failed: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    metadata_file = ROOT / "pyproject.toml"
    if not metadata_file.is_file():
        fail("pyproject.toml is missing")

    with metadata_file.open("rb") as handle:
        config = tomllib.load(handle)

    project = config.get("project", {})
    comfy = config.get("tool", {}).get("comfy", {})
    name = project.get("name", "")
    version = project.get("version", "")
    publisher = comfy.get("PublisherId", "")
    repository = project.get("urls", {}).get("Repository", "")

    if not isinstance(name, str) or not NODE_ID.fullmatch(name) or len(name) >= 100:
        fail("project.name must be a valid, unique Registry node ID")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        fail("project.version must use X.Y.Z semantic versioning")
    if not isinstance(publisher, str) or not publisher.strip() or "REPLACE" in publisher.upper():
        fail("set tool.comfy.PublisherId to your real Comfy Registry publisher ID")
    if repository != "https://github.com/Latent-Talent/LT-Nodes":
        fail("project.urls.Repository must link to this GitHub repository")

    entry_file = ROOT / "__init__.py"
    if not entry_file.is_file():
        fail("ComfyUI entry point __init__.py is missing")
    code = entry_file.read_text(encoding="utf-8")
    try:
        tree = ast.parse(code, filename=str(entry_file))
    except SyntaxError as exc:
        fail(f"invalid __init__.py: {exc}")

    # The initial scaffold must not be published as an empty node pack.
    if not any(
        isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Import, ast.ImportFrom))
        or (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "NODE_CLASS_MAPPINGS"
        )
        or (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Dict)
            and bool(node.value.keys)
        )
        for node in ast.walk(tree)
    ):
        fail("no node implementation or mappings found; add your custom nodes before publishing")

    print(f"Registry preflight passed: {name} v{version} (publisher: {publisher})")


if __name__ == "__main__":
    main()
