#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes  # type: ignore
import unittest

import opuslib


class CtlExtensionsTest(unittest.TestCase):

    def test_bitrate_max_uses_codec_maximum(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)

        encoder.bitrate = opuslib.BITRATE_MAX

        self.assertEqual(1500000, encoder.bitrate)

    def test_encoder_decorator_properties_roundtrip(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)

        encoder.phase_inversion_disabled = 1
        self.assertEqual(1, encoder.phase_inversion_disabled)
        encoder.phase_inversion_disabled = 0
        self.assertEqual(0, encoder.phase_inversion_disabled)

        encoder.expert_frame_duration = opuslib.FRAMESIZE_20_MS
        self.assertEqual(
            opuslib.FRAMESIZE_20_MS,
            encoder.expert_frame_duration
        )

        encoder.prediction_disabled = 1
        self.assertEqual(1, encoder.prediction_disabled)
        encoder.prediction_disabled = 0
        self.assertEqual(0, encoder.prediction_disabled)

    def test_encoder_optional_ctl_properties_report_unimplemented(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)

        try:
            encoder.dred_duration = 0
        except opuslib.OpusError as exc:
            self.assertEqual(opuslib.UNIMPLEMENTED, exc.code)
        else:
            self.assertEqual(0, encoder.dred_duration)

        try:
            encoder.qext = 0
        except opuslib.OpusError as exc:
            self.assertEqual(opuslib.UNIMPLEMENTED, exc.code)
        else:
            self.assertEqual(0, encoder.qext)

    def test_decoder_decorator_properties_roundtrip(self):
        decoder = opuslib.Decoder(48000, 2)

        decoder.phase_inversion_disabled = 1
        self.assertEqual(1, decoder.phase_inversion_disabled)
        decoder.phase_inversion_disabled = 0
        self.assertEqual(0, decoder.phase_inversion_disabled)

        decoder.ignore_extensions = 1
        self.assertEqual(1, decoder.ignore_extensions)
        decoder.ignore_extensions = 0
        self.assertEqual(0, decoder.ignore_extensions)

    def test_decoder_optional_ctl_properties_report_unimplemented(self):
        decoder = opuslib.Decoder(48000, 2)

        try:
            decoder.osce_bwe = 0
        except opuslib.OpusError as exc:
            self.assertEqual(opuslib.UNIMPLEMENTED, exc.code)
        else:
            self.assertEqual(0, decoder.osce_bwe)

        try:
            decoder.in_dtx
        except opuslib.OpusError as exc:
            self.assertEqual(opuslib.UNIMPLEMENTED, exc.code)
        else:
            self.assertIn(decoder.in_dtx, (0, 1))

    def test_decoder_read_only_packet_duration(self):
        fs = 48000
        channels = 2
        frame_size = 960
        pcm = b'\x00' * ctypes.sizeof(ctypes.c_short) * channels * frame_size
        encoder = opuslib.Encoder(fs, channels, opuslib.APPLICATION_AUDIO)
        decoder = opuslib.Decoder(fs, channels)

        packet = encoder.encode(pcm, frame_size)
        decoder.decode(packet, frame_size)

        self.assertEqual(frame_size, decoder.last_packet_duration)


if __name__ == '__main__':
    unittest.main()
