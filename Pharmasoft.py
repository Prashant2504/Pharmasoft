from tkinter import *
import sqlite3

root = Tk()
root.title('Pharmasoft')

# Create a database
conn = sqlite3.connect('order.db')
c = conn.cursor()

# Create table 
'''
c.execute("""CREATE TABLE orders (
		first_name text,
		last_name text,
		phone_number integer,
		medicine_name text,
		quantity integer,
		price integer
		)""")
'''

def update():
	conn = sqlite3.connect('order.db')
	c = conn.cursor()

	record_id = delete_box.get()

	c.execute("""UPDATE orders SET
		first_name = :first,
		last_name = :last,
		phone_number = :phone_number,
		medicine_name = :medicine_name,
		quantity = :quantity,
		price = :price 
		WHERE oid = :oid""",
		{
		'first': f_name_editor.get(),
		'last': l_name_editor.get(),
		'phone_number': phone_number_editor.get(),
		'medicine_name': medicine_name_editor.get(),
		'quantity': quantity_editor.get(),
		'price': price_editor.get(),
		'oid': record_id
		})

	conn.commit()
	conn.close()
	editor.destroy()
	root.deiconify()

def edit():
	root.withdraw()
	global editor
	editor = Tk()
	editor.title('Update A Record')
	
	conn = sqlite3.connect('order.db')
	c = conn.cursor()

	record_id = delete_box.get()
	c.execute("SELECT * FROM orders WHERE oid = " + record_id)
	records = c.fetchall()
	

	global f_name_editor
	global l_name_editor
	global phone_number_editor
	global medicine_name_editor
	global quantity_editor
	global price_editor

	# Create Text Boxes
	f_name_editor = Entry(editor, width=30)
	f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
	l_name_editor = Entry(editor, width=30)
	l_name_editor.grid(row=1, column=1)
	phone_number_editor = Entry(editor, width=30)
	phone_number_editor.grid(row=2, column=1)
	medicine_name_editor = Entry(editor, width=30)
	medicine_name_editor.grid(row=3, column=1)
	quantity_editor = Entry(editor, width=30)
	quantity_editor.grid(row=4, column=1)
	price_editor = Entry(editor, width=30)
	price_editor.grid(row=5, column=1)
	
	# Create Text Box Labels
	f_name_label = Label(editor, text="First Name")
	f_name_label.grid(row=0, column=0, pady=(10, 0))
	l_name_label = Label(editor, text="Last Name")
	l_name_label.grid(row=1, column=0)
	phone_number_label = Label(editor, text="Phone Number")
	phone_number_label.grid(row=2, column=0)
	medicine_name_label = Label(editor, text="Medicine Name")
	medicine_name_label.grid(row=3, column=0)
	quantity_label = Label(editor, text="Quantity")
	quantity_label.grid(row=4, column=0)
	price_label = Label(editor, text="Price")
	price_label.grid(row=5, column=0)

	for record in records:
		f_name_editor.insert(0, record[0])
		l_name_editor.insert(0, record[1])
		phone_number_editor.insert(0, record[2])
		medicine_name_editor.insert(0, record[3])
		quantity_editor.insert(0, record[4])
		price_editor.insert(0, record[5])
	
	edit_btn = Button(editor, text="Save Record", command=update)
	edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

def delete():
	conn = sqlite3.connect('order.db')
	c = conn.cursor()

	c.execute("DELETE from orders WHERE oid = " + delete_box.get())
	delete_box.delete(0, END)

	conn.commit()
	conn.close()

def submit():
	conn = sqlite3.connect('order.db')
	c = conn.cursor()

	c.execute("INSERT INTO orders VALUES (:f_name, :l_name, :phone_number, :medicine_name, :quantity, :price)",
			{
				'f_name': f_name.get(),
				'l_name': l_name.get(),
				'phone_number': phone_number.get(),
				'medicine_name': medicine_name.get(),
				'quantity': quantity.get(),
				'price': price.get()
			})


	conn.commit()
	conn.close()

	f_name.delete(0, END)
	l_name.delete(0, END)
	phone_number.delete(0, END)
	medicine_name.delete(0, END)
	quantity.delete(0, END)
	price.delete(0, END)


def query():
	conn = sqlite3.connect('order.db')
	c = conn.cursor()

	c.execute("SELECT *, oid FROM orders")
	records = c.fetchall()

	print_records = ''
	for record in records:
		print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" +str(record[6]) + "\n"

	query_label = Label(root, text=print_records)
	query_label.grid(row=12, column=0, columnspan=2)

	conn.commit()
	conn.close()


# Create Text Boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)
phone_number = Entry(root, width=30)
phone_number.grid(row=2, column=1)
medicine_name = Entry(root, width=30)
medicine_name.grid(row=3, column=1)
quantity = Entry(root, width=30)
quantity.grid(row=4, column=1)
price = Entry(root, width=30)
price.grid(row=5, column=1)
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)


# Create Text Box Labels
f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0, pady=(10, 0))
l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)
phone_number_label = Label(root, text="Phone Number")
phone_number_label.grid(row=2, column=0)
medicine_name_label = Label(root, text="Medicine Name")
medicine_name_label.grid(row=3, column=0)
quantity_label = Label(root, text="Quantity")
quantity_label.grid(row=4, column=0)
price_label = Label(root, text="Price")
price_label.grid(row=5, column=0)
delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=9, column=0, pady=5)

# Create Submit Button
submit_btn = Button(root, text="Add Record To Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create a Query Button
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

#Create A Delete Button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

# Create an Update Button
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=143)


#Commit Changes
conn.commit()

# Close Connection 
conn.close()

root.mainloop()