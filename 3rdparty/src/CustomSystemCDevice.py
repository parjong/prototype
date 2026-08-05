from m5.params import *
from m5.SimObject import SimObject
from m5.objects.Device import BasicPioDevice

class CustomSystemCDevice(BasicPioDevice):
    type = 'CustomSystemCDevice'
    cxx_header = 'custom_systemc_device.hh'
    cxx_class = 'gem5::CustomSystemCDevice'
