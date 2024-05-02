
class Plate(object):

    def __init__(self, well):
        self.well = well
        self.A1_z = None
        self.A1_y = None
        self.A1_x = None
        self.row = None
        self.column = None
        self.tx = []
        self.ty = []
        self.x_plate_field = None
        self.y_plate_field = None

    def well_6(self):
        self.row = 2
        self.column = 3
        self.A1_x = 2
        self.A1_y = 6
        self.A1_z = -35
        self.tx = [0.0] * 4
        self.ty = [0.0] * 3
        self.x_plate_field = 12
        self.y_plate_field = 8


    # def coordinate_well(self):
    #     for r in range(1, len(self.ty)):
    #         y = self.A1_y - ((self.y_plate_field / self.row) * (r - 1))
    #         self.ty[r] = y
    #         print(str(y) + ' y ' + str(r))
    #
    #         for c in range(1, len(self.tx)):
    #             x = self.A1_x + ((self.x_plate_field / self.column) * (c - 1))
    #             self.tx[c] = x
    #             print(str(x) + ' x ' + str(c))


    def coordinate_well(self):
        for c in range(1, len(self.tx)):
            x = self.A1_x + ((self.x_plate_field / self.column) * (c - 1))
            self.tx[c] = x
            print(str(x) + ' x ' + str(c))

            for r in range(1, len(self.ty)):
                y = self.A1_y - ((self.y_plate_field / self.row) * (r - 1))
                self.ty[r] = y
                print(str(y) + ' y ' + str(r))


