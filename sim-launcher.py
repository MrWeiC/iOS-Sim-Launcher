from subprocess import Popen, PIPE
import re
import argparse

# Parse Input Parameters including Device Type and OS Type
parser = argparse.ArgumentParser(
    description='This code is to start a simulator by device type and OS type. Example command: python sim-launcher.py "iPhone 6s Plus" "iOS 9.3"')
parser.add_argument('device_type', metavar='DEVICE_TYPE', type=str, nargs=1,
                    help='User can choose from below: iPhone 4s / iPhone 5 / iPhone 5s / iPhone 6 / iPhone 6 Plus / iPhone 6s / iPhone 6s Plus / iPad 2 / iPad Retina / iPad Air / iPad Air 2 / iPad Pro ')
parser.add_argument('os_type', metavar='OS_VERSION', type=str, nargs=1,
                    help='User can choose from below : iOS 9.2 / iOS 9.3')
args = parser.parse_args()

# Define Device Type and OS version
deviceType = args.device_type
deviceOSVersion = args.os_type

# Define Filter Tag
tagDeviceOSVersion = "-- " + deviceOSVersion + " --"

# Define CONSTANT TAG
TAG_DEVICES = "== Devices =="
TAG_DEVICES_PAIRS = "== Device Pairs =="
TAG_UNAVAILABLE = "-- Unavailable:"
TAG_DELLIMITER = "-- "
TAG_SHUTDOWN = "(Shutdown)"

# Read xcrun simctl list command result into a variable
p = Popen(["xcrun", "simctl", "list"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate(b"input data that is passed to subprocess' stdin")

# Get == Devices == Info
output = output[output.find(TAG_DEVICES):output.find(TAG_DEVICES_PAIRS)]

# Get Only the Blocks for the specific OS
output = output[(output.find(tagDeviceOSVersion) + len(tagDeviceOSVersion)):]
output = output[:output.find(TAG_DELLIMITER)]

# Get specfic DevicUDID for the devices
output = output[output.find(deviceType):]
output = output[:output.find(TAG_SHUTDOWN)]

deviceUDID = output[output.find("(") + 1:output.find("0") - 1]

# Check the device UDID match the UDID Pattern.
if deviceUDID == "":
    raise ValueError("Device UDID is null. Something is wrong in loading the device UDID")
pattern = re.compile(r'[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}')

if pattern.match(deviceUDID):
    print("Device UIDI is " + deviceUDID)
else:
    print ("There are some errors in the device UDID")
    raise ValueError("Device UDID is not match expected pattern. Something is wrong in loading the device UDID")
