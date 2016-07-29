import sys
import glob
import serial

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Looks at all ports and grabs the one that looks like arduino. Could break if other ports available. If it prints out more than one tty.usbmodem then you might need to add the name of the port manually
def get_arduino_ports():
    all_ports = serial_ports()
    print all_ports
    tty_ports = filter(lambda port_name: "tty.usbmodem" in port_name or "COM" in port_name, all_ports)
    if len(tty_ports) > 2:
        print "Too many ports found! Try manually entering them from this list:"
        print tty_ports
        assert False
    if len(tty_ports) == 0:
        print "No ports found! Is arduino plugged in?"
        assert False
    return tty_ports
    
if __name__=="__main__":
    print get_arduino_port()