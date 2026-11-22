# CardboardXR apps repository

This is a catalog the CardboardXR App Store reads. Put it on GitHub as a **public** repository (the store
fetches files from `raw.githubusercontent.com` without signing in, so a private one can't be read), then
type `your-name/this-repo` into the store's Settings.

```
index.json            the catalog: generated, do not edit by hand
apps/<id>/app.json    each app's manifest
apps/<id>/main.lua    its code (and any other .lua files it requires)
tools/build_index.py  makes index.json from apps/
```

To add or change an app:

1. Edit or add a folder under `apps/` (see the API reference, `LUA_API.md`).
2. `python3 tools/build_index.py` (it checks the rules the store enforces and tells you what's wrong).
3. Commit `index.json` and the app together, and push.
4. In the store: Store tab, refresh, open the app, Install or Update. GitHub's raw files are cached for a few
   minutes; the store asks around that, so a change shows at once.

`.github/workflows/check-index.yml` fails a push whose `index.json` is out of date with `apps/`.

The three apps here are examples: Hello Cube (the smallest), Orb Pop (several files, saved score) and
Metronome (panels, sliders, timers, sound).
