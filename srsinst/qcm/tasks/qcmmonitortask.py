
import time
import numpy as np
from srsgui import Task
from srsgui import InstrumentInput, FloatListInput
from srsgui import TimePlot

from srsinst.qcm import get_qcm


class QCMMonitorTask(Task):
    """Monitor QCM200 frequency and resistance 
    """
    
    InstrumentName = 'qcm to monitor'
    GateTime = 'gate time (s)'
    GateTimeList = [0.1, 1.0, 10.0]

    input_parameters = {
        InstrumentName: InstrumentInput(),
        GateTime: FloatListInput(GateTimeList, '{:.1f}')
    }

    def setup(self):    
        self.logger = self.get_logger(__name__)
        
        self.params = self.get_all_input_parameters()
        self.qcm = get_qcm(self, self.params[self.InstrumentName])
        self.gate_time = self.params[self.GateTime]
        self.qcm.cmd.gate_time = self.gate_time
        self.initial_frequency = self.qcm.cmd.frequency
        self.initial_resistance = self.qcm.cmd.resistance

        self.add_details(self.initial_frequency, 'Initial frequency (Hz)')
        self.add_details(self.initial_resistance, 'Initial resistance (Ohm)')

        self.logger.info('Gate time: {} s'.format(self.params[self.GateTime]))
        
        self.ax = self.get_figure().subplots(nrows=2, ncols=1, sharex=True)

        self.resistance_plot = TimePlot(self, self.ax[1], 'Resistance', ['Resistance'])
        self.frequency_plot = TimePlot(self, self.ax[0], 'Frequency\n', ['Frequency'])
        self.frequency_plot.round_float_resolution = 9

        self.retry = 0

    def test(self):
        while self.is_running():
            try:
                new_data = self.qcm.get_data_if_both_new()
                if new_data:
                    freq = self.qcm.cmd.frequency
                    self.frequency_plot.add_data([freq], True)

                    resistance = self.qcm.cmd.resistance
                    self.resistance_plot.add_data([resistance], True)

                    # If the gate time in the input parameter frame is changed, change the gate time setting.
                    new_gate_time = self.get_input_parameter(self.GateTime)
                    if new_gate_time != self.gate_time:
                        self.gate_time = new_gate_time
                        self.qcm.cmd.gate_time = self.gate_time
                        self.logger.info('Gate time changed to {:.1f} s'.format(self.gate_time))
                    time.sleep(self.qcm.cmd.gate_time - 0.1)

                # Zoom in after the initial autoscale
                if self.frequency_plot.data_points == 2:
                    self.frequency_plot.ax.set_ylim(self.initial_frequency - 5, self.initial_frequency + 5)
                    self.resistance_plot.ax.set_ylim(self.initial_resistance - 0.5, self.initial_resistance + 0.5)

                self.retry = 0
            except Exception as e:
                self.logger.error(e)
                self.retry += 1
                if self.retry > 5:
                    break
                    
    def cleanup(self):
        pass
        
