import cv2
from picamera2 import Picamera2

def main():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration())
    picam2.start()

    try:
        while True:
            frame = picam2.capture_array()
            cv2.imshow('Raspberry Pi Camera', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()