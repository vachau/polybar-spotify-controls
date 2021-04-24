#!/bin/python

import sys
import dbus
import argparse

MP2_INTERFACE = 'org.mpris.MediaPlayer2.Player'

def fix_string(string):
    # corrects encoding for the python version used
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')

def truncate(name, trunclen):
    if len(name) > trunclen:
        name = name[:trunclen]
        name += '...'
        if ('(' in name) and (')' not in name):
            name += ')'
    return name

def parse_commandline():
    # just looking for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--trunclen',
        type=int,
        metavar='length',
        help='specifies the maximum length of the printed string',
        default=35
    )
    parser.add_argument(
        '-f',
        '--format',
        type=str,
        metavar="'format'",
        help="specifies whether and how to display the song, the artist's name and the play-pause indicator",
        default=fix_string(u'{play_pause} {artist}: {song}'),
        dest='format'
    )
    parser.add_argument(
        '-p',
        '--playpause',
        type=str,
        metavar="'<playing>,<paused>'",
        help='set which unicode symbols to use for the status indicator',
        default=fix_string(u'\u25B6,\u23F8'), # first character is play, second is paused
        dest='play_pause'
    )
    parser.add_argument(
        '--font',
        type=str,
        metavar='font_id',
        help='the index of the font from your Polybar config to use for the main label',
        dest='font'
    )
    parser.add_argument(
        '--playpause-font',
        type=str,
        metavar='font_id',
        help='the index of the font from your Polybar config to use to display the play-pause indicator',
        dest='play_pause_font'
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help="if set, don't show any output when the current song is paused",
        dest='quiet',
    )
    parser.add_argument(
        '--action',
        help="playback action (don't use this in 'exec')",
        choices=["PlayPause", "Next", "Previous"],
        dest='player_action',
    )
    return parser.parse_args()


args = parse_commandline()

output = args.format
trunclen = args.trunclen
play_pause = args.play_pause
player_action = args.player_action

label_with_font = '%{{T{font}}}{label}%{{T-}}'
font = args.font
play_pause_font = args.play_pause_font

quiet = args.quiet

try:
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        'org.mpris.MediaPlayer2.spotify',
        '/org/mpris/MediaPlayer2'
    )

    if player_action is not None:
        spotify_player = dbus.Interface(spotify_bus, dbus_interface=MP2_INTERFACE)
        if player_action == 'Next':
            spotify_player.Next()
        elif player_action == 'PlayPause':
            spotify_player.PlayPause()
        elif player_action == 'Previous':
            spotify_player.Previous()
    else:

        spotify_properties = dbus.Interface(
            spotify_bus,
            'org.freedesktop.DBus.Properties'
        )

        metadata = spotify_properties.Get(MP2_INTERFACE, 'Metadata')
        status = spotify_properties.Get(MP2_INTERFACE, 'PlaybackStatus')

        # Handle play/pause label

        play_pause = play_pause.split(',')

        if status == 'Playing':
            play_pause = play_pause[0]
        elif status == 'Paused':
            play_pause = play_pause[1]
        else:
            play_pause = str()

        if play_pause_font:
            play_pause = label_with_font.format(font=play_pause_font, label=play_pause)

        # Handle main label

        artist = fix_string(metadata['xesam:artist'][0]) if metadata['xesam:artist'] else ''
        song = fix_string(metadata['xesam:title']) if metadata['xesam:title'] else ''
        album = fix_string(metadata['xesam:album']) if metadata['xesam:album'] else ''

        if (quiet and status == 'Paused') or (not artist and not song and not album):
            print('')
        else:
            if font:
                artist = label_with_font.format(font=font, label=artist)
                song = label_with_font.format(font=font, label=song)
                album = label_with_font.format(font=font, label=album)

            # Add 4 to trunclen to account for status symbol, spaces, and other padding characters
            print(truncate(output.format(artist=artist,
                                        song=song,
                                        play_pause=play_pause,
                                        album=album), trunclen + 4))

except Exception as e:
    if isinstance(e, dbus.exceptions.DBusException):
        print('')
    else:
        print(e)
