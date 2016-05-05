from csv import Sniffer, DictReader, DictWriter, Dialect


class CSV:

    @staticmethod
    def read(filename):

        with open(filename, "r") as file:

            sample = file.read(4096)
            dialect = Sniffer().sniff(sample, delimiters=[";", ","])
            file.seek(0)

            reader = DictReader(file, dialect=dialect)
            lines = [line for line in reader]
            return reader.fieldnames, lines

    @staticmethod
    def write(filename, header, lines):

        with open(filename, "w") as file:
            writer = DictWriter(file, header)
            writer.writeheader()
            writer.writerows(lines)