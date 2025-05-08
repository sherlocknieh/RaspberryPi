from ServoGimbal import ServoGimbal
from time import sleep
# Create a servo gimbal object
sg = ServoGimbal(14, 15)

# Run the servo gimbal
sg.move_to(0, 90)
sleep(2)
sg.release()