import logging
import struct
import threading
import time
import serial
import codi_stm32_generated_functions as stm32_cmd

log = logging.getLogger("codi-app: ({})".format(__name__))


class SerialPort:
    thread: threading.Thread
    socket: serial.Serial
    lock: threading.Lock = threading.Lock()
    is_running: bool = False
    is_uploading: bool = False

    def __init__(self):
        try:
            # init socket (cmd mode)
            self.stm32_cmd_mode_switch()
        except Exception as e:
            log.critical(e)

    def read_from_serial(self) -> None:
        msg_header: bytes = bytes.fromhex("58 21 58 21")  # X!X!

        log.info("[cmd_mode]: Listening to CoDi...")

        while self.is_running:
            header: bytes = self.socket.read_until(msg_header, size=300)

            if len(header) >= 4 and self.is_running and header[0:4] == msg_header:
                log.debug("[cmd_mode]: CoDi packet received, unpacking...")
                msg_size = struct.unpack(">I", self.socket.read(4))[
                    0
                ]  # TODO: Type hint this

                if msg_size <= 300 and self.is_running:
                    log.debug("[cmd_mode]: Valid CoDi packet, parsing...")
                    msg = self.socket.read(msg_size - 8)  # TODO: type hint
                    stm32_cmd.readMessage(msg)
                else:
                    if self.is_running:
                        log.error("[cmd_mode]: Malformed CoDi packet, ignoring.")

    def stm32_cmd_mode_switch(self) -> None:
        try:
            if self.socket is not None:
                self.socket.cancel_read()
                time.sleep(1)
                self.socket.close()

            if self.thread is not None:
                self.thread.join(4)

            # connect to socket
            self.socket = serial.Serial("/dev/ttyS1", baudrate=115200)

            self.thread = threading.Thread(target=self.read_from_serial)
        except Exception as e:
            log.critical(e)

    def stop_serial(self) -> None:
        self.is_running = False
        self.socket.cancel_read()
        time.sleep(0.1)
        self.socket.close()
        self.thread.join(4)

    def get_socket(self) -> serial.Serial:
        self.is_running = False
        self.is_uploading = False

        if self.socket is not None:
            self.socket.cancel_read()

        if self.thread is not None:
            self.thread.join(4)

        return self.socket

    def send_command(self, cmd: int) -> None:
        try:
            self.lock.acquire()
            self.socket.write(cmd)
            self.lock.release()
        except Exception as e:
            log.critical(e)

    def upload_read_from_serial(self) -> None:
        log.info("[upload_mode]: Listening to CoDi...")

        while self.is_running:
            resp = self.socket.read()
            if self.socket.in_waiting > 0:
                resp += self.socket.read(self.socket.in_waiting)
            log.debug("[upload_mode]: Response from coDi: %r", resp)

    def switch_to_upload_mode(self) -> None:
        try:
            self.is_running = False

            if self.socket is not None:
                self.socket.cancel_read()
                time.sleep(1)
                self.socket.close()

            if self.thread is not None:
                self.thread.join(4)

            # now switch

            self.socket = serial.Serial("/dev/ttyS1", baudrate=230400, timeout=4)

            self.thread = threading.Thread(target=self.upload_read_from_serial)

            self.is_running = True

            self.thread.start()
        except Exception as e:
            log.critical(e)

    def switch_to_cmd_mode(self) -> None:
        try:
            self.is_running = False
            if self.socket is not None:
                self.socket.cancel_read()
                time.sleep(1)
                self.socket.close()
            if self.thread is not None:
                self.thread.join(4)

            self.socket = serial.Serial("/dev/ttyS1", baudrate=115200)
            self.thread = threading.Thread(target=self.read_from_serial)

            self.is_running = True
            self.thread.start()

        except Exception as e:
            log.error(e)
