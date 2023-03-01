# import the tabule module to organise data in a table format
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:
    """A class used to represent a pair of shoes.

    Attributes:
        country (str) : the country of production
        code (str) : the code of the shoes in catalogue
        product (str) : the name of the shoes
        cost (int) : the price of the shoes
        quantity (int) : the number of the shoes available in stock

    Methods:
        get_cost : returns the cost of the shoe
        get_quantity : returns the quantity of the shoes
        __str__ : returns a string representation of a class. """

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        '''Returns the cost of the shoe.'''
        return self.cost

    def get_quantity(self):
        '''Returns the quantity of the shoes.'''
        return self.quantity

    def __str__(self):
        '''Returns a string representation of a class in a table format.'''

        # create a table represented by a list of two lists where first list is used as a headliner,
        # the second list represents a row of the table
        table = [['Country', 'Code', 'Product', 'Cost', 'Quantity'],
                 [self.country, self.code, self.product, self.cost, self.quantity]]
        output = tabulate(table, headers="firstrow", tablefmt="fancy_outline")
        return output

#=============Shoe list===========
# create a variable to store a list of objects of shoes.
shoe_list = []

#==========Functions outside the class==============

def read_shoes_data():
    '''Read the data from the file inventory.txt, creates a shoes object with this data
    and append this object into the shoes list.'''

    # open the 'inventory.txt' file, ensure the file is stored in a corresponding folder
    try:
        f = open('inventory.txt', 'r')
    except FileNotFoundError:
        print("File 'inventory.txt' not found. Put the file in the folder you are working in.")
    else:
        # iterate over the file content
        for pos, line in enumerate(f):

            # skip the first line as it
            if pos == 0:
                continue

            # split each line where the comma is and store each part in separate variables
            line_split = line.split(",")
            country = line_split[0]
            code = line_split[1]
            product = line_split[2]

            # convert the cost and quantity into integer, ensure the data can be converted
            try:
                cost = int(line_split[3])
                quantity = int(line_split[4].strip('\n'))
            except ValueError:
                print(f"Invalid data in 'inventory.txt' file in line {pos + 1}.")
            else:
                # at each iteration create a shoe object using the variables as parameters and add each object to the shoe list
                shoe_obj = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe_obj)

        # go to the beginning of the file to calculate the number of shoes in the file and print out the relevant message
        f.seek(0)
        shoe_data_total = len(f.readlines())-1
        if len(shoe_list) == shoe_data_total:
            print(f"Data has been downloaded. There are {len(shoe_list)} shoe items out of {shoe_data_total}.")
        elif len(shoe_list) < shoe_data_total:
            print(f"Data has not been fully downloaded. There are {len(shoe_list)} shoe items out of {shoe_data_total}.")


def capture_shoes():
    '''Captures data about a shoe and creates a shoe object, then appends this object inside the shoe list
    and updates the 'inventory.txt' file.'''

    # request inputs from a user
    country = input("Country: ")
    code = input("Code: ")
    product = input("Product: ")

    # convert inputs for cost and quantity into integer, ensure the user has entered digits
    while True:
        try:
            cost = int(input("Cost: "))
            break
        except ValueError:
            print("Invalid format of cost. Try again.")

    while True:
        try:
            quantity = int(input("Quantity: "))
            break
        except ValueError:
            print("Invalid format of quantity. Try again.")

    # create a shoe object, append it to the shoe list and update the file
    shoe_obj = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe_obj)
    with open('inventory.txt', 'a') as f:
        f.write(f"\n{country},{code},{product},{cost},{quantity}")

    print("New product has been added.")


def view_all():
    '''Displays the details of all the shoes in a table format.'''

    # declare a list variable for creating a table
    table = []

    # iterate over the shoe list
    for shoe in shoe_list:

        # declare a variable for a row of the table
        row = []

        # store the attributes of each shoe object into a row list
        row.append(shoe.country)
        row.append(shoe.code)
        row.append(shoe.product)
        row.append(shoe.cost)
        row.append(shoe.quantity)

        # append each row list to the table list
        table.append(row)

    # print out the table
    print(tabulate(table, headers="firstrow", tablefmt="fancy_outline"))


