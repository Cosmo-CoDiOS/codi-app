"""
=======================================
 Modified YMODEM file transfer protocol
=======================================

.. $Id$

This is a implementation of YMODEM as used on the Cosmo Communicator.

Data flow example
=================

Here is a sample of the data flow, sending a 3-block message.

Batch Transmission Session (1 file - not tested with more than one)
-------------------------------------------------------------------

::

    SENDER                                      RECEIVER
                                            <-- C (command:rb)
    SOH 00 FF foo.c NUL[123] CRC CRC        -->
                                            <-- ACK
    SOH 01 FE Data[1024] CRC CRC            --> (probably received garbled)
                                            <-- C
    SOH 01 FE Data[1024] CRC CRC (resend)   --> (starts flash erase)
                                            <-- (empty read timed out)
                                            <-- (empty read timed out)
                                            <-- (empty read timed out)
                                            <-- C
    SOH 01 FE Data[1024] CRC CRC (resend)   -->
                                            <-- ACK
    SOH 02 FC Data[1024] CRC CRC            --> (probably received garbled)
                                            <-- C
    SOH 02 FC Data[1024] CRC CRC (resend)   -->
                                            <-- ACK
    SOH 03 FB Data[1000] CPMEOF[24] CRC CRC  -->
                                            <-- ACK
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- C
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- C
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- C
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- ACK

"""
from __future__ import division, print_function

__author__ = "Wijnand Modderman <maze@pyth0n.org>"
__copyright__ = [
    "Copyright (c) 2010 Wijnand Modderman",
    "Copyright (c) 1981 Chuck Forsberg",
    "Copyright (c) 2016 Michael Tesch",
]
__license__ = "MIT"
__version__ = "0.4.5"

import logging
import sys
import os

# Protocol bytes
NUL = b"\x00"
SOH = b"\x01"
STX = b"\x02"
EOT = b"\x04"
ACK = b"\x06"
ACK2 = b"\x86"
DLE = b"\x10"
NAK = b"\x15"
CAN = b"\x18"
CAN2 = b"\x98"
CRC = b"C"  # 0x43
CRC2 = b"\xc3"
CRC3 = b"\x83"
ABT = b"a"  # 0x61 - flash fail - abort


