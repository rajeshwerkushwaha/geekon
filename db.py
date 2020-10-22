import sqlite3
# conn = sqlite3.connect('geekon.db')
#
# c = conn.cursor()
#
# # Create table
# c.execute('''CREATE TABLE receipt_data (
#               file_uuid varchar(50) PRIMARY KEY,
#               merch_uuid varchar(50),
#               cust_uuid varchar(50),
#               raw_data text,
#               html_data text,
#               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             );''')
#
# c.execute('''CREATE TABLE receipt_items (
#               file_uuid varchar(50),
#               item_name text,
#               item_price real
#             );''')

# Insert a row of data
# query1 = "insert into receipt_data values('45f743a8-13c5-11eb-969c-acde48001122',
# result = c.execute(query1)
# for row in result:
#     print(row)


# Save (commit) the changes
# conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

def insertReceiptData(file_uuid, merch_uuid, raw_data, html_data):
    conn = sqlite3.connect('geekon.db')
    c = conn.cursor()
    query = '''insert into receipt_data (file_uuid, merch_uuid, raw_data, html_data) values
                ({},{},{},{})
            '''.format(file_uuid, merch_uuid, raw_data, html_data)
    print(query)
    result = c.execute(query)
    print(result)
    conn.commit()
    conn.close()
    # result = c.execute(query1)
