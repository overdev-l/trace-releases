# Trace builds and releases

This repository contains build configuration and downloadable Trace desktop applications. **The application source remains private.** GitHub's automatic “Source code” archives contain only the files in this CI repository.

- [Download releases](https://github.com/overdev-l/trace-releases/releases)
- [Build workflow](https://github.com/overdev-l/trace-releases/actions/workflows/build.yml)
- Platforms: macOS Apple Silicon (arm64), Windows x64.

Maintainers can run **Build Trace** on `main`, select an exact source commit (or `main`), and choose:

| Mode | Result |
| --- | --- |
| `build` | CI artifacts only, retained for 7 days |
| `preview` | Unsigned prerelease installers; never the stable updater channel |
| `stable` | Signed release, including macOS notarization; requires signing secrets |

The source checkout uses a dedicated read-only deploy key stored as `TRACE_SOURCE_DEPLOY_KEY`. No personal GitHub token is copied into this repository. Builds do not run for external pull requests. Private build logs, source archives, and source maps are not published.

Both platforms must build successfully before a draft release is created. Only validated installers, blockmaps, and checksums are uploaded. Stable update manifests are uploaded last; the draft becomes visible only after the complete asset set is verified. Published releases are immutable.

Stable signing secrets: `CSC_LINK`, `CSC_KEY_PASSWORD`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`, `WIN_CSC_LINK`, `WIN_CSC_KEY_PASSWORD`. A preview is not a signed automatic-update baseline. Only grant repository write access to trusted release maintainers.

Failed build logs are encrypted with RSA-OAEP/SHA-256 and AES-256-GCM before upload (one-day retention). Only the maintainer holding the matching private key can read diagnostics. Plaintext logs never leave the runner.
