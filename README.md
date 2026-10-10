# lwjgl-orbis

The four LWJGL profiles (3.2.2, 3.3.3, 3.4.1, 3.4.3) for Orbis: native modules, the Java
adapter (facade) JARs, optional modules, FreeType, SPIR-V tools, VMA and the graphics
platform PRX. See PORT-PROVENANCE.json for exact origins. Upstream archives and official
Java JARs are hash-pinned in `lwjgl-sources.lock.json`.

| Recipe | Builds | Needs besides the SDK |
| --- | --- | --- |
| `build_lwjgl_natives.py` | `liblwjgl*` | orbis-runtime-support |
| `build_lwjgl_optional.py` | stand-in OpenAL/TinyFD modules for 3.2.2 | orbis-runtime-support, official JARs |
| `build_freetype.py` | `libfreetype` | orbis-runtime-support |
| `build_spirv.py` | `libshaderc`, `libspirv-cross` | orbis-runtime-support, orbis-compat source |
| `build_vma.py` | `liblwjgl_vma` | orbis-runtime-support, orbis-compat source, Mesa's Vulkan headers |
| `build_platform_prx.py` | `liborbis_lwjgl_platform` | orbis-runtime-support, a Mesa build, orbis-compat build, orbis-porting-kit, mesa-orbis |
| `build_lwjgl_facade.py` | `orbis-lwjgl-<release>-adapter.jar` | official JARs, the launcher's `NativeInput.java` (`--native-input`) |

Sibling checkouts are found next to this one (`orbis-runtime-support`, `mesa-orbis`) or through
`ORBIS_RUNTIME_SUPPORT` and `ORBIS_MESA_PORT`. `ORBIS_BUILD_ROOT` (default `build/`) holds
`downloads/`, prepared sources (`sources/orbis-compat`, `sources/mesa`,
`sources/orbis-porting-kit`), the Mesa build (`target/`) and outputs. The launcher sets it to
its `graphics-probe/build`.

LWJGL loads OpenAL and SDL at run time and does not build against them; those ports live in
openal-soft-orbis and sdl-orbis. The platform PRX is the only module that links another
library: it statically links Mesa's EGL, radeonsi and RADV archives.

Integration tests and package assembly remain in orbis-launcher.

## Releases

`.github/workflows/release.yml` builds this port on GitHub-hosted Ubuntu with the SDKs and the
dependencies pinned in `dependencies.lock.json`, and with `publish` checked releases
`<tag_prefix>-<commit>` holding the archive `release.json` describes. Cyrene Launcher pins that
release by SHA-256. The workflow needs a `CYRENE_RELEASES_TOKEN` secret that can read the private
CyreneLauncher repositories.

The LWJGL release also needs the Mesa release pinned in `dependencies.lock.json` (`revision` and
`sha256`); `fetch_java_artifacts.py` downloads the official JARs from this repository's lock.
