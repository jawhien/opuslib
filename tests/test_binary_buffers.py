#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import struct
import unittest

import opuslib
import opuslib.api.decoder


class BinaryBufferTest(unittest.TestCase):

    def test_packet_helpers_accept_embedded_nul_bytes(self):
        packet = bytes([252, 0, 0])

        self.assertEqual(
            opuslib.BANDWIDTH_FULLBAND,
            opuslib.api.decoder.packet_get_bandwidth(packet)
        )
        self.assertEqual(1, opuslib.api.decoder.packet_get_nb_frames(packet))
        self.assertEqual(
            960,
            opuslib.api.decoder.packet_get_samples_per_frame(packet, 48000)
        )

    def test_encode_decode_roundtrip_with_binary_packet(self):
        fs = 48000
        channels = 2
        frame_size = 960
        samples = []

        for i in range(frame_size):
            value = int(12000 * math.sin(2 * math.pi * 440 * i / fs))
            samples.extend([value, value])

        pcm = struct.pack('<' + 'h' * len(samples), *samples)
        encoder = opuslib.Encoder(fs, channels, opuslib.APPLICATION_AUDIO)
        packet = encoder.encode(pcm, frame_size)

        self.assertIn(b'\x00', packet)
        self.assertEqual(1, opuslib.api.decoder.packet_get_nb_frames(packet))

        decoder = opuslib.Decoder(fs, channels)
        decoded = decoder.decode(packet, frame_size)

        self.assertEqual(len(pcm), len(decoded))


if __name__ == '__main__':
    unittest.main()
