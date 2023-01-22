"""Generates dataset of random data into CSV file"""

from enum import Enum
import generators

# available column types for generation
class ColumnType(Enum):
    NAME = 1
    PHONE_NUMBER = 2
    EMAIL = 3
    RANDOM_NUMBER = 4
    CITY = 5
    COUNTRY = 6
    PASSWORD = 7


generator_functions = [
    generators.get_random_name,
    generators.get_random_phone_number,
    generators.get_random_email,
    generators.get_random_number,
    generators.get_random_city,
    generators.get_random_country,
    generators.get_random_password,
]

# print all column types
def list_column_types():
    print("Available column types:")
    for col_type in ColumnType:
        print("\t{0}) {1}".format(col_type.value, col_type.name))


class Column:
    def __init__(self, name, col_type):
        self.name = name
        self.col_type = col_type
        # borders for RANDOM_NUMBER
        # lo also used for specifying country for CITY type
        self.lo = 0
        self.hi = 0

    def __str__(self):
        return "{0}, ".format(self.name)


class Header:
    columns = []  # list of Column objects

    def __init__(self):
        pass

    def add_column(self, col: Column):
        self.columns.append(col)

    def remove_column(self, index: int):
        del self.columns[index]

    # print all values in columns list
    def show_header(self):
        print("+--------+--------------+--------+")
        print("|   id   |     type     |  name  |")
        print("+--------+--------------+--------+")
        for i in range(len(self.columns)):
            # printing with index in list
            if self.columns[i].col_type == ColumnType.RANDOM_NUMBER.name:
                print(
                    "[{0}]\t{1} ({3}-{4})\t{2}".format(
                        i,
                        self.columns[i].col_type,
                        self.columns[i].name,
                        self.columns[i].lo,
                        self.columns[i].hi,
                    )
                )
            elif self.columns[i].col_type == ColumnType.CITY.name:
                print(
                    "[{0}]\t{1} ({3})\t{2}".format(
                        i,
                        self.columns[i].col_type,
                        self.columns[i].name,
                        self.columns[i].lo,
                    )
                )
            else:
                print(
                    "[{0}]\t{1}\t{2}".format(
                        i, self.columns[i].col_type, self.columns[i].name
                    )
                )
        print()

    def change_column_name(self, index: int, new_name: str):
        self.columns[index].name = new_name

    def change_column_type(self, index: int, new_type: ColumnType):
        # if new column type is CITY
        if new_type == ColumnType.CITY.name:
            print("enter 'countries' to see list of all countries.")
            lo = input("(specify country/leave empty if any)~> ").strip().title()
            while lo.lower() == "countries":
                print(generators.get_all_countries())
                lo = input("(specify country/leave empty if any)~> ")

            # if country not found in list of countries write warning and exit
            if lo.strip() != "" and lo.strip() not in generators.get_all_countries():
                print("Country not found.")
                return

            # if no input then any country
            if lo == "":
                lo = "any"

            self.columns[index].col_type = new_type
            self.columns[index].lo = lo

        # if new column type is RANDOM_NUMBER
        elif new_type == ColumnType.RANDOM_NUMBER.name:
            try:
                lo = int(input("(lowest number)~> "))
                hi = int(input("(highest number)~> "))

                if lo > hi:
                    print("Incorrect input. First number must be lower than second.")
                else:
                    self.columns[index].col_type = new_type
                    self.columns[index].lo = lo
                    self.columns[index].hi = hi

            except:
                print("Incorrect number.")


class DataRow:
    cells = []  # row of data

    def __init__(self):
        pass

    def __str__(self):
        str_row = ""
        for cell in self.cells:
            str_row += "{0}, ".format(cell)
        str_row += "\n"
        return str_row

    def generate(self):
        self.cells.clear()
        for col in Header.columns:
            self.cells.append(
                generator_functions[ColumnType[col.col_type].value - 1](col.lo, col.hi)
            )


running = True
header = Header()


def clear_table():
    header.columns.clear()


