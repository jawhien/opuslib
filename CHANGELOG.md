# Changelog

## 3.0.5

- Updated bundled Windows `opus.dll` binaries to libopus 1.6.1.
- Fixed ctypes binary buffer handling for Opus packets and encoded payloads.
- Fixed high-level encoder default packet size to use the Opus packet limit.
- Added packet-loss concealment support with `Decoder.decode(None, ...)` and
  `Decoder.decode_float(None, ...)`.
- Removed incorrect high-level properties `Encoder.pitch` and
  `Decoder.lsb_depth`.
- Added packet helpers: `packet_get_nb_samples`, `packet_has_lbrr`, and
  `packet_parse`.
- Added Opus CTL constants and wrappers for bitrate maximum, expert frame
  duration, phase inversion, prediction, extension handling, and related
  Opus 1.6.x requests.
- Documented through tests that standard Opus encoder/decoder sample rates do
  not include 44100 Hz; callers should resample to a supported Opus rate.
