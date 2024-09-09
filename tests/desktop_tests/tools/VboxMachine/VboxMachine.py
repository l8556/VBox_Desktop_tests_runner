# -*- coding: utf-8 -*-
from functools import wraps

from VBoxWrapper import VirtualMachine
from .vm_data import VmData

def vm_is_turn_on(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):

        if not self.vm.power_status():
            return print("[red]|ERROR| Vm data has not been created, start the vm machine")

        return method(self, *args, **kwargs)

    return wrapper


class VboxMachine:

    def __init__(self, name: str, cores: int = 1, memory: int = 2096):
        self.vm = VirtualMachine(name)
        self.cores = cores
        self.memory = memory
        self.name = name
        self.data = None

    @vm_is_turn_on
    def create_data(self):
        self.data = VmData(
            ip=self.vm.network.get_ip(),
            user=self.vm.get_logged_user(),
            name=self.name,
            local_dir=self.vm.get_parameter('CfgFile')
        )

    def run(self, headless: bool = True, status_bar: bool = False, timeout: int = 600):
        if self.vm.power_status():
            self.vm.stop()

        self.vm.snapshot.restore()
        self.configurate()
        self.vm.run(headless=headless)
        self.vm.network.wait_up(status_bar=status_bar, timeout=timeout)
        self.vm.wait_logged_user(status_bar=status_bar, timeout=timeout)
        self.create_data()


    def configurate(self):
        self.vm.set_cpus(self.cores)
        self.vm.nested_virtualization(True)
        self.vm.set_memory(self.memory)
        self.vm.audio(False)
        self.vm.speculative_execution_control(True)

    def stop(self):
        self.vm.stop()
