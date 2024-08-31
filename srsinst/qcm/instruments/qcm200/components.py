
from srsgui.inst.component import Component
from srsgui.inst.commands import IntCommand, FloatCommand, FloatGetCommand, DictCommand

from .commands import QCMGetCommand, QCMIntGetCommand, QCMFloatGetCommand


class Keys:
    AbsoluteFrequency = 'abs. F'
    RelativeFrequency = 'rel. F'
    MassDisplacement = 'mass disp.'
    AbsoluteResistance = 'abs. R'
    RelativeResistance = 'rel. R'
    GateTime = 'gate time'
    AnalogFrequencyScaleFactor = 'f scale factor'

    NewResistanceValue = 'new R'
    NewFrequencyValue = 'new F'
    FrequencyOverRange = 'F over range'
    FrequencyUnderRange = 'F under range'
    CommunicationError = 'comm. error'

    InternalTCXO = 'int. TCXO'
    External10MHz = 'ext. 10 MHz'


class Cmd(Component):
    """Component holding all remote command used in QCM200"""

    DisplayModeDict = {
        Keys.AbsoluteFrequency:  0,
        Keys.RelativeFrequency:  1,
        Keys.MassDisplacement:   2,
        Keys.AbsoluteResistance: 3,
        Keys.RelativeResistance: 4,
        Keys.GateTime:           5,
        Keys.AnalogFrequencyScaleFactor: 6
        }
    
    AnalogFrequencyScaleDict = {  # Hz/V
        200:   0,
        500:   1,
        1000:  2,
        2000:  3,
        5000:  4,
        10000: 5,
        20000: 6
        }
    
    GateTimeDict = {
        0.1:  0,
        1.0:  1,
        10.0: 2,
        }
    
    StatusBitDict = {
        Keys.NewResistanceValue:  0,
        Keys.NewFrequencyValue:   1,
        Keys.FrequencyOverRange:  2,
        Keys.FrequencyUnderRange: 3,
        Keys.CommunicationError:  4
        }
    
    TimeBaseDict = {
        Keys.InternalTCXO:  0,
        Keys.External10MHz: 1
        }
    
    id_string = QCMGetCommand('I')
    display_mode = DictCommand('D', DisplayModeDict)
    frequency_scale = DictCommand('V', AnalogFrequencyScaleDict, None, 'Hz/V')
    gate_time = DictCommand('P', GateTimeDict, None, 's')
    frequency = QCMFloatGetCommand('F', 'Hz')
    frequency_offset = FloatGetCommand('G', 'Hz', 0.0, 10000000.0, 0.01, 9)
    resistance = QCMFloatGetCommand('R', 'Ohm')
    resistance_offset = FloatGetCommand('S', 'Ohm')
    status = QCMIntGetCommand('B')
    timebase = DictCommand('T', TimeBaseDict)

    def reset_frequency_offset(self):
        self.comm.send('G')

    def reset_resistance_offset(self):
        self.comm.send('S')

    allow_run_button = [reset_frequency_offset, reset_resistance_offset]
