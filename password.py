import random


class PassWord:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z'
                              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    symbols = ['!', '#', '$', '%', '(', ')', '*', '+', '@']

    def __init__(self):
        self.num_of_letters = random.randint(8, 10)
        self.num_of_numbers = random.randint(2, 4)
        self.num_of_symbols = random.randint(2, 4)
        self.password = []
        self.create_password()

    def create_password(self):
        for i in range(0, self.num_of_letters):
            self.password.append(self.letters[random.randint(0, len(self.letters) - 1)])
        for i in range(self.num_of_letters, self.num_of_numbers + self.num_of_letters):
            self.password.append(self.numbers[random.randint(0, len(self.numbers) - 1)])
        for i in range(self.num_of_numbers + self.num_of_letters,
                       self.num_of_symbols + self.num_of_numbers + self.num_of_letters):
            self.password.append(self.symbols[random.randint(0, len(self.symbols) - 1)])
        random.shuffle(self.password)
        self.password = "".join(str(pas) for pas in self.password)
