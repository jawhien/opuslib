#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
import unittest
import unittest.mock

import opuslib
import opuslib.api.encoder


class EncoderMaxDataBytesTest(unittest.TestCase):

    def test_encode_uses_opus_packet_default(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)
        pcm = b'\x00' * ctypes.sizeof(ctypes.c_short) * 2 * 960

        with unittest.mock.patch(
                'opuslib.api.encoder.encode',
                return_value=b'packet'
        ) as encode:
            result = encoder.encode(pcm, 960)

        self.assertEqual(b'packet', result)
        encode.assert_called_once_with(
            encoder.encoder_state,
            pcm,
            960,
            opuslib.api.encoder.DEFAULT_MAX_DATA_BYTES
        )

    def test_encode_allows_custom_packet_limit(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)
        pcm = b'\x00' * ctypes.sizeof(ctypes.c_short) * 2 * 960

        with unittest.mock.patch(
                'opuslib.api.encoder.encode',
                return_value=b'packet'
        ) as encode:
            result = encoder.encode(pcm, 960, max_data_bytes=64)

        self.assertEqual(b'packet', result)
        encode.assert_called_once_with(encoder.encoder_state, pcm, 960, 64)

    def test_encode_float_uses_opus_packet_default(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)
        pcm = b'\x00' * ctypes.sizeof(ctypes.c_float) * 2 * 960

        with unittest.mock.patch(
                'opuslib.api.encoder.encode_float',
                return_value=b'packet'
        ) as encode:
            result = encoder.encode_float(pcm, 960)

        self.assertEqual(b'packet', result)
        encode.assert_called_once_with(
            encoder.encoder_state,
            pcm,
            960,
            opuslib.api.encoder.DEFAULT_MAX_DATA_BYTES
        )

    def test_encode_float_allows_custom_packet_limit(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)
        pcm = b'\x00' * ctypes.sizeof(ctypes.c_float) * 2 * 960

        with unittest.mock.patch(
                'opuslib.api.encoder.encode_float',
                return_value=b'packet'
        ) as encode:
            result = encoder.encode_float(pcm, 960, max_data_bytes=64)

        self.assertEqual(b'packet', result)
        encode.assert_called_once_with(encoder.encoder_state, pcm, 960, 64)


if __name__ == '__main__':
    unittest.main()
