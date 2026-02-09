'''
Project Name: Personal Dashboard
Author: Sanaa
Date: 01/28/2025
Description: The Personal Dashboard will allow for keeping track of finances, help out with monthly grocery needs.
    - Finance: The dashboard will prompt monthly spending recommendation as well as saving recommendations based 
    monthy income, spending habits, as well as monthly expenses.
    - Grocery: The dashboard will look into and analyze how often a particular item is used and consumed on a 
    bi-weekly basis and will add to a "shopping cart" list of items that need to be bought at a certain date.
    The list will be included automatically to google calendar.
'''

import pandas as pd
import sqlite3

def create_tables(conn, cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions
                   (Transaction_ID INTEGER, Name varchar(100), Group_Type varchar(100), Category varchar(100), Amount numeric(7,2), PRIMARY KEY("Transaction_ID" AUTOINCREMENT))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Card_Transactions
                   (Transaction_Date date, Posted_Date date, Card_Number int, Description varchar(100), Category varchar(100), Standardized_Category varchar(100), Debit numeric(7,2), Credit numeric(7,2))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Category_Correction
                   (Item_ID INTEGER, Item_Name varchar(100), Category_Name varchar(100), PRIMARY KEY("Item_ID" AUTOINCREMENT))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Standardized_Categories
                   (Category_ID INTEGER, Standardized_Name varchar(100), Keywords text, PRIMARY KEY("Category_ID" AUTOINCREMENT))''')
    
    # Check if Standardized_Category column exists, if not add it
    try:
        cursor.execute("ALTER TABLE Card_Transactions ADD COLUMN Standardized_Category varchar(100)")
        conn.commit()
        print("Added Standardized_Category column to existing Card_Transactions table")
    except sqlite3.OperationalError:
        # Column already exists, ignore error
        pass
    
    conn.commit()

def convert_category(expenses_dict, description):
    """
    Convert transaction description to standardized category based on keywords.
    Returns the standardized category name or 'Uncategorized' if no match found.
    """
    description_lower = description.lower()
    
    for category, keywords in expenses_dict.items():
        for keyword in keywords:
            if keyword.lower() in description_lower:
                return category
    
    return 'Uncategorized'

def populate_standardized_categories(conn, cursor, expenses_dict):
    """
    Populate the Standardized_Categories table with the expenses dictionary.
    """
    # Clear existing data
    cursor.execute("DELETE FROM Standardized_Categories")
    
    for category, keywords in expenses_dict.items():
        keywords_str = ', '.join(keywords)
        cursor.execute('''INSERT INTO Standardized_Categories (Standardized_Name, Keywords) 
                          VALUES (?, ?)''', (category, keywords_str))
    
    conn.commit()
    print(f"Populated {len(expenses_dict)} standardized categories")

def process_transactions(conn, cursor, df, expenses_dict):
    """
    Process the transaction data and insert into database with standardized categories.
    """
    # Clear existing data
    cursor.execute("DELETE FROM Card_Transactions")
    
    processed_count = 0
    for _, row in df.iterrows():
        # Convert description to standardized category
        standardized_category = convert_category(expenses_dict, row['Description'])
        
        # Insert into database
        cursor.execute('''INSERT INTO Card_Transactions 
                          (Transaction_Date, Posted_Date, Card_Number, Description, Category, 
                           Standardized_Category, Debit, Credit) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (row['Transaction Date'], row['Posted Date'], row['Card No.'], 
                       row['Description'], row['Category'], standardized_category,
                       row['Debit'] if pd.notna(row['Debit']) else None,
                       row['Credit'] if pd.notna(row['Credit']) else None))
        processed_count += 1
    
    conn.commit()
    print(f"Processed {processed_count} transactions")

def display_category_summary(conn, cursor):
    """
    Display a summary of transactions by standardized category.
    """
    cursor.execute('''SELECT Standardized_Category, COUNT(*) as count, 
                      SUM(COALESCE(Debit, 0) - COALESCE(Credit, 0)) as total_amount
                      FROM Card_Transactions 
                      GROUP BY Standardized_Category 
                      ORDER BY total_amount DESC''')
    
    results = cursor.fetchall()
    print("\n=== Transaction Summary by Standardized Category ===")
    print(f"{'Category':<20} {'Count':<8} {'Total Amount':<15}")
    print("-" * 50)
    
    for category, count, amount in results:
        print(f"{category:<20} {count:<8} ${amount:<14.2f}")

def add_category_keywords(conn, cursor, category_name, new_keywords):
    """
    Add new keywords to an existing category or create a new category.
    """
    # Check if category exists
    cursor.execute("SELECT Keywords FROM Standardized_Categories WHERE Standardized_Name = ?", (category_name,))
    result = cursor.fetchone()
    
    if result:
        # Category exists, update keywords
        existing_keywords = result[0].split(', ') if result[0] else []
        all_keywords = list(set(existing_keywords + new_keywords))
        keywords_str = ', '.join(all_keywords)
        
        cursor.execute("UPDATE Standardized_Categories SET Keywords = ? WHERE Standardized_Name = ?", 
                      (keywords_str, category_name))
        print(f"Updated category '{category_name}' with new keywords: {', '.join(new_keywords)}")
    else:
        # Create new category
        keywords_str = ', '.join(new_keywords)
        cursor.execute("INSERT INTO Standardized_Categories (Standardized_Name, Keywords) VALUES (?, ?)", 
                      (category_name, keywords_str))
        print(f"Created new category '{category_name}' with keywords: {', '.join(new_keywords)}")
    
    conn.commit()

### Change the following to different categories
### Other Travel -> Travel, Merchandise -> Shopping
expenses_category_dict = {"Subscription": ["Amazon Prime", "Spotify"], "Groceries":["Safeway", "Costco", "Hmart"], "Fitness": ["Chuze Fitness"], "Travel": ["COT*FLT"], "Internet" : ["Quantum Fiber"],"Entertainment" : ["Nintendo"], }

# Main execution
conn = sqlite3.connect('card_transaction.db')
cursor = conn.cursor()

# Create all tables
create_tables(conn, cursor)

# Load transaction data
df = pd.read_csv('2025-01-30_transaction_download.csv')

# Populate standardized categories table
populate_standardized_categories(conn, cursor, expenses_category_dict)

# Process transactions and apply standardized categories
process_transactions(conn, cursor, df, expenses_category_dict)

# Display summary
display_category_summary(conn, cursor)

# Show some examples of categorized transactions
print("\n=== Sample Categorized Transactions ===")
cursor.execute('''SELECT Description, Category, Standardized_Category, Debit, Credit 
                  FROM Card_Transactions 
                  WHERE Standardized_Category != 'Uncategorized'
                  LIMIT 10''')

results = cursor.fetchall()
print(f"{'Description':<30} {'Original':<15} {'Standardized':<15} {'Amount':<10}")
print("-" * 80)

for desc, orig_cat, std_cat, debit, credit in results:
    amount = debit if debit else -credit if credit else 0
    print(f"{desc[:29]:<30} {orig_cat:<15} {std_cat:<15} ${amount:<9.2f}")

conn.close()