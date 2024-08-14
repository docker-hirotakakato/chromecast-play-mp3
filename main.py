#!/usr/bin/python

import os

DEFAULT_VOLUME_SCALE = os.getenv('DEFAULT_VOLUME_SCALE', 1.25)

from flask import Flask, abort, request, Response
import pychromecast, time

app = Flask(__name__)

@app.route('/')
def play_mp3():
    host = request.args.get('host')

    try:
        cc = pychromecast.get_chromecasts(known_hosts=[host])[0][0]
        cc.wait()

    except:
        abort(500)

    mp3 = request.args.get('mp3')

    if mp3 is None:
        abort(500)

    volume_scale = float(request.args.get('volume_scale', DEFAULT_VOLUME_SCALE))

    volume = cc.status.volume_level

    try:
        cc.set_volume(volume * volume_scale)

        mc = cc.media_controller
        mc.play_media(mp3, 'audio/mpeg')
        mc.block_until_active()

        time.sleep(1)

        while mc.status.player_is_playing:
            time.sleep(1)

    finally:
        cc.set_volume(volume)

        return Response()

if __name__ == '__main__':
    app.run('0.0.0.0', 80, True)