def re_stock():
    '''Finds the shoe object with the lowest quantity, adds this quanitity of this shoe objects if wanted,
    and updates the list and the file for this shoe.'''

    # find a shoe object with the lowest quantity using lambda function and print its details out
    low_qty_shoe = min(shoe_list, key=lambda shoes: shoes.quantity)
    print(low_qty_shoe)

    # define the shoe's index in the shoe list
    index = shoe_list.index(low_qty_shoe)

    while True:
        # ask the user if they want to restock the shoe, use upper() method to eliminate the lettercase
        restock_choice = input("Want to restock? Y/N: ").upper()

        if restock_choice == 'Y':
            '''restocks the shoes'''
            # request quantity to add from the user, convert it into integer
            while True:
                try:
                    add_quantity = int(input("Quantity: "))
                    break
                except ValueError:
                    print("Invalid format of quantity. Try again.")

            # add the quantity entered to the quantity that is already in stock, and update the quantity attribute of the shoe
            new_quantity = low_qty_shoe.quantity + add_quantity
            low_qty_shoe.quantity = new_quantity

            # update the shoe object in the shoe list by its index and update the file
            shoe_list[index] = low_qty_shoe
            with open('inventory.txt', 'w') as f:
                f.write("Country,Code,Product,Cost,Quantity")
                for shoe in shoe_list:
                    f.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")

            print("Product has been re-stocked.")
            break

        elif restock_choice == 'N':
            break

        else:
            print("You have made a wrong choice, Please Try again")


def search_shoe():
    '''Searches for a shoe from the list by code and displays details of this shoe.'''

    # declare a variable to store the shoe object founded by the code
    shoe_search = None

    # request a code from a user
    code_search = input("Code: ")

    # iterate over the shoe list, store the shoe obj to the variable if its code matches the code entered by the user
    # and print out the shoe detaiks
    for shoe in shoe_list:
        if shoe.code == code_search:
            shoe_search = shoe
            print(shoe_search)

    # if the variable value remains None, print out the relevant message
    if shoe_search == None:
        print("No matches found.")


def value_per_item():
    '''Calculate the total value for each item and displays the result on on the console for all the shoes.'''

    # declare a variable for a table
    table = []

    # declare a variable to store the total value of all the shoes
    total_value = 0

    # iterate over the shoe list
    for shoe in shoe_list:

        # declare a list variable to store data of each row of the table
        row = []

        # for each shoe calculate its value, increment the total value by its value,
        # store its code and value into the row list and append the row to the table list
        cost = shoe.get_cost()
        quantity = shoe.get_quantity()
        value = cost * quantity
        total_value += value
        row.append(shoe.code)
        row.append(value)
        table.append(row)
    table.append(['TOTAL', total_value])

    # display the table
    print(tabulate(table, headers=['Code', 'Value'], tablefmt="fancy_outline"))


def highest_qty():
    '''Determines the product with the highest quantity and prints out the details of this shoe. '''

    # find a shoe object with the highest quantity using lambda function and print its details out
    high_qty_shoe = max(shoe_list, key=lambda shoes: shoes.quantity)
    print(high_qty_shoe)


def print_menu():
    '''Displays the main menu on the console.'''

    output = "MENU:\n"
    output += "1 - read shoes data\n"
    output += "2 - capture shoes\n"
    output += "3 - view all\n"
    output += "4 - restock\n"
    output += "5 - search\n"
    output += "6 - value per item\n"
    output += "7 - highest quantity\n"
    output += "8 - quit"
    print(output)


#==========Main Menu=============
# presenting main menu to a user
print_menu()

while True:
    # request an option to execute from the user
    menu = input("Select an option: ")

    if menu == '1':
        """Reads data from the file"""

        # ensure the data hasn't been read before, so that the data isn't dublicated
        if len(shoe_list) == 0:
            read_shoes_data()

    elif menu == '2':
        """Captures shoes"""

        # ensure the data has been downloaded from the file beforehand
        if len(shoe_list) == 0:
            read_shoes_data()
        capture_shoes()

    elif menu == '3':
        """Displays details of all the shoes"""

        # ensure the data has been downloaded from the file beforehand
        if len(shoe_list) == 0:
            read_shoes_data()
        view_all()

    elif menu == '4':
        """Finds the shoe with lowest quantity and restocks it"""

        # ensure the data has been downloaded from the file beforehand
        if len(shoe_list) == 0:
            read_shoes_data()
        re_stock()

    elif menu == '5':
        """Searches a shoe"""

        # ensure the data has been downloaded from the file beforehand
        if len(shoe_list) == 0:
            read_shoes_data()
        search_shoe()

    elif menu == '6':
        """Calculates value of each shoe"""

        # ensure the data has been downloaded from the file beforehand
        if len(shoe_list) == 0:
            read_shoes_data()
        value_per_item()

    elif menu == '7':
        """Finds the shoe with the highest quantity and displays its details"""

        # ensure the data has been downloaded from the file beforehand
        if len(shoe_list) == 0:
            read_shoes_data()
        highest_qty()

    elif menu == '8':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")