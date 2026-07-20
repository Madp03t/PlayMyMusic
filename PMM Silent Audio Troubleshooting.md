## PMM Silent Audio Troubleshooting

**Symptom:**

* PMM appears to be playing (seek bar moves, track changes), but there is no sound.

**First check:**

```bash
pavucontrol
```

* Open the **Playback** tab.
* If the PMM/mpv stream is muted, unmute it.
* If that restores audio, note what happened immediately before the issue.

**If it happens again:**

While PMM is still silent, run:

```bash
pactl list sink-inputs
```

Save the output so it can be reviewed later.

**Notes:**

* Issue is intermittent.
* Suspected to be related to PipeWire/mpv.
* Do not modify PMM until the issue can be reproduced consistently.


## Observed again

### Steps:

* Watch a YouTube video in Waterfox.
* Pause the video (browser remains open).
* Launch Play.My.Music.
* PMM appears to play normally, but there is no audio.
* Open pavucontrol → Playback.
* The PMM/mpv stream is muted.
* Unmuting the stream immediately restores audio.

## Current observations

Playback itself is unaffected (seek bar advances, track changes work).
The mute occurs at the PipeWire application stream level.
The issue has now happened multiple times, suggesting it is reproducible under some conditions.

Next coding session
Determine whether:

mpv is creating its PipeWire stream muted.
PipeWire/WirePlumber is restoring a previously muted state for mpv.
PMM can explicitly request an unmuted audio stream when playback begins.