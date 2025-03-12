all_orders=[]
revenue=0
profit=0
#database connection
import mysql.connector
def create_database(database_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YUvaraj91@@"
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created or already exists.")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error creating the database '{database_name}': {err}")
def get_connection(database_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YUvaraj91@@",
            database=database_name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database '{database_name}': {err}")
        return None

def create_table(connection, table_name, columns):
    try:
        cursor = connection.cursor()
        columns_definition = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {columns_definition}
            )
        """
        print("generated query")
        print(create_table_query)
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"An error occured: {err}")

def insert_data(connection, table_name, columns, data):
    cursor = connection.cursor()

    # Ensure the columns are joined into a string for the SQL query
    columns_str = ", ".join(columns)
    
    # Generate placeholders for the values based on the number of columns
    placeholders = ", ".join(["%s"] * len(columns))
    
    # SQL query for inserting data
    insert_query = f"""
    INSERT INTO {table_name} ({columns_str}) 
    VALUES ({placeholders}) 
    ON DUPLICATE KEY UPDATE id=id
    """
    
    # Insert each row of data
    for row in data:
        cursor.execute(insert_query, tuple(row))  # Execute query with the tuple of values
    
    # Commit the transaction
    connection.commit()
    print(f"Data inserted into '{table_name}'.")

    cursor.close()

def main(database_name):
    connection=None
    try:
        create_database(database_name)
        connection = get_connection(database_name)

        # Get table name and columns
        l=[]
        while True:
            table_name = input("Enter the table name: ")
            print("Enter columns in the format: name datatype (e.g., 'item VARCHAR(255)', 'price DECIMAL(10,2)')")
            columns_input = input("Enter columns separated by dash-: ")
            columns = {}
            column_names=[]
            #creating columns and its data type dictionary
            for col in columns_input.split("-"):
                col = col.strip()  # Remove leading/trailing spaces
                first_space_index = col.find(" ")  # Find the first space to separate name and type
                if first_space_index != -1:  # Ensure there is at least one space
                    column_name = col[:first_space_index]
                    column_names.append(column_name)
                    column_type = col[first_space_index + 1:]
                    columns[column_name] = column_type
                else:
                    print(f"invalid column format: '{col}'")
                    return
            print(columns)

            create_table(connection, table_name, columns)
            

            # Insert data
            print("Enter multiple rows separated by new lines. Type 'done' when finished.")
            rows = []
            while True:
                row_input = input("Enter row data (comma-separated values): ")
                if row_input.lower() == "done":
                    break
                row_values = row_input.split(",")  # Split the input into individual values
                if len(row_values) != len(columns):
                    print(f"Invalid input. Expected {len(columns)} values, got {len(row_values)}.")
                    continue
                rows.append(tuple(row_values))  # Convert to tuple for database insertion


            insert_data(connection, table_name,column_names, rows)

            print("All operations completed successfully.")
            l.append(table_name)
            choice=input("do you want to add another table:yes/no: ")
            if choice=="no":
                break
        print("the below tables and its data are updated in database")
        print(l)

    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")

    finally:
        if connection and connection.is_connected():
            connection.close()

database_name =input("Enter the database name: ")
main(database_name)


from tabulate import tabulate

#database connection
#view MENU
def view_menu(table, database):
    try:
        print(f"Attempting to fetch data from table: '{table}' in database: '{database}'")

        connection = get_connection(database)
        if not connection:
            print(f"Failed to connect to the database '{database}'.")
            return
        
        cursor = connection.cursor()

        # Debug: Before query execution
        print(f"Executing query: SELECT * FROM `{table}`")
        query = f"SELECT * FROM `{table}`"  # Use backticks to handle special characters in table names
        cursor.execute(query)

        # Debug: After query execution
        print(f"Query executed successfully for table: '{table}'")

        # Fetch column names and rows
        columns = [i[0] for i in cursor.description]  # Column names
        rows = cursor.fetchall()  # Fetch all rows

        # Display the table with proper formatting
        if rows:
            print(f"\n{'*' * 10} {table.upper()} MENU {'*' * 10}") 
            print(tabulate(rows, headers=columns, tablefmt="grid"))
        else:
            print(f"No data found in the '{table}' table.")

    except mysql.connector.Error as e:
        print(f"Database error while fetching the menu for table '{table}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred for table '{table}': {e}")
    finally:
        # Close resources
        try:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
        except Exception as e:
            print(f"Error closing resources for table '{table}': {e}")


#ADDING ITEM TO THE CART
def add_cart(table,item_id,quantity,database):
    
    try:
        connection = get_connection(database)
        cursor = connection.cursor()
        query = f"SELECT * FROM `{table}`"
        cursor.execute(query)
        columns = [i[0] for i in cursor.description]
        print(columns)
        cursor.close()
        connection.close()
        print("select columns you want to add.type done when you done")
        b=[]
        while True:
            ans=input("enter column name or done to complete: ")
            if ans=="done":
                break
            elif ans in columns:
                b.append(ans)
            else:
                print("invalid column name: ")
                
        if b:
            connection = get_connection(database)
            cursor = connection.cursor()
            selected_columns = ", ".join([f"`{col}`" for col in b]) 
            query = f"SELECT {selected_columns} FROM `{table}` WHERE id = %s"
            cursor.execute(query,(item_id,))
        result = cursor.fetchone()
            
        if result:
            item_name, price,cost = result
            money = quantity * price
                
            d[item_name] = [quantity, money, table, item_id,cost,price]
            print(f"Added '{item_name}' to the cart with quantity {quantity} and total price {money}.")
        else:
            print(f"No item found with ID '{item_id}' in table '{tableitem}'.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        cursor.close()
        connection.close()
        
#MODIFY CART ITEM QUANTITY
def modify_quantity(tableitem,item,item_id,quantity):
    if item in d:
        d[item][0]+=quantity
        s_money=d[item][1]
        money=s_money*quantity
        d[item][1]+=money
        
    
def delete_cust_cart_item(item):
    if item in d:
        d.pop(item)
        print(f"Item '{item}' has been removed from the cart.")
    else:
        print(f"Item '{item}' not found in the cart.")
    
def add_items(typ,b,c,d):
        try:
            connection=get_connection()
            cursor=connection.cursor()
            query=f"""insert into {typ} (item,price) values (%s,%s)"""
            new_row=(b,c)
            cursor.execute(query,new_row)
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Row with item '{b}' added from table '{typ}'.")
            else:
                print(f"No matching row found for item '{b}' in table '{typ}'.")
            if typ in globals() and isinstance(globals()[typ], list):
                try:
                    globals()[typ].append(d)
                    print(f"Item '{b}' added from the global list '{typ}'.")
                except ValueError:
                    print(f"Item '{b}' not found in the global list '{typ}'.")
            else:
                print(f"No matching global list found for '{typ}'.")
        except Exception as e:
            print(f" an error {e} is occured")
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'connection' in locals() and connection is not None:
                connection.close()
    
            
def del_item(typ,b):
    valid_table=["veg","nonveg","starters","cool_drinks","deserts"]
    if typ in valid_table:
        try:
            connection=get_connection(database_name)
            cursor=connection.cursor()
            query=f"""delete from {typ} where id=%s"""
            cursor.execute(query,(b,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Row with item '{b}' deleted from table '{typ}'.")
            else:
                print(f"No matching row found for item '{b}' in table '{typ}'.")
            if typ in globals() and isinstance(globals()[typ], list):
                try:
                    globals()[typ].pop(b-1)
                    print(f"Item '{b}' removed from the global list '{typ}'.")
                except ValueError:
                    print(f"Item '{b}' not found in the global list '{typ}'.")
            else:
                print(f"No matching global list found for '{typ}'.")
        except Exception as e:
            print(f" an error {e} is occured")
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'connection' in locals() and connection is not None:
                connection.close()
    else:
        print(f"invalid table name: '{a}'")
def modify_menu(itemty,itemnm,itemput):
    valid_table=["veg","nonveg","starters","cool_drinks","deserts"]
    if itemty in valid_table:
        try:
            connection=get_connection()
            cursor=connection.cursor()
            if not itemty.isidentifier():
                raise ValueError(f"invalid table name:{itemty}")
            if str(itemnm).isdigit():
                query=f"""update {itemty} set price=%s where price=%s"""
            else:
                query=f"""update {itemty} set item=%s where item=%s"""
            cursor.execute(query,(itemput,itemnm))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Successfully updated {itemnm} to {itemput} in table {itemty}.")
            else:
                print(f"No matching record found to update in table {itemty}.")
        except Exception as e:
            print("An error occured",e)
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
    else:
        print(f"invalid table name:'{itemty}'")
def view_all_orders():
    h=1
    for i in all_orders:
        details=i
        print("CUSTOMER-",h)
        for key,val in details.items():
            print(key,"no of plates- :",val)
        h=h+1
def day_wise_profit_and_revenue():
    print("*"*10,"REVENUE OF THE RESTAURENT","*"*10)
    print("OVERALL REVENUE IS",revenue)
    print("*"*10,"PROFIT OF THE RESTAURENT","*"*10)
    print("OVERALL PROFIT IS",profit)

while True:
    user=int(input("1.customer/2.manager/3.exit:::enter the number "))
    if user==2:
        print("1.adding items :")
        print("2.delete items:  ")
        print("3.modify items from menu :")
        print("4.view all orders :")
        print("5.day wise profit :")
        while True:
            num=int(input("enter the number to access: "))
            if num==1:
                print("*"*10,"ADDING ITEMS FOR DIFFERENT CATEGORIES","*"*10)
                while True:
                    typ=input("give the type:veg/nonveg/starters/cool_drinks/deserts")
                    item=input("give the item name: ")
                    p=int(input("give the selling_price"))
                    q=int(input("give the cost price"))
                    add_items(typ,item,p,q)
                    inp=input("do you want to continue changing:yes/no ")
                    if inp=="no":
                        break
            elif num==2:
                print("*"*10,"DELETING ITEMS","*"*10)
                while True:
                    typ=input("give the type:veg/nonveg/starters/cool_drinks/deserts")
                    itemid=input("give the ID of the item")
                    del_item(typ,itemid)
                    inp=input("do you want to continue changing:yes/no ")
                    if inp=="no":
                        break
            elif num==3:
                while True:
                    print("do you want to change the 1.itemname/2.item price give your answer")
                    itemty=input("give the item type:veg/nonveg/starters/cool_drinks/deserts")
                    itemnm=input("give the item name/item price you want to change")
                    itemput=input("give the item name/price you want to put")
                    modify_menu(itemty,itemnm,itemput)
                    inp=input("do you want to continue changing:yes/no ")
                    if inp=="no":
                        break
                
                    
            elif num==4:
                view_all_orders()
            elif num==5:
                day_wise_profit_and_revenue()
            else:
                print("give valid number")
            CHOICE=input("do you want to continue:yes/no :")
            if CHOICE=="no":
                break
                
                    
    elif user==1:
        print("1.view menu")
        print("2.Add to cart")
        print("3.modify cart")
        print("4.Bill")
        d={}
        while True:
            num=int(input("enter the number:1/2/3/4: "))
            if num==1:
                print("*"*10,"MENU","*"*10)
                connection=get_connection(database_name)
                cursor=connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                print("Tables found:", tables)

                j = 1
                for tab in tables:
                    print(f"Processing table {j}: {tab}")
                    try:
                        view_menu(tab, database_name)  # Call the view_menu function
                    except Exception as e:
                        print(f"An error occurred while viewing the menu for table '{tab}': {e}")
                    j += 1
                cursor.close()
                connection.close()
            elif num==2:
                print("*"*10,"ADDING TO CART","*"*10)
                print("select type of recepies from the menu")
                connection=get_connection(database_name)
                cursor=connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                print(tables)
                while True:
            
                    ch=input("give the choice of type in a table shown")
                    item_id=int(input("give the item id of the dish: "))
                    quantity=int(input("give the number of plates: "))
                    add_cart(ch,item_id,quantity,database_name)
                    choice=input("do you want to add any more items:yes/no: ").strip().lower()
                    if choice=="no":
                        cursor.close()
                        connection.close()
                        break
                        
                                    
            elif num==3:
                print("*"*10,"MODINFYING CART","*"*10)
                while True:
                    print("choose you want to delete an item or modify the quantity ,")
                    action=input("give one of them:modify/delete: ")
                    typ=input("give the type:veg/nonveg/starters/cool_drinks/deserts")
                    itm_id=int(input("enter the item id: "))
                    if action=="modify":
                        item=input("give the item name: ")
                        quant=int(input("enter a value to increase or decrease the quantity: "))
                        modify_quantity(typ,item,itm_id,quant)
                    elif action=="delete":
                        item=input("give the item name: ")
                        delete_cust_cart_item(item)
                    ans=input("do you want to continue changing:yes/no: ").strip().lower()
                    if ans=="no":
                        break
                        
            elif num==4:
                print("*"*10,"BILL CART","*"*10)
                orders={}
                total=0
                for i in d:
                    if d[i][0]==0:
                        continue
                    orders[i]=d[i][0]
                    total+=d[i][1]
                    print(f"{i}-Rupees: {d[i][1]}")
                    c_p=d[i][4]*d[i][0]
                    s_p=d[i][5]*d[i][0]
                    profit += (s_p- c_p)
                   
                print("TOTAL AMOUNT IS: ",total)
                revenue+=total
                all_orders.append(orders)
            else:
                print("give valid number: ")
            choic=input("Do want to quit:yes/no ")
            if choic=="yes":
                break
                
                    
    elif user==3:
        print("thank you for visiting our restaurent: ")
        break
    else:
        print("invalid user")
    choice=input("do you want to continue manager/customer:yes/no")
    if choice=="no":
        break
    elif choice=="yes":
        print("ok")


        
