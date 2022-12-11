from time import sleep
import serial 
import keyboard

class SerialIO:
    def __init__(self) -> None:
        pass

class keybrdInput:
    def checkInput(self) -> None:
        while True:
            if keyboard.read_key() == "p":
                print("You pressed p")
                #break

def main():
    ser = serial.Serial('COM4')
    print(ser.name)
    
   
    while True:
        if keyboard.is_pressed("left"):
            print("left")
            ser.write(b'1')
        if keyboard.is_pressed("up"):
            print("up")
            ser.write(b'2')
        if keyboard.is_pressed("right"):
            print("right")
            ser.write(b'3')
        if keyboard.is_pressed("down"):
            print("down")
            ser.write(b'4')
        if keyboard.is_pressed("esc"):
            break
        sleep(0.010)
    ser.close()
    
    

if __name__ == '__main__':
    main()