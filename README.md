# polybar-spotify-controls

This is a module that shows the current song playing and its primary artist on Spotify, with a Spotify-green underline, for people that don't want to set up mpd. If Spotify is not active, nothing is shown. If the song name is longer than `trunclen` characers (default 25), it is truncated and `...` is appended. If the song is truncated and contains a single opening parenthesis, the closing paranethsis is appended as well.

This fork adds playback controls, which can be bound to mouse click actions. 

### Dependencies
- Python (2.x or 3.x)
- Python `dbus` module

[![sample screenshot](https://i.imgur.com/kEluTSq.png)](https://i.imgur.com/kEluTSq.png)

### Settings
``` ini
[module/spotify]
type = custom/script
interval = 1
format-prefix = " "
format = <label>
exec = python /path/to/spotify_status.py -f '{artist}: {song}'
format-underline = #1db954
click-left = python /path/to/spotify_status.py --action PlayPause
click-right = python /path/to/spotify_status.py --action Next
click-middle = python /path/to/spotify_status.py --action Previous
```

#### Optional arguments

##### Playback controls

`--action action` will send the specified playback action to the Spotify application. This does not print any output and is meant to be used with the `click-[button]=` Polybar options.

Availible `action` values:

- `PlayPause`: Toggle play and pause
- `Next`: Skip song
- `Previous`: Restart the current song / Go to the previous song

##### Truncate

`-t length` or `--trunclen length` truncates the printed output to the specified `length`. Defaults to 35

Example:

``` ini
exec = python /path/to/spotify/script -t 42
```

##### Format

`-f format` or `--format format` specifies the output format. Defaults to `{play_pause}{artist}: {song}`

Fields:

- `{play_pause}`: Playback status indicator
- `{song}`: Song title
- `{artist}`: Artist name
- `{album}`: Album name

Example:

``` ini
exec = python /path/to/spotify/script -f '{play_pause} {song} - {artist} - {album}'
```

This would output "▶ Lone Digger - Caravan Palace - <I°_°I>" in your polybar, instead of what is shown in the screenshot.

##### Status indicator

`-p '<playing>,<paused>'` or `--playpause '<playing>,<paused>'` specifies the comma-separated play and pause symbol characters.

Example:

``` ini
exec = python /path/to/spotify/script -p '▶,⏸'
```

##### Fonts

`--font font_id` specifies the font ID from your Polybar config for displaying the `{song}`, `{artist}`, and `{album}` fields.

Example:
```ini
exec = python /path/to/spotify/script --font=1
```

`--playpause-font font_id` specifies the font ID from your Polybar config for displaying the `{play_pause}` field. Useful for fonts that don't support the playback Unicode symbols.

Example:
``` ini
exec = python /path/to/spotify/script -p '▶,⏸' --playpause-font=2
```

##### Quiet

`-q` or `--quiet` disables printing any output when playback is paused.

Example:
```ini
exec = python /path/to/spotify/script -q
```
