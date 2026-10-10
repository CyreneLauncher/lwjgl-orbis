#!/usr/bin/env python3
"""Download the official LWJGL Java JARs pinned in lwjgl-sources.lock.json, checking each SHA-1.

JARs go to OUTPUT/<release>/<name>, the layout the recipes' --jars options expect.
"""
import argparse
import hashlib
from pathlib import Path
import time
import urllib.error
import urllib.request

import lwjgl_sources

RELEASES = ('3.2.2', '3.3.3', '3.4.1', '3.4.3')


def fetch(url, path, expected, attempts=6):
    if path.is_file() and hashlib.sha1(path.read_bytes()).hexdigest() == expected:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + '.partial')
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(url) as response:
                partial.write_bytes(response.read())
            break
        except urllib.error.HTTPError as error:
            # Maven Central answers bursts with 429; anything else is final.
            if error.code != 429 or attempt == attempts - 1:
                raise
            time.sleep(5 * 2 ** attempt)
    digest = hashlib.sha1(partial.read_bytes()).hexdigest()
    if digest != expected:
        partial.unlink()
        raise SystemExit(f'{url} SHA-1 {digest} is not the pinned {expected}')
    partial.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    count = 0
    for key, table in lwjgl_sources.LOCK.items():
        if not key.startswith('java_artifacts'):
            continue
        for name, sha1 in table.items():
            if not name.endswith('.jar'):
                continue  # each table also carries a description
            release = next(r for r in RELEASES if f'-{r}' in name)
            artifact = name.split(f'-{release}')[0]
            fetch(f'https://repo.maven.apache.org/maven2/org/lwjgl/{artifact}/{release}/{name}',
                  args.output / release / name, sha1)
            count += 1
    print(f'{count} official LWJGL JARs in {args.output}')


if __name__ == '__main__':
    main()
