import serial

# http://playground.arduino.cc/Interfacing/Python

def loop():
    ser = serial.Serial('/dev/tty.usbserial', 9600)
    while True:
        print ser.readline()


if __name__ == "__main__":
    loop()