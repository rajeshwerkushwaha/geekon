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
# conn.close()

def insertReceiptData(file_uuid, merch_uuid, raw_data, html_data):
    conn = sqlite3.connect('geekon.db')
    c = conn.cursor()
    query = '''insert into receipt_data (file_uuid, merch_uuid, raw_data, html_data) values
                ('{}','{}','{}','{}')
            '''.format(file_uuid, merch_uuid, raw_data, html_data)
    # print(query)
    result = c.execute(query)
    # print(result)
    conn.commit()
    conn.close()


def insertReceiptInfo(file_uuid, data):
    conn = sqlite3.connect('geekon.db')
    c = conn.cursor()

    for d in data:
        query = '''insert into receipt_items (file_uuid, item_name, item_price) values
                    ('{}','{}','{}')
                '''.format(file_uuid, d[0], d[1])
        print(query)
        result = c.execute(query)
    # print(result)
    conn.commit()
    conn.close()


def getItemFromDB(item):
    conn = sqlite3.connect('geekon.db')
    c = conn.cursor()
    query = '''select rd.merch_uuid, ri.item_name, ri.item_price
                from receipt_data as rd
                join receipt_items as ri
                    on rd.file_uuid = ri.file_uuid
                where ri.item_name like '%{}%'
            '''.format(item)
    # print(query)
    c.execute(query)
    result = c.fetchall()
    # print(result)
    conn.commit()
    conn.close()
    return result

#
#
# select rd.file_uuid, rd.merch_uuid, ri.item_name, ri.item_price
# from receipt_data as rd
# join receipt_items as ri
#     on rd.file_uuid = ri.file_uuid
# where ri.item_name like '{}'
#
#
#
# insert into receipt_data (file_uuid, merch_uuid, raw_data, html_data) values
# ('d708ccc8-147a-11eb-91aa-acde48001122','fcb916ac-147b-11eb-8e23-acde48001122','raw_data', '''<body>
# <div class="esc-receipt">
# <div class="esc-line esc-justify-center"><img alt="Image 300x236" class="esc-bitimage" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAADsAQAAAADmmabYAAAABGdBTUEAALGPC/xhBQAAAAJiS0dEAAHdihOkAAAAB3RJTUUH5AoWDysK4zqwnAAAAolJREFUaN7t2TGLIyEUB/AnQiy9cosl3kfYMkVYv1aKYcdwX8yQ4r6GYYstz9JCxnvPmHFuk0y2OHI5cPjjQPIjTJ5PBAfSVy4PjTX2l5iFGxfPzHyN3VLA/h3jt8qxbayxxhpr7H5MNDbPjEqgcPQbkRzusvhRfGZJmH7nVGUgBxAY/53hZo3bOrInSAvQOyNHhiACx3jcFAF6A32KeF+AsiBGFgUPigVgHmAA0NxpYhpAWtzpTyyobdA7HL00UTgtAjK0sJH2dcp2XmOsV7aTfpmZ8IpFaXs2MgL6OLpOhiUVIsqgeBQW0ZSplKXbqLDkJzZ8ZoEl1xNbqSBBI1PnDCCAysyvVJRUnA6ZOGMRRGUGrrEEvDIH3TVmWWUB1hcZPTKrfyGZ52ssmbEgCuudC3KJ2bG811hQP33v6mTJqGiyNLHJZOU5RYNTbzvhXwX9GrUAsrc69VEyNGHBPIeBYVPgU0RmM3vmk7bk2Gy1LbHVclsSm7Rlyt2bm5xTk+fuxSYnNmnyZHAtSFw1/iUvGcvKkkFmJ0vG99QfLvlXfHYqBnWITLlM/fk6zQU8Xqgzu7ScG3vAXaaxxhq7B3sfFASxfz8k03X84GWgW5KGxsr2g4QN3x8OCTb4jUO2Zo011lhjjTV2X4Z7VmX+Cnvkbbexxhp7dBZ0Cv3nRD2mMDrfOkbXHE9scgpzMpWoGi/HFGZFKpE1TowpzPBUImosH1MYHdAcw2sMG7M9vZIbStiYRKdjJYUx6CaJOQODt1PKCz5uVpNscjpu1qcUJuy3SV5yVsI+nVKYdPMpTPn5FKbDfArr4/UMOBaWhvkcGZvNlkZiP2azp5HYr0v5+COP/ha7scb+U/Ybf0wPkvQsJyoAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMTAtMjJUMTU6NDM6MTArMDA6MDAtA3JqAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTEwLTIyVDE1OjQzOjEwKzAwOjAwXF7K1gAAAABJRU5ErkJggg==" width="150px"/></div>
# <div class="esc-line esc-justify-center"><span class="esc-text-scaled esc-width-2">ExampleMart Ltd.</span></div>
# <div class="esc-line esc-justify-center">Shop No. 42.</div>
# <div class="esc-line esc-justify-center"> </div>
# <div class="esc-line esc-justify-center"><span class="esc-emphasis">SALES INVOICE</span></div>
# <div class="esc-line"><span class="esc-emphasis">                                               $</span></div>
# <div class="esc-line">Example item #1                             4.00</div>
# <div class="esc-line">Another thing                               3.50</div>
# <div class="esc-line">Something else                              1.00</div>
# <div class="esc-line">A final item                                4.45</div>
# <div class="esc-line"><span class="esc-emphasis">Subtotal                                   12.95</span></div>
# <div class="esc-line"> </div>
# <div class="esc-line">A local tax                                 1.30</div>
# <div class="esc-line"><span class="esc-text-scaled esc-width-2">Total            $ 14.25</span></div>
# <div class="esc-line"> </div>
# <div class="esc-line esc-justify-center">Thank you for shopping at ExampleMart</div>
# <div class="esc-line esc-justify-center">For trading hours, please visit example.com</div>
# <div class="esc-line esc-justify-center"> </div>
# <div class="esc-line esc-justify-center">Monday 6th of April 2015 02:56:25 PM</div>
# <div class="esc-line esc-justify-center"> </div>
# </div>
# </body>''')
