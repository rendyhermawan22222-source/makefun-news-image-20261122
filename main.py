"""make.fun news-image-20261122 entry: writes the front page to /output/entry.png.

The finished PNG is committed as base64 text (entry.png.b64), because the page was
composed ahead of time by build/compose.py. This program only decodes it, so every
run produces byte-identical output and needs no network.
"""
import base64
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SHA256 = "ecefe61b909ee141b34dc3dd3d4804db07208ee20b37db87264587aa28db326e"


def main() -> None:
    with open(os.path.join(HERE, "entry.png.b64"), "r", encoding="ascii") as f:
        data = base64.b64decode("".join(f.read().split()))
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise SystemExit("entry.png.b64 is corrupted")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
