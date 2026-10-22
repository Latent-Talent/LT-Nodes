# LT-Nodes

A collection of custom nodes and utilities for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), developed under Latent Talent.

LT-Nodes is organized as **one installable ComfyUI node pack**. Its custom nodes may cover image and video generation, local LLMs, model integration, performance optimizations, and workflow automation. Nodes added to this repository will share a Registry listing and package version.

## Status

**Scaffold only — no functional nodes are included or published yet.**
The Comfy Registry publishing workflow and package metadata are in place, but a real node implementation, the correct Registry Publisher ID, and a publishing token must be added before the first release.

## Repository layout

| Path | Purpose |
| --- | --- |
| `__init__.py` | ComfyUI entry point; register node classes here |
| `pyproject.toml` | Package metadata, Registry publisher, and version |
| `.comfyignore` | Excludes development-only files from Registry packages |
| `.github/workflows/publish-registry.yml` | Automated Registry publication |
| `scripts/validate_registry.py` | Pre-publication checks |
| `docs/REGISTRY_PUBLISHING.md` | One-time configuration and release steps |

## Installation

After nodes have been added, developers can clone the repository into the ComfyUI `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Latent-Talent/LT-Nodes.git
```

Install any dependencies required by the individual node implementations, then restart ComfyUI. Registry installation via ComfyUI-Manager will become available after a successful, approved publication.

## Publishing updates

The [publishing guide](docs/REGISTRY_PUBLISHING.md) explains how to create a Comfy Registry publisher, set the `REGISTRY_ACCESS_TOKEN` GitHub Actions secret, register the first version, and publish updates.

Once configured, bump the `version` field in `pyproject.toml` and push to `main`; GitHub Actions publishes new versions automatically. The workflow can also be started manually from the Actions tab.

Published Registry versions cannot be overwritten.