class YMODEM(object):
    """
    YMODEM Protocol handler, expects two callables which encapsulate the read
        and write operations on the underlying stream.

    Example functions for reading and writing to a serial line:

    >>> import serial
    >>> from xmodem import YMODEM
    >>> ser = serial.Serial('/dev/ttyUSB0', timeout=0) # or whatever you need
    >>> modem = YMODEM(ser)


    :param ser: serial port to read from or write to.
    :type getc: class
    :type mode: string
    :param pad: Padding character to make the packets match the packet size
    :type pad: char

    """

    # crctab calculated by Mark G. Mendel, Network Systems Corporation
    crctable = [
        0x0000,
        0x1021,
        0x2042,
        0x3063,
        0x4084,
        0x50A5,
        0x60C6,
        0x70E7,
        0x8108,
        0x9129,
        0xA14A,
        0xB16B,
        0xC18C,
        0xD1AD,
        0xE1CE,
        0xF1EF,
        0x1231,
        0x0210,
        0x3273,
        0x2252,
        0x52B5,
        0x4294,
        0x72F7,
        0x62D6,
        0x9339,
        0x8318,
        0xB37B,
        0xA35A,
        0xD3BD,
        0xC39C,
        0xF3FF,
        0xE3DE,
        0x2462,
        0x3443,
        0x0420,
        0x1401,
        0x64E6,
        0x74C7,
        0x44A4,
        0x5485,
        0xA56A,
        0xB54B,
        0x8528,
        0x9509,
        0xE5EE,
        0xF5CF,
        0xC5AC,
        0xD58D,
        0x3653,
        0x2672,
        0x1611,
        0x0630,
        0x76D7,
        0x66F6,
        0x5695,
        0x46B4,
        0xB75B,
        0xA77A,
        0x9719,
        0x8738,
        0xF7DF,
        0xE7FE,
        0xD79D,
        0xC7BC,
        0x48C4,
        0x58E5,
        0x6886,
        0x78A7,
        0x0840,
        0x1861,
        0x2802,
        0x3823,
        0xC9CC,
        0xD9ED,
        0xE98E,
        0xF9AF,
        0x8948,
        0x9969,
        0xA90A,
        0xB92B,
        0x5AF5,
        0x4AD4,
        0x7AB7,
        0x6A96,
        0x1A71,
        0x0A50,
        0x3A33,
        0x2A12,
        0xDBFD,
        0xCBDC,
        0xFBBF,
        0xEB9E,
        0x9B79,
        0x8B58,
        0xBB3B,
        0xAB1A,
        0x6CA6,
        0x7C87,
        0x4CE4,
        0x5CC5,
        0x2C22,
        0x3C03,
        0x0C60,
        0x1C41,
        0xEDAE,
        0xFD8F,
        0xCDEC,
        0xDDCD,
        0xAD2A,
        0xBD0B,
        0x8D68,
        0x9D49,
        0x7E97,
        0x6EB6,
        0x5ED5,
        0x4EF4,
        0x3E13,
        0x2E32,
        0x1E51,
        0x0E70,
        0xFF9F,
        0xEFBE,
        0xDFDD,
        0xCFFC,
        0xBF1B,
        0xAF3A,
        0x9F59,
        0x8F78,
        0x9188,
        0x81A9,
        0xB1CA,
        0xA1EB,
        0xD10C,
        0xC12D,
        0xF14E,
        0xE16F,
        0x1080,
        0x00A1,
        0x30C2,
        0x20E3,
        0x5004,
        0x4025,
        0x7046,
        0x6067,
        0x83B9,
        0x9398,
        0xA3FB,
        0xB3DA,
        0xC33D,
        0xD31C,
        0xE37F,
        0xF35E,
        0x02B1,
        0x1290,
        0x22F3,
        0x32D2,
        0x4235,
        0x5214,
        0x6277,
        0x7256,
        0xB5EA,
        0xA5CB,
        0x95A8,
        0x8589,
        0xF56E,
        0xE54F,
        0xD52C,
        0xC50D,
        0x34E2,
        0x24C3,
        0x14A0,
        0x0481,
        0x7466,
        0x6447,
        0x5424,
        0x4405,
        0xA7DB,
        0xB7FA,
        0x8799,
        0x97B8,
        0xE75F,
        0xF77E,
        0xC71D,
        0xD73C,
        0x26D3,
        0x36F2,
        0x0691,
        0x16B0,
        0x6657,
        0x7676,
        0x4615,
        0x5634,
        0xD94C,
        0xC96D,
        0xF90E,
        0xE92F,
        0x99C8,
        0x89E9,
        0xB98A,
        0xA9AB,
        0x5844,
        0x4865,
        0x7806,
        0x6827,
        0x18C0,
        0x08E1,
        0x3882,
        0x28A3,
        0xCB7D,
        0xDB5C,
        0xEB3F,
        0xFB1E,
        0x8BF9,
        0x9BD8,
        0xABBB,
        0xBB9A,
        0x4A75,
        0x5A54,
        0x6A37,
        0x7A16,
        0x0AF1,
        0x1AD0,
        0x2AB3,
        0x3A92,
        0xFD2E,
        0xED0F,
        0xDD6C,
        0xCD4D,
        0xBDAA,
        0xAD8B,
        0x9DE8,
        0x8DC9,
        0x7C26,
        0x6C07,
        0x5C64,
        0x4C45,
        0x3CA2,
        0x2C83,
        0x1CE0,
        0x0CC1,
        0xEF1F,
        0xFF3E,
        0xCF5D,
        0xDF7C,
        0xAF9B,
        0xBFBA,
        0x8FD9,
        0x9FF8,
        0x6E17,
        0x7E36,
        0x4E55,
        0x5E74,
        0x2E93,
        0x3EB2,
        0x0ED1,
        0x1EF0,
    ]

    def __init__(self, ser, pad=b"\x1a"):
        self.ser = ser
        self.pad = pad
        self.log = logging.getLogger("codiUpdate")

    def abort(self, count=2, timeout=60):
        """
        Send an abort sequence using CAN bytes.

        :param count: how many abort characters to send
        :type count: int
        :param timeout: timeout in seconds
        :type timeout: int
        """
        for _ in range(count):
            self.ser.write(CAN)

    def send(self, filename, slow_mode=False, retry=20, timeout=60, callback=None):
        """
        Send a stream via the YMODEM protocol.

            >>> print(modem.send('filename'))
            True

        Returns ``True`` upon successful transmission or ``False`` in case of
        failure.

        :param filename: The filename to send data from.
        :type filename: string
        :param slow_mode: If True, send only imediately after being asked, this can
                          help with repeatedly failing flashing.
        :type slow_mode: bool
        :param retry: The maximum number of times to try to resend a failed
                      packet before failing.
        :type retry: int
        :param timeout: The number of seconds to wait for a response before
                        timing out.
        :type timeout: int
        :param callback: Reference to a callback function that has the
                         following signature.  This is useful for
                         getting status updates while a ymodem
                         transfer is underway.
                         Expected callback signature:
                         def callback(total_packets, success_count, error_count, total)
        :type callback: callable
        """

        # initialize protocol
        packet_size = 1024

        self.log.debug("Begin start sequence, packet_size=%d", packet_size)
        error_count = 0
        cancel = 0
        while True:
            char = self.ser.read(1)
            if char:
                if char == CRC:
                    self.log.debug("16-bit CRC requested (CRC).")
                    break
                elif char == CAN or char == CAN2:
                    self.log.debug("received CAN")
                    if cancel:
                        self.log.info(
                            "Transmission canceled: received 2xCAN " "at start-sequence"
                        )
                        print(
                            "Remote side requested cancel, suggest trying again later"
                        )
                        return False
                    else:
                        self.log.debug("cancellation at start sequence.")
                        cancel = 1
                else:
                    self.log.info(
                        "send error: expected NAK, CRC, or CAN; " "got %r", char
                    )

            error_count += 1
            if error_count > retry:
                self.log.info("send error: error_count reached %d, " "aborting.", retry)
                self.abort(timeout=timeout)
                return False

        error_count = 0
        nak_count = 0
        success_count = 0
        total_packets = 0
        sequence = 0

        # send packet sequence 0 containing:
        #  Filename Length [Modification-Date [Mode [Serial-Number]]]
        stream = open(filename, "rb")
        stat = os.stat(filename)
        data = os.path.basename(filename).encode() + NUL + str(stat.st_size).encode()
        self.log.debug('ymodem sending : "%s" len:%d', filename, stat.st_size)

        if len(data) <= 128:
            header_size = 128
        else:
            header_size = 1024

        header = self._make_send_header(header_size, sequence)
        data = data.ljust(header_size, NUL)
        checksum = self._make_send_checksum(1, data)
        total = (stat.st_size / packet_size) + 1
        header_sent = False

        while not header_sent:
            self.log.debug("header send: block %d, pks: %d", sequence, header_size)
            self.ser.write(header + data + checksum)
            while True:
                char = self.ser.read(1)
                if char == CRC or char == CRC2 or char == CRC3:
                    in_waiting = self.ser.in_waiting
                    if in_waiting == 0:
                        self.log.debug(
                            "header re-send: block %d, pks: %d", sequence, packet_size
                        )
                        self.ser.write(header + data + checksum)
                    elif in_waiting > 1:
                        rubbish = self.ser.read(in_waiting - 1)
                        self.log.info(
                            "header got rubbish %r for block %d", rubbish, sequence
                        )
                    continue
                if char == ACK or char == ACK2:
                    success_count += 1
                    if callable(callback):
                        callback(total_packets, success_count, error_count, total)
                    error_count = 0
                    header_sent = True
                    break

                self.log.info(
                    "send error: expected CRC|ACK; got %r for block %d", char, sequence
                )
                error_count += 1
                if callable(callback):
                    callback(total_packets, success_count, error_count, total)
                if error_count > retry:
                    # excessive amounts of retransmissions requested,
                    # abort transfer
                    self.log.info(
                        "header send error: Unexpected received %d times, " "aborting.",
                        error_count,
                    )
                    self.abort(timeout=timeout)
                    return False

            # keep track of sequence
            sequence = (sequence + 1) % 0x100

        # send data
        while True:
            # build normal data packet
            data = stream.read(packet_size)
            if not data:
                # end of stream
                self.log.debug("send: at EOF")
                break
            total_packets += 1

            header = self._make_send_header(packet_size, sequence)
            data = data.ljust(packet_size, self.pad)
            checksum = self._make_send_checksum(1, data)

            # emit packet & get ACK
            if not slow_mode:
                self.log.debug("send: block %d, pks: %d", sequence, packet_size)
                self.ser.write(header + data + checksum)

            while True:
                char = self.ser.read(1)
                if char == CRC or char == CRC2 or char == CRC3:
                    in_waiting = self.ser.in_waiting
                    if slow_mode:
                        self.log.debug("send: block %d, pks: %d", sequence, packet_size)
                        self.ser.write(header + data + checksum)
                    elif in_waiting == 0:
                        self.log.debug(
                            "re-send: block %d, pks: %d", sequence, packet_size
                        )
                        self.ser.write(header + data + checksum)
                    elif in_waiting > 1:
                        rubbish = self.ser.read(in_waiting - 1)
                        self.log.info("got rubbish %r for block %d", rubbish, sequence)
                    continue
                if char == ACK or char == ACK2 or (char == NAK and not slow_mode):
                    success_count += 1
                    if callable(callback):
                        callback(total_packets, success_count, error_count, total)
                    error_count = 0
                    nak_count = 0
                    if char == NAK:
                        rubbish = self.ser.read(1024)
                        self.log.info(
                            "got NAK rubbish %r for block %d", rubbish, sequence
                        )
                        rubbish = self.ser.read(1024)
                        self.log.info(
                            "got NAK rubbish %r for block %d", rubbish, sequence
                        )
                        rubbish = self.ser.read(1024)
                        self.log.info(
                            "got NAK rubbish %r for block %d", rubbish, sequence
                        )
                        rubbish = self.ser.read(1024)
                        self.log.info(
                            "got NAK rubbish %r for block %d", rubbish, sequence
                        )
                    break
                if slow_mode and char == NAK:
                    nak_count += 1
                    error_count += 1
                    self.log.error(
                        "send error: expected CRC|ACK; got NAK(%d) for block %d",
                        nak_count,
                        sequence,
                    )
                    if nak_count > 4:
                        nak_count = 0
                        self.log.debug("try sending next block: %d", sequence)
                        break
                if char == ABT:
                    self.log.debug("got abort")
                    return False
                if char == CAN or char == CAN2:
                    self.log.debug("got cancel")
                    return False

                self.log.info(
                    "send error: expected CRC|ACK; got %r for block %d", char, sequence
                )
                error_count += 1
                if callable(callback):
                    callback(total_packets, success_count, error_count, total)
                if error_count > retry:
                    # excessive amounts of retransmissions requested,
                    # abort transfer
                    self.log.info(
                        "send error: Unexpected received %d times, " "aborting.",
                        error_count,
                    )
                    self.abort(timeout=timeout)
                    return False

            # keep track of sequence
            sequence = (sequence + 1) % 0x100

        # emit EOT and get corresponding ACK
        while True:
            self.log.debug("sending EOT, awaiting ACK")
            # end of transmission
            self.ser.write(EOT)
            self.ser.write(EOT)
            self.ser.write(EOT)

            # An ACK should be returned
            char = self.ser.read(1)
            if char == ACK:
                break
            else:
                self.log.info("send error: expected ACK; got %r", char)
                error_count += 1
                if error_count > retry:
                    self.log.warning("EOT was not ACKd, aborting transfer")
                    self.abort(timeout=timeout)
                    return False

        self.log.info("Transmission successful (ACK received).")
        stream.close()
        return True

    def _make_send_header(self, packet_size, sequence):
        assert packet_size in (128, 1024), packet_size
        _bytes = []
        if packet_size == 128:
            _bytes.append(ord(SOH))
        elif packet_size == 1024:
            _bytes.append(ord(STX))
        _bytes.extend([sequence, 0xFF - sequence])
        return bytearray(_bytes)

    def _make_send_checksum(self, crc_mode, data):
        assert crc_mode is 1
        _bytes = []
        if crc_mode:
            crc = self.calc_crc(data)
            _bytes.extend([crc >> 8, crc & 0xFF])
        return bytearray(_bytes)

    def calc_crc(self, data, crc=0):
        """
        Calculate the Cyclic Redundancy Check for a given block of data, can
        also be used to update a CRC.

            >>> crc = modem.calc_crc('hello')
            >>> crc = modem.calc_crc('world', crc)
            >>> hex(crc)
            '0xd5e3'

        """
        for char in bytearray(data):
            crctbl_idx = ((crc >> 8) ^ char) & 0xFF
            crc = ((crc << 8) ^ self.crctable[crctbl_idx]) & 0xFFFF
        return crc & 0xFFFF
