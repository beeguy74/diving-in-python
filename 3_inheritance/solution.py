import os
import csv

class CarBase():
    def __init__(self, brand, photo_file_name, carrying):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        ext = os.path.splitext(self.photo_file_name)
        return (ext[-1])
        
class Truck(CarBase):
    car_type = "truck"
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl
        self._whl = self.whl
        self._body_length = None
        self._body_height = None
        self._body_width = None

    @property
    def whl(self):
        ret = self.body_whl.split(sep='x')
        flag = True
        for i in ret:
            try:
                float(i)
            except:
                flag = False
                break
        if flag and len(ret) == 3:
            self._whl = ret
        else:
            self._whl = 0.
        return self._whl

    @property
    def body_length(self):
        if self._body_length is None:
            if self._whl:
                self._body_length =  float(self._whl[0])
            else:
                self._body_length = 0.
        return self._body_length
    
    @property
    def body_height(self):
        if self._body_height is None:
            if self._whl:
                self._body_height=  float(self._whl[2])
            else:
                self._body_height= 0.
        return self._body_height

    @property
    def body_width(self):
        if self._body_width is None:
            if self.whl:
                self._body_width=  float(self._whl[1])
            else:
                self._body_width= 0.
        return self._body_width

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width

class Car(CarBase):
    car_type = "car"
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

class SpecMachine(CarBase):
    car_type = "spec_machine"
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

def check_row(row):
    types = ('car', 'truck', 'spec_machine')
    formats = ('.jpg', '.jpeg', '.png', '.gif')

    if len(row) != 7:
        return False
    if row[0] not in types:
        return False
    if row[1] == '':
        return False
    if row[0] == 'car':
        try:
            int(row[2])
        except:
            return False
    ch = os.path.splitext(row[3])
    if ch[-1] not in formats:
        return False
    try:
        float(row[5])
    except:
        return False
    if row[0] == 'spec_machine' and row[6] == "":
        return False
    return True


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if check_row(row):
                if row[0] == 'truck':
                    elem = Truck(row[1], row[3], row[5], row[4])
                elif row[0] == 'car':
                    elem = Car(row[1], row[3], row[5], row[2])
                elif row[0] == 'spec_machine':
                    elem = SpecMachine(row[1], row[3], row[5], row[6])
                car_list.append(elem)
    return car_list

# lst = get_car_list('list.csv')
# for i in lst:
#     print(i.brand)

# Order :
# type  brand seats image  whl  carry  extra

# pis = Truck('volvo', 'vala.jpeg', 20, '10x15x20')
# print(f"brand = {pis.brand} ext = {pis.get_photo_file_ext()} len = {pis.body_length}\nwid = {pis.body_width} hei = {pis.body_height}")
# print(f"volume = {pis.get_body_volume()}") 