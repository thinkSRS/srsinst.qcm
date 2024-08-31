
from srsgui import Task
from srsinst.qcm.instruments.qcm200.qcm import QCM200


def get_qcm(task: Task, name=None) -> QCM200:
    inst = task.get_instrument(name)
    
    if not issubclass(inst.__class__, QCM200):
        raise TypeError('{} is not a QCM200 instance'.format(name))
    return inst
