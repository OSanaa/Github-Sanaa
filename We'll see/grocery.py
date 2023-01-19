"""
Project Name: Grocery Expiry Date Tracker
Project Creation Date: 1/9/2023
Description: This application keeps track of the expirey date of groceries.
(Maybe) Notifies phone once the 

"""

import datetime
import csv

'''
class myItems()
Description: myItems is a class of items kept in the fridge. 
The the class will have the attributes: itemName, itemType, expiryDate, purchaseDate
Things to implement: 
    Create a GUI 
    Try to read in the csv file and show it in a format.
    Be able to reorder the list based on different attributes
    Add new items onto the CSV
'''

class MyItems():
    """
    MyItems is a class that represents item objects. Items will have 
    
    
    
    
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

e_date = datetime.datetime(2021, 1, 23)
p_date = datetime.datetime(2023, 1, 14)

myItem = MyItems("Milk","Dairy",e_date,p_date)
print(myItem.expiration_date())

