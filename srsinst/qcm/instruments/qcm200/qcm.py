
from srsgui import Instrument, SerialInterface, InstIdError
from srsgui import FindListInput
from .components import Cmd


class QCM200(Instrument):
    _IdString = 'QCM200'
    _term_char = b'\r'

    available_interfaces = [
        [
            SerialInterface,
            {
                'port': FindListInput(),
                'baud_rate': 9600,
                'hardware_flow_control': False
            }
        ],
    ]

    def __init__(self, interface_type=None, *args):
        super().__init__(interface_type, *args)

        self._over_frequency_flag = False
        self._under_frequency_flag = False
        self._comm_error_flag = False
        self._new_frequency_flag = False
        self._new_resistance_flag = False

        self.last_over_frequency_error = False
        self.last_under_frequency_error = False
        self.last_comm_error = False

        self.last_frequency = 0.0
        self.last_resistance = 0.0

        self.cmd = Cmd(self)

    def check_id(self):
        if not self.is_connected():
            return None, None, None
        reply = self.query_text('I')
        strings = reply.split('_')

        if len(strings) != 4:
            return None, None, None

        if self._IdString not in reply:
            raise InstIdError("Invalid instrument: {} not in {}"
                              .format(self._IdString, reply))

        self._id_string = reply
        self._model_name = strings[0]
        self._serial_number = strings[3]
        self._firmware_version = strings[1]
        return self._model_name, self._serial_number, self._firmware_version

    def handle_command(self, cmd_string):
        cmd = cmd_string.upper()
        reply = ''
        if cmd == 'F' or \
           cmd == 'R' or \
           cmd == 'B' or \
           cmd == 'I':
            reply = self.query_text(cmd).strip()
        else:
            reply = super().handle_command(cmd)
        return reply

    def get_data_if_both_new(self):
        status = self.cmd.status
        if status & 0x02 != 0:
            self._new_frequency_flag = True
        if status & 0x01 != 0:
            self._new_resistance_flag = True

        new_error = status & 0x1C != 0
        if new_error:
            if status & 0x4:
                self._over_frequency_flag = True
            if status & 0x8:
                self._under_frequency_flag = True
            if status & 0x10:
                self._comm_error_flag = True

        if self._new_resistance_flag and self._new_resistance_flag:
            self.last_frequency = self.cmd.frequency
            self.last_resistance = self.cmd.resistance
            self._new_resistance_flag = False
            self._new_frequency_flag = False

            self.last_over_frequency_error = True if self._over_frequency_flag else False
            self.last_under_frequency_error = True if self._under_frequency_flag else False
            self.last_comm_error = True if self._comm_error_flag else False
            last_error_state = self.last_over_frequency_error or self.last_under_frequency_error or self.last_comm_error

            self._over_frequency_flag = False
            self._under_frequency_flag = False
            self._comm_error_flag = False

            return self.last_frequency, self.last_resistance, last_error_state
        else:
            return None

    def get_status(self):
        """
        Get error status in text.
        it overrides Instrument.get_status() method.

        :rtype: str
        """

        status = self.cmd.status
        if status & 0x1C == 0:
            return 'OK'

        # Now there is an error
        over_freq_error = True if status & 0x4 else False
        under_freq_error = True if status & 0x8 else False
        comm_error = True if status & 0x10 else False

        msg = ''
        if over_freq_error:
            msg += 'Freq. Over Range Error, '
        if under_freq_error:
            msg += 'Freq. Under Range Error, '
        if comm_error:
            msg += 'Comm. Error, '
        if len(msg) > 2:
            msg = msg[:-2]
        return msg
