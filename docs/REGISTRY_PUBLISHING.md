# Comfy Registry publishing

This repository is configured as **one ComfyUI custom-node pack** named `lt-nodes`.
Individual node classes can live in separate modules but share one Registry
listing and version. Publishing each module independently would require a
separate package manifest and publishing workflow.

## One-time setup

1. Sign in at https://registry.comfy.org, create a **publisher**, and copy its exact Publisher ID (shown after `@` on your publisher profile).
2. Replace `REPLACE_WITH_REGISTRY_PUBLISHER_ID` in the root `pyproject.toml` with that exact ID. This is not automatically your GitHub username.
3. Create a Registry **publishing API key** for that publisher.
4. In GitHub, open **Settings → Secrets and variables → Actions → New repository secret**, name it `REGISTRY_ACCESS_TOKEN`, and paste the API key as the value. **Never commit or paste the key into source files.**
5. Add your real ComfyUI node code to the repository and expose its classes in the root `__init__.py` through `NODE_CLASS_MAPPINGS` (and optionally `NODE_DISPLAY_NAME_MAPPINGS`). The current mappings are empty placeholders.
6. Update project dependencies in `pyproject.toml` and/or `requirements.txt` as required by the actual node code. Choose and include a LICENSE if you intend to grant reuse rights.

## First publication

The workflow `.github/workflows/publish-registry.yml` can be run manually
from **Actions → Publish to Comfy Registry → Run workflow** on `main`.
It also runs after a new version is committed in `pyproject.toml` on `main`.

The workflow validates required Registry metadata and checks that the
initial empty node scaffold has been replaced before using the secret.
The first successful publication registers the pack on the Registry,
subject to Registry review.

## Publishing updates

1. Make changes to node code and documentation.
2. Change `[project].version` in `pyproject.toml` to a **new**, three-part
   semantic version, e.g. `0.1.0` → `0.1.1` (bug fix), `0.2.0` (new features), or `1.0.0` (stable major release).
3. Push the version bump to `main`. The workflow checks that the **version
   changed** and publishes the declared new version. Edits to other
   metadata without a version change do not republish an existing version.
4. Review the workflow run and verify the release in https://registry.comfy.org.

**Registry versions cannot be overwritten.** Every publication needs a
previously unused version. If a release needs correction, bump the version.

GitHub Actions needs to be enabled for this repository. Workflow execution,
Registry authentication, ownership, and Registry review are outside the
source-code setup and must be completed through your accounts.

Official references:
- https://docs.comfy.org/registry/publishing
- https://docs.comfy.org/registry/specifications
- https://github.com/Comfy-Org/publish-node-action
