# Chromecast MQTT-smarthome connector

Fork of [dersimn](https://github.com/dersimn)'s [chromecast-mqtt-smarthome-connector](https://github.com/dersimn/chromecast-mqtt-smarthome-connector), but with some configuration tweaks.

## Usage

Control behaviour by defining ENV variables `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER`, `MQTT_PASSWORD`, `MQTT_CAFILE`.

    git clone
    pip3 install -r requirements.txt
    MQTT_HOST=10.1.1.50 python3 connector.py

Set the log level with the `LOG_LEVEL` environment variable ([possible values](https://docs.python.org/3/library/logging.html#levels)).

All environment variables may also be set with a `_FILE` suffix to support [Docker secrets](https://docs.docker.com/engine/swarm/secrets/) in [Swarm mode](https://docs.docker.com/engine/swarm/).

## Docker

    docker run -d --net=host -e "MQTT_HOST=10.1.1.100" nielsrowinbik/chromecast-mqtt-smarthome-connector

## Discovery and control

Using MQTT you can find the following topics. `FRIENDLY_NAME` is the name used to connect
to each Chromecast.

    chromecast/maintenance/_bridge/online -> bool

    chromecast/maintenance/FRIENDLY_NAME/online -> bool
    chromecast/maintenance/FRIENDLY_NAME/connection_status -> string
    chromecast/maintenance/FRIENDLY_NAME/cast_type -> string

    chromecast/status/FRIENDLY_NAME/current_app -> string

    chromecast/status/FRIENDLY_NAME/volume -> JSON
    chromecast/set   /FRIENDLY_NAME/volume -> float
    chromecast/set   /FRIENDLY_NAME/volume/muted -> bool

    chromecast/status/FRIENDLY_NAME/player -> JSON
    chromecast/set   /FRIENDLY_NAME/player -> string
    chromecast/set   /FRIENDLY_NAME/player/position -> int

    chromecast/status/FRIENDLY_NAME/media -> JSON

Change volume using values from `0` to `1.0`:

- Publish e.g. `1.0` to `chromecast/set/FRIENDLY_NAME/volume`

Change mute state: publish `false` or `true` to `chromecast/set/FRIENDLY_NAME/volume/muted`.

Play something: Publish a json array with two elements (content url and content type) to
`chromecast/set/FRIENDLY_NAME/player`, e.g. `["http://your.stream.url.here", "audio/mpeg"]`.
You can also just publish a URL to `player_state` (just as string, not as json array, e.g.
`http://your.stream.url.here`), the application then tries to guess the required MIME type.

For other player controls, simply publish e.g. `RESUME`, `PAUSE`, `STOP`, `SKIP` or `REWIND` to
`chromecast/set/FRIENDLY_NAME/player`. Attention: This is case-sensitive!

## Development / Debug

### docker build

    docker build -t chromecast-mqtt-smarthome-connector .

Cross-build (for Raspberry Pi):

    docker buildx create --name mybuilder
    docker buildx use mybuilder
    docker buildx build \
        --platform linux/amd64,linux/arm/v7 \
        -t dersimn/chromecast-mqtt-smarthome-connector \
        -t dersimn/chromecast-mqtt-smarthome-connector:1 \
        -t dersimn/chromecast-mqtt-smarthome-connector:1.3 \
        -t dersimn/chromecast-mqtt-smarthome-connector:1.3.2 \
        --push .
