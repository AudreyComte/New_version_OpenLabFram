from abc import ABC

from action import Action
from arduino import Arduino

# Definition of the Mouvement class, inheriting from the Action class
class Mouvement(Action):

    def __init__(self, coordinate_x, coordinate_y, coordinate_z, arduino):

        super().__init__()
        self.ok = None # Variable to track the success of the movement
        self.type_of_coordinate = "G90" # Type of coordinate system (G90 for absolute positioning)
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.coordinate_z = coordinate_z
        self.arduino = arduino  # Instance of the Arduino class

    # Method to execute the movement
    def toDo(self) -> bool:

        ok: bool = True  # Variable to indicate whether the movement was successful

        g_code = (str(self.type_of_coordinate) + 'G0X' + str(self.coordinate_x) + 'Y' + str(
            self.coordinate_y) + 'Z' + str(self.coordinate_z) + '\n')

        print(f"{self.coordinate_x} mm movement in x and {self.coordinate_y} mm movement in y \r\n")

        # Send the G-code command to the Arduino
        self.arduino.write_read(g_code)

        print(g_code + 'ok!')

        # Test if the G2 command was executed successfully on the Arduino
        ok = self.arduino.test_G2()

        # Return the result of the movement (True if successful, False otherwise)
        return ok

    # Method to provide information about the movement's success or failure
    def info(self, ok: bool):
        if ok:
            # If movement was successful, print a confirmation message
            print("OK : the move has been made \r\n\n")
        else:
            # If movement failed, print an error message
            print("Error : Arduino didn't receive movement information \r\n\n")
