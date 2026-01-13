from PySide2.QtCore import QBuffer, QIODevice, QByteArray
from PySide2.QtMultimedia import QAudioOutput, QAudioFormat, QAudio

from ..lib.tones.constants import ALERT_SEQ
from ..lib.tones.gen import generate_tone, BITRATE
from ..app import PyCountdownApp


class AudioPlayer:
    def __init__(self, audio_data: bytes, sample_rate_hz: int):
        audio_format = QAudioFormat()
        audio_format.setSampleRate(sample_rate_hz)
        audio_format.setChannelCount(1)
        audio_format.setSampleSize(BITRATE)
        audio_format.setCodec("audio/pcm")
        audio_format.setByteOrder(QAudioFormat.LittleEndian)
        audio_format.setSampleType(QAudioFormat.SignedInt)

        # Store as instance attributes to prevent garbage collection
        self.byte_array = QByteArray(audio_data)  # this needs to stay alive
        self.buffer = QBuffer(self.byte_array)  # this is a pointer to buffer
        self.buffer.open(QIODevice.ReadOnly)
        self.audio_output = QAudioOutput(audio_format)

        # Connect to state changes to clean up when playback finishes
        self.audio_output.stateChanged.connect(self._on_state_changed)

    def start(self):
        self.audio_output.start(self.buffer)

    def stop(self):
        self.audio_output.stop()

    def _on_state_changed(self, state):
        "Remove from active set when playback finishes."
        if state == QAudio.IdleState:
            _active_players.discard(self)


# Keep references to active audio players to prevent garbage collection
_active_players: set[AudioPlayer] = set()


def play_alert_tones(sample_rate_hz: int = 48000):
    "Play alert tone sequence. Uses main thread event loop for playback."
    # Pre-generate all tone data and concatenate
    user_vol = PyCountdownApp.get('local.alert_volume_pct', 50)/100
    data = b''.join(generate_tone(freq_hz, dur_s, sample_rate_hz, user_vol*vol)
                    for freq_hz, dur_s, vol in ALERT_SEQ)

    # Create player and keep reference alive until playback completes
    player = AudioPlayer(data, sample_rate_hz)
    _active_players.add(player)
    player.start()


def stop_all_alerts():
    "Stop all currently playing alert tones."
    for player in _active_players:
        player.stop()
