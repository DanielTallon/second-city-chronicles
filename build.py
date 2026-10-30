#!/usr/bin/env python3
"""Build the public, read-only Second City Chronicles site.

Inputs, all under source/ (exported from the claude.ai map):
  map.html            the map page as published on claude.ai, without the publish wrapper
  data/places/*.json  your own locations, one file per location
  data/notes/*.json   your notes and photos on sourcebook sites, one file per site
  photos/<id>.<ext>   the photos those files point to by id

Output: site/index.html and site/photos/, ready for GitHub Pages.
"""
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "source"
OUT = ROOT / "site"

DESCRIPTION = ("A story map of Chicago in the Chronicle of Darkness: "
               "haunts, havens and hunting grounds laid over the real city.")


def load_docs(collection):
    """Read one exported collection as {doc_id: fields}."""
    docs = {}
    for f in sorted((SRC / "data" / collection).glob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        # The export wraps each document as {"id", "data", "version", ...}; plain field objects work too.
        docs[f.stem] = doc["data"] if isinstance(doc.get("data"), dict) else doc
    return docs


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "photos").mkdir(parents=True)

    photos = {}
    for f in sorted((SRC / "photos").iterdir()):
        if f.is_file() and not f.name.startswith("."):
            shutil.copy2(f, OUT / "photos" / f.name)
            photos[f.stem] = "photos/" + f.name

    places, notes = load_docs("places"), load_docs("notes")
    wanted = {p for d in [*places.values(), *notes.values()] for p in d.get("photos", [])}
    missing = sorted(wanted - photos.keys())
    if missing:
        raise SystemExit(f"Missing photo files in source/photos: {', '.join(missing)}")

    page = (SRC / "map.html").read_text(encoding="utf-8")
    # Everything before the map stage is head material (title, fonts, styles).
    split = page.index('<div class="stage">')
    head, body = page[:split], page[split:]

    # "</" is escaped so a note containing "</script>" can't end the data block early.
    data = json.dumps({"places": places, "notes": notes, "photos": photos},
                      ensure_ascii=False).replace("</", "<\\/")

    (OUT / "index.html").write_text(
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
        f"<meta name=\"description\" content=\"{DESCRIPTION}\">\n"
        "<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);"
        "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}"
        "[hidden]{display:none!important}</style>\n"
        f"{head}"
        f"<script>window.SITE_DATA = {data};</script>\n"
        "</head>\n<body>\n"
        f"{body}"
        "</body>\n</html>\n",
        encoding="utf-8",
    )
    print(f"Built site/ with {len(places)} of your locations, "
          f"notes on {len(notes)} sourcebook sites and {len(photos)} photos.")


if __name__ == "__main__":
    main()
