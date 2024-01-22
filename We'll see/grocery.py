"""
Project Name: Grocery Expiry Date Tracker
Project Creation Date: 1/9/2023
Description: This application keeps track of the expirey date of groceries.
(Maybe) Notifies phone once the 

"""

import datetime
import csv
import pandas as pd

'''
class myItems()
Description: myItems is a class of items kept in the fridge. 
The the class will have the attributes: itemName, itemType, expiryDate, purchaseDate
Things to implement: 
    Try to read in the csv file and show it in a format.
    Be able to reorder the list based on different attributes
    Add new items onto the CSV
    Create a GUI 
    
'''

class MyItems():
    """
    MyItems is a class that represents grocery items in a fridge     
    
    """

    # def __init__(self, itemName, itemType, expiryDate, purchaseDate, groceryList):
    # def __init__(self, itemName, itemType, expiryDate, purchaseDate, expired):
    def __init__(self, itemName, itemType, expiryDate, purchaseDate):
        self.itemName = itemName
        self.itemType = itemType
        self.expiryDate = expiryDate
        self.purchaseDate = purchaseDate
        # self.expired = expired # Bool value that is true 
        #self.groceryList = groceryList
        print('{} has been created'.format(itemName))

    def __str__(self):
        return f"{self.itemName} was bought on {self.purchaseDate} and will expire on {self.expiryDate}. The item type is {self.itemType}"
    """
    def expiration_date(self)
    Description: Checks if the product is expired. If expired returns true. If not expired returns false.
    """

    def expiration_date(self):
        c = self.expiryDate - self.purchaseDate
        if c.days > 365:
            return f"{self.itemName} will expire in over a year"
        else:
            return f"{self.itemName} will expire in {self.expiryDate - self.purchaseDate} days"

def read_file(file_name):
    
    with open(f"{file_name}/", 'r') as file:
        csv_read = csv.reader(file)
        for row in csv_read:
            print(row)

# e_date = datetime.datetime(2021, 1, 23)
# p_date = datetime.datetime(2023, 1, 14)

# myItem = MyItems("Milk","Dairy",e_date,p_date)
# print(myItem.expiration_date())

# read_file("grocery_list.xlsx")

df = pd.read_excel(r'grocery_list.xlsx')

print(df)