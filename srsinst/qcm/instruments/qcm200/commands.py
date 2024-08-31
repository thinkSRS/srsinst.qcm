
from srsgui.inst.commands import GetCommand, IntGetCommand, FloatGetCommand


class QCMGetCommand(GetCommand):
    def __init__(self, remote_command_name):
        super().__init__(remote_command_name)
        self.get_command_format = '{}'


class QCMIntGetCommand(IntGetCommand):
    def __init__(self, remote_command_name):
        super().__init__(remote_command_name)
        self.get_command_format = '{}'


class QCMFloatGetCommand(FloatGetCommand):
    def __init__(self, remote_command_name, unit=''):
        super().__init__(remote_command_name, unit)
        self.get_command_format = '{}'
