# Second City Chronicles

A story map of Chicago in the Chronicle of Darkness: sourcebook haunts, havens and hunting grounds laid over the real city, plus my own locations, notes and photos.

**Live site:** <https://danieltallon.github.io/second-city-chronicles/>

The site is a read-only snapshot. Editing happens on the private map on claude.ai, and Claude exports it here.

## How it fits together

```
source/
├── map.html            the map page, exported from claude.ai
├── data/places/        my own locations, one JSON file each
├── data/notes/         my notes and photos on sourcebook sites, one JSON file each
└── photos/             the photos those files point to
build.py                turns source/ into site/ (no dependencies beyond Python 3)
.github/workflows/      builds and deploys to GitHub Pages on every push to main
```

`site/` is generated, so it isn't committed.

## Updating the site

1. Edit on the claude.ai map: add locations, notes and photos.
2. Ask Claude to export the map into `source/` here.
3. Check the result locally:

   ```bash
   python3 build.py && python3 -m http.server -d site 8000
   ```

   Then open <http://localhost:8000>.
4. Commit and push. The workflow publishes it within a minute or two.

## Credits

Sites and icons come from the [Chronicle of Darkness Sites](https://www.google.com/maps/d/viewer?mid=1ADtXovdxb5zVAMieQDfRXUw5m_9EigPj) community map. Streets © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL). Neighborhood boundaries come from the City of Chicago Data Portal. Chronicle of Darkness is a trademark of Paradox Interactive; this is an unofficial fan project.
