from hpssa import HPSSA

from mercury.hardware import platform_detection
from mercury.hardware.drivers import driver, PCIDriverBase


@driver()
class SmartArrayDriver(PCIDriverBase):
    name = 'hpssa'
    driver_type = 'raid'
    _handler = HPSSA

    PCI_DEVICE_IDS = [
        "3239"  # Smart Array Gen9 Controllers
    ]

    @classmethod
    def probe(cls, pci_data):
        raid_pci_devices = platform_detection.get_raid_controllers(pci_data)
        if not platform_detection.has_smart_array_gen9(pci_data=raid_pci_devices):
            return

        owns = list()
        for device in raid_pci_devices:
            if cls.check(device):
                owns.append(device['slot'])
        return owns

    @classmethod
    def check(cls, pci_device):
        return pci_device['device_id'] in cls.PCI_DEVICE_IDS

    def inspect(self):
        hpssa = HPSSA()

        adapters = []
        for adapter in hpssa.adapters:
            _a = dict(**adapter)
            _a.update({
                'total_drives': adapter.total_drives,
                'total_size': adapter.total_size,
                'adapter_handler': self.name
            })

            adapters.append(_a)

        return adapters
