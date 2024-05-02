from abc import ABC

from action import Action
from arduino import Arduino


class Mouvement(Action):

    def __init__(self, coordinate_x, coordinate_y, coordinate_z, arduino):

        super().__init__()
        self.ok = None
        self.type_of_coordinate = "G90"
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.coordinate_z = coordinate_z
        self.arduino = arduino

    def toDo(self) -> bool:

        ok: bool = True

        g_code = (str(self.type_of_coordinate) + 'G0X' + str(self.coordinate_x) + 'Y' + str(
            self.coordinate_y) + 'Z' + str(self.coordinate_z) + '\n')

        print(f"{self.coordinate_x} mm movement in x and {self.coordinate_y} mm movement in y \r\n")

        self.arduino.write_read(g_code)

        print(g_code + 'ok!')

        ok = self.arduino.test_G2()

        return ok

    def info(self, ok: bool):
        if ok:
            print("OK : the move has been made \r\n\n")
        else:
            print("Error : Arduino didn't receive movement information \r\n\n")
