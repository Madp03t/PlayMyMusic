
# New Music App Concept

A lightweight, local-first music player focused on simplicity, album art, and an always-current music library.

## Core Philosophy

The Music folder is the source of truth.

The app should reflect whatever music currently exists inside the selected Music folder. No stale playlists, no removed tracks lingering in the library, and no manual rebuilding required.

The goal is simple:

Open the app, hit Play or Shuffle, and listen to whatever music is currently inside the Music folder.

## Intended Workflow

* User selects a Music folder.
* App scans the folder and all subfolders on launch.
* Tracks currently inside the folder become the playable library.
* Added music appears automatically after re-scan/startup.
* Removed music disappears automatically.
* Playback is based on the current folder contents, not static playlists.

## Playback Features

* Normal playback
* Shuffle playback
* Play/Pause
* Next/Previous track
* Seek/progress bar
* Volume control

## Metadata Philosophy

All metadata is local only.

The app reads:

* Artist
* Title
* Album
* Embedded album art

directly from the MP3 file tags.

No internet lookups.
No cloud metadata.
No streaming services.

## Supported Formats

Primary focus:

* MP3

Possible future support:

* FLAC
* WAV
* M4A
* OGG

But MP3 support is the priority.

## Interface Philosophy

Minimal, clean, art-focused.

The app should feel calm and visually pleasing instead of crowded or overly technical.

### Main Window

* Large album art display
* Artist/title/album text
* Playback controls
* Progress bar
* Optional smooth audio visualizer/spectrum analyzer
* Dark theme preferred

### Mini Player Mode

Compact version with:

* Album art
* Track info
* Basic controls
* Optional always-on-top mode

### Art-Focused Listening Mode

A larger, immersive view designed for appreciating album art while listening.

Not intended as a cluttered fullscreen dashboard.

Could include:

* Large centered album art
* Dark background
* Smooth visualizer
* Minimal controls
* Ambient aesthetic

## Design Boundaries

The app should NOT become bloated.

No:

* streaming
* accounts
* subscriptions
* social features
* recommendations
* podcasts
* telemetry
* online syncing
* internet metadata scraping

The app is intended to be:
local, focused, lightweight, and personal.

## Technical Direction (Initial Idea)

Potential stack:

* Python
* PyQt or PySide for GUI
* mpv backend for audio playback

Development philosophy:
start simple, then expand carefully.

Version 1 goal:
a stable local music player that respects the user’s Music folder and makes listening enjoyable again.
