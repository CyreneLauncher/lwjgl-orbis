"""Pinned LWJGL/dyncall archives and official Java JARs from lwjgl-sources.lock.json."""
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUPPORT = Path(os.environ.get('ORBIS_RUNTIME_SUPPORT') or HERE.parent / 'orbis-runtime-support').resolve()
sys.path.insert(0, str(SUPPORT))
import pinned_archive  # noqa: E402

LOCK = json.loads((HERE / 'lwjgl-sources.lock.json').read_text())
extract = pinned_archive.extract


def archive(name, downloads, fetch=False):
    """Returns the verified archive for LOCK[name], downloading it only when fetch is set."""
    return pinned_archive.archive(LOCK[name], downloads, fetch)


def java_artifact(jars, filename):
    """An official LWJGL Java JAR, verified against its pinned SHA-1."""
    path = Path(jars) / filename
    # Each LWJGL release has its own table; file names carry the version, so they do not collide.
    tables = [entry for key, entry in LOCK.items() if key.startswith('java_artifacts')]
    expected = next((table[filename] for table in tables if filename in table), None)
    if expected is None:
        raise SystemExit(f'{filename} is not a pinned LWJGL Java artifact')
    if not path.is_file():
        raise SystemExit(f'missing official {filename} under {jars}')
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != expected:
        raise SystemExit(f'{path} SHA-1 {digest} is not the audited {expected}')
    return path
