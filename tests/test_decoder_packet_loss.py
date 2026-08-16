#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import struct
import unittest

import opuslib


class DecoderPacketLossTest(unittest.TestCase):

    def test_existing_decode_with_packet_still_works(self):
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

        decoder = opuslib.Decoder(fs, channels)
        decoded = decoder.decode(packet, frame_size)

        self.assertEqual(len(pcm), len(decoded))

    def test_decode_none_conceals_lost_packet(self):
        fs = 48000
        channels = 2
        frame_size = 960

        decoder = opuslib.Decoder(fs, channels)
        decoded = decoder.decode(None, frame_size)

        self.assertEqual(frame_size * channels * 2, len(decoded))

    def test_decode_float_none_conceals_lost_packet(self):
        fs = 48000
        channels = 2
        frame_size = 960

        decoder = opuslib.Decoder(fs, channels)
        decoded = decoder.decode_float(None, frame_size)

        self.assertEqual(frame_size * channels * 4, len(decoded))


if __name__ == '__main__':
    unittest.main()
