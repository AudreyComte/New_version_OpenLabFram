class Plate(object):

    def __init__(self, well):
        self.well = well  # Number of wells on the plate
        self.A1_z = None  # Z-coordinate of the A1 well
        self.A1_y = None  # Y-coordinate of the A1 well
        self.A1_x = None  # X-coordinate of the A1 well
        self.row = None  # Number of rows in the plate
        self.column = None  # Number of columns in the plate
        self.tx = []  # List to store X coordinates for each well
        self.ty = []  # List to store Y coordinates for each well
        self.x_plate_field = None  # Plate size in x
        self.y_plate_field = None  # plate size in y

    # Method to define the layout for a 6-well plate
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

    # Method to calculate the coordinates of the wells in the plate
    def coordinate_well(self):
        # Loop through the columns to calculate the X-coordinate for each column
        for c in range(1, len(self.tx)):
            x = self.A1_x + ((self.x_plate_field / self.column) * (c - 1))  # Calculate X based on column position
            self.tx[c] = x  # Store the calculated X value in the list
            print(str(x) + ' x ' + str(c))

            # Loop through the rows to calculate the Y-coordinate for each row
            for r in range(1, len(self.ty)):
                y = self.A1_y - ((self.y_plate_field / self.row) * (r - 1))  # Calculate Y based on row position
                self.ty[r] = y  # Store the calculated Y value in the list
                print(str(y) + ' y ' + str(r))
