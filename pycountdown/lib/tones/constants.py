# pitches
PITCH_A4 = 440  # Hz
PITCH_C5 = 523  # Hz, approximate
PITCH_E5 = 659  # Hz, approximate
PITCH_G5 = 784  # Hz, approximate

# duration
EIGHTH_NOTE_DUR = 0.1  # sec

# alert sequence (freq_hz, dur_s, volume)
ALERT_SEQ = (
    (PITCH_A4, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_C5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_E5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_G5, 3*EIGHTH_NOTE_DUR, 0.5),
    (PITCH_G5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_E5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_C5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_A4, 3*EIGHTH_NOTE_DUR, 0.5),
    (PITCH_A4, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_C5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_E5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_G5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_E5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_C5, EIGHTH_NOTE_DUR, 0.5),
    (PITCH_A4, 3*EIGHTH_NOTE_DUR, 0.5),
)
