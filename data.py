import ctypes  # import the C compatible data types
from sys import platform, path  # this is needed to check the OS type and get the PATH
from os import sep  # OS specific file path separators


lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
dwf = ctypes.cdll.LoadLibrary(lib_path)
constants_path = (
    sep
    + "Applications"
    + sep
    + "WaveForms.app"
    + sep
    + "Contents"
    + sep
    + "Resources"
    + sep
    + "SDK"
    + sep
    + "samples"
    + sep
    + "py"
)


# import constants
path.append(constants_path)


from ctypes import *
from dwfconstants import *
import time
import sys

hdwf = c_int()
sts = c_byte()
IsEnabled = c_int()
vpp = c_double()
vpn = c_double()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: " + str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

# set up analog IO channel nodes
# enable positive supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(0), c_double(1))
# set voltage to 5 V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(5.0))
# enable negative supply


dwf.FDwfAnalogIOEnableSet(hdwf, c_int(1))


def measure(channel):
    """
    measure a voltage
    parameters: - device data
                - the selected oscilloscope channel (1-2, or 1-4)

    returns:    - the measured voltage in Volts
    """
    # set up the instrument
    dwf.FDwfAnalogInConfigure(hdwf, c_bool(False), c_bool(False))

    # read data to an internal buffer
    dwf.FDwfAnalogInStatus(hdwf, c_bool(False), c_int(0))

    # extract data from that buffer
    voltage = c_double()  # variable to store the measured voltage
    dwf.FDwfAnalogInStatusSample(hdwf, c_int(channel - 1), byref(voltage))

    # store the result as float
    voltage = voltage.value
    return voltage


for i in range(1, 100000):
    # wait 1 second between readings
    time.sleep(0.1)
    # fetch analogIO status from device
    if dwf.FDwfAnalogIOStatus(hdwf) == 0:
        break

    # voltage readback
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(0), c_int(1), byref(vpp))
    print("Positive Supply: " + str(round(vpp.value, 3)) + " V")
    data = measure(1)
    print("AnalogIn Channel 1: " + str(round(data, 3)) + " V")


dwf.FDwfDeviceClose(hdwf)
