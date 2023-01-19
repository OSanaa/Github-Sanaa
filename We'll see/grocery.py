"""
Project Name: Grocery Expiry Date Tracker
Project Creation Date: 1/9/2023
Description: This application keeps track of the expirey date of groceries.
(Maybe) Notifies phone once the 

"""

import datetime

'''
class myItems()
Description: myItems is a class of items kept in the fridge. 
The the class will have the attributes: itemName, itemType, expiryDate, purchaseDate
'''

class MyItems():
    def __init__(self, itemName, itemType, expiryDate, purchaseDate):
        self.itemName = itemName
        self.itemType = itemType
        self.expiryDate = expiryDate
        self.purchaseDate = purchaseDate
        print('{} has been created'.format(itemName))

    def __str__(self):
        return f"{self.itemName} was bought on {self.purchaseDate} and will expire on {self.expiryDate}. The item type is {self.itemType}"

    def expiration_date(self):
        c = self.expiryDate - self.purchaseDate
        if c.days > 365:
            return f"{self.itemName} will expire in over a year"
        else:
            return f"{self.itemName} will expire in {self.expiryDate - self.purchaseDate} days"

e_date = datetime.datetime(2025, 1, 23)
p_date = datetime.datetime(2023, 1, 14)

myItem = MyItems("Milk","Dairy",e_date,p_date)
print(myItem.expiration_date())