# introduction, waiting for commands
print("====== Dataset Generator ======\n")
print('Type "help" for information.')
while running == True:
    user_input = input(">>> ")
    # list of available commands
    if user_input.lower().strip() == "help":
        print(
            "List of commands:\n"
            "\th - show created table\n"
            "\tn - add new column\n"
            "\tr - remove column\n"
            "\tc - change column\n"
            "\tg - generate dataset\n"
            "\treset - clear table template\n"
            "\texit - terminate app\n"
        )

    # show header
    elif user_input.lower().strip() == "h":
        header.show_header()

    # add new column
    elif user_input.lower().strip() == "n":
        input_name = input("(column name)~> ").strip()

        # column name can't be empty
        if input_name.strip() == "":
            print("Column name can't be empty.")
            continue

        # specifying type of column
        try:
            list_column_types()
            input_type = input("(column type)(1-7)~> ")

            input_type = ColumnType(int(input_type)).name
        except:
            print("Incorrect data type. Enter type id from list of available options.")
            continue

        created_column = Column(input_name, input_type)

        # if type is CITY ask user to enter country
        # if country not found generates city from random country
        if input_type == ColumnType.CITY.name:
            print("enter 'countries' to see list of all countries.")
            created_column.lo = (
                input("(specify country/leave empty if any)~> ").strip().title()
            )
            while created_column.lo.lower() == "countries":
                print(generators.get_all_countries())
                created_column.lo = input("(specify country/leave empty if any)~> ")

            # if country not found in list of countries write warning and exit
            if (
                created_column.lo.strip() != ""
                and created_column.lo.strip() not in generators.get_all_countries()
            ):
                print("Country not found.")
                continue

            # if no input then any country
            if created_column.lo == "":
                created_column.lo = "any"

        # if type is RANDOM_NUMBER ask user to enter borders
        if input_type == ColumnType.RANDOM_NUMBER.name:
            try:
                created_column.lo = int(input("(lowest number)~> "))
                created_column.hi = int(input("(highest number)~> "))

                if created_column.lo > created_column.hi:
                    print("Incorrect input. First number must be lower than second.")
                    continue
            except:
                print("Incorrect number.")
                continue

        header.add_column(created_column)

    # remove column
    elif user_input.lower().strip() == "r":
        # displaying all columns
        header.show_header()

        # getting id of column to delete
        user_input = input("(column id to delete)~> ")
        try:
            header.remove_column(int(user_input))
        except:
            print("Column with id {0} not found.".format(user_input))

    # change column
    elif user_input.lower().strip() == "c":
        # displaying all columns
        header.show_header()

        # getting id of column to change
        try:
            id_to_change = int(input("(column id to change)~> "))
        except:
            print("Invalid id.")

        what_to_change = input(
            "What'd you like to change?\n" "\t1) Name\n" "\t2) Type\n" "\t3) Both\n~> "
        )

        # changing only name
        if what_to_change.strip() == "1":
            new_name = input("(enter new name)~> ")
            header.change_column_name(id_to_change, new_name)

            print("Column name changed.")

        # changing only type
        elif what_to_change.strip() == "2":
            list_column_types()
            new_type = input("(column type)(1-7)~> ")
            try:
                new_type = ColumnType(int(new_type)).name
                header.change_column_type(id_to_change, new_type)
            except:
                print(
                    "Incorrect data type. Enter type id from list of available options."
                )
                continue

        # changing name and type
        elif what_to_change.strip() == "3":
            # changing name
            new_name = input("(enter new name)~> ")
            header.change_column_name(id_to_change, new_name)

            # changing type
            list_column_types()
            new_type = input("(column type)(1-7)~> ")
            try:
                new_type = ColumnType(int(new_type)).name
                header.change_column_type(id_to_change, new_type)
            except:
                print(
                    "Incorrect data type. Enter type id from list of available options."
                )
                continue

        else:
            print("Unknown option.")

    # generate dataset
    elif user_input.lower().strip() == "g":
        file_name = input("(enter name of CSV file)~> ")

        try:
            amount_of_rows = int(input("(how many rows to generate?)~> "))
        except:
            print("Invalid value.")

        print("Generating data...")

        # writing header to file
        f = open("{0}.csv".format(file_name), "a")
        for column in header.columns:
            f.write("{0}, ".format(column.name))
        f.write("\n")
        f.close()

        # generating rows of data, writing data to csv file
        f = open("{0}.csv".format(file_name), "a")
        for row_index in range(amount_of_rows):
            data_row = DataRow()
            data_row.generate()
            f.write(str(data_row))
        f.close()

        print("Generation complete.")
        answer = input("Do you want to continue working? (y/n): ").strip()
        if answer.lower() == "y":
            answer = input("Clean last table template? (y/n): ")
            if answer.lower() == "y":
                clear_table()
                continue
            else:
                continue

        elif answer.lower() == "n":
            running = False

    # clearing table template
    elif user_input.lower().strip() == "reset":
        clear_table()
        print("Template cleared.")

    # terminating on exit command
    elif user_input.lower().strip() == "exit":
        running = False

    elif user_input.strip() == "":
        pass

    else:
        print("Unknown command. Type 'help' for information.")

print("Program complete.")
