import csv


class CSV:

    @staticmethod
    def read(filename):
        with open(filename, "r") as file:
            reader = csv.reader(file, delimiter=";")
            lines = [line for line in reader]
            return lines[:1][0], lines[1:]

    @staticmethod
    def write(filename, header, lines):
        with open(filename, "w") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)
            for line in lines:
                writer.writerow(line)