# Program stores stock take data and restock, sort, discount price, calculate
# total worth per shoe

from operator import itemgetter
from tabulate import tabulate

class Shoe():

    def __init__(self, shoe_list = []):
        self.shoe_list = shoe_list

    # Stores data from "inventory.txt" in a 2D list
    def read_data(self):
        shoe_details_list = []
        try:
            with open("inventory.txt", 'r', encoding="utf-8") as file:
                file = file.readlines()[1:]
                for line in file:
                    line = line.replace("\n", '')
                    line = line.split(',')

                    line[3] = int(line[3])
                    line[4] = int(line[4])

                    shoe_details_list.append(line)
            self.shoe_list = shoe_details_list
        except FileExistsError as error:
            print(error)

    # Searches for shoe based of shoe code
    def search_shoe(self, shoe_code):

        for i in range(len(self.shoe_list)):
            if self.shoe_list[i][1] == shoe_code:
                return self.shoe_list[i]

        return f"No shoe listed with code: {shoe_code} in inventory"
    
    # Finds lowest quantity shoe in the list and restock to
    # the amount of what user entered
    def lowest_quant_shoe(self, restock_num):
        self.shoe_list.sort(key=itemgetter(4), reverse=False)
        self.shoe_list[0][4] += restock_num


    # Finds highest quantity shoe in the list and puts a sale discount on it
    # based of the amount the user entered
    def highest_quant_shoe(self, sale_discount):
        self.shoe_list.sort(key=itemgetter(4), reverse=True)
        self.shoe_list[0][3] = round(self.shoe_list[0][3] \
                                    * abs(sale_discount - 100)/100, 2)
    
    # adds a new column to the list that show the total stock value
    def value_per_item(self):
        for i in range(len(self.shoe_list)):
            total_worth = self.shoe_list[i][3] * self.shoe_list[i][4]                    
            self.shoe_list[i].insert(5, total_worth) 

    
store_list = []

# Creates a list of Shoe class and fills class list
for i in range(5):
    store_list.append(Shoe())
    store_list[i].read_data()

shoe_code = input("Enter shoe code you wish to search for: ")
print(store_list[0].search_shoe(shoe_code))

print("Lowest stock shoe")
restock_num = float(input("How many shoes do you wish to order for restock: "))
store_list[1].lowest_quant_shoe(restock_num)

print("Highest stock shoe")
discount = int(input("Enter discount price: "))
store_list[2].highest_quant_shoe(discount)

store_list[3].value_per_item()

for i in range(5):
    print(tabulate(store_list[i].shoe_list, headers=["Country", "Code",  
        "Product", "Cost", "Quantity", "Total worth"], tablefmt='fancy_grid'))
