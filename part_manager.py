import tkinter as tk
from tkinter import messagebox
from db import Database

db = Database('store.db')

class Application(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		master.title('Part Manager')
		master.geometry('700x380')

		self.createWidgets()
		self.selected_item = 0
		self.populate_list()

	def createWidgets(self):
		# Part
		self.part_text = tk.StringVar()
		self.part_label = tk.Label(self.master, text='Part Name', font=('bold', 14), pady=20)
		self.part_label.grid(row=0, column=0, sticky=tk.W)
		self.part_entry = tk.Entry(self.master, textvariable=self.part_text)
		self.part_entry.grid(row=0, column=1)

		# Customer
		self.customer_text = tk.StringVar()
		self.customer_label = tk.Label(self.master, text='Customer Name', font=('bold', 14))
		self.customer_label.grid(row=0, column=2, sticky=tk.W)
		self.customer_entry = tk.Entry(self.master, textvariable=self.customer_text)
		self.customer_entry.grid(row=0, column=3)

		# Retailer
		self.retailer_text = tk.StringVar()
		self.retailer_label = tk.Label(self.master, text='Retailer Name', font=('bold', 14))
		self.retailer_label.grid(row=1, column=0, sticky=tk.W)
		self.retailer_entry = tk.Entry(self.master, textvariable=self.retailer_text)
		self.retailer_entry.grid(row=1, column=1)

		# Price
		self.price_text = tk.StringVar()
		self.price_label = tk.Label(self.master, text='Price Name', font=('bold', 14))
		self.price_label.grid(row=1, column=2, sticky=tk.W)
		self.price_entry = tk.Entry(self.master, textvariable=self.price_text)
		self.price_entry.grid(row=1, column=3)

		# Parts List (Listbox)
		self.parts_list = tk.Listbox(self.master, height=8, width=50, border=0)
		self.parts_list.grid(row=3, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

		# Create Scrollbar
		self.scrollbar = tk.Scrollbar(self.master, orient="vertical")
		self.scrollbar.grid(row=3, column=3)
		# Set scroll to listbox
		self.parts_list.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.parts_list.yview)
		# Bind select
		self.parts_list.bind('<<ListboxSelect>>', self.select_item)

		# Buttons
		self.add_btn = tk.Button(self.master, text='Add Part', width=12, command=self.add_item)
		self.add_btn.grid(row=2, column=0, pady=20)

		self.remove_btn = tk.Button(self.master, text='Remove Part', width=12, command=self.remove_item)
		self.remove_btn.grid(row=2, column=1)

		self.update_btn = tk.Button(self.master, text='Update Part', width=12, command=self.update_item)
		self.update_btn.grid(row=2, column=2)

		self.clear_btn = tk.Button(self.master, text='Clear Input', width=12, command=self.clear_text)
		self.clear_btn.grid(row=2, column=3)

	def populate_list(self):
		self.parts_list.delete(0, tk.END)
		for row in db.fetch():
			self.parts_list.insert(tk.END, row)

	def add_item(self):
		partText = self.part_text.get()
		customerText = self.customer_text.get()
		retailerText = self.retailer_text.get()
		priceText = self.price_text.get()

		if partText == '' or customerText == '' or retailerText == '' or priceText == '':
			messagebox.showerror('Required Fields', 'Please fill the all fields')
			return

		insertTuple = (partText, customerText, retailerText, priceText)

		db.insert(partText, customerText, retailerText, priceText)
		self.parts_list.delete(0, tk.END)
		self.parts_list.insert(tk.END, insertTuple)

		self.clear_text()
		self.populate_list()

	def select_item(self, event):
		try:
			index = self.parts_list.curselection()[0]
			self.selected_item = self.parts_list.get(index)

			self.part_entry.delete(0, tk.END)
			self.part_entry.insert(tk.END, self.selected_item[1])

			self.customer_entry.delete(0, tk.END)
			self.customer_entry.insert(tk.END, self.selected_item[2])

			self.retailer_entry.delete(0, tk.END)
			self.retailer_entry.insert(tk.END, self.selected_item[3])

			self.price_entry.delete(0, tk.END)
			self.price_entry.insert(tk.END, self.selected_item[4])
		except IndexError:
			pass

	def remove_item(self):
		db.remove(self.selected_item[0])

		self.clear_text()
		self.populate_list()

	def update_item(self):
		partText = self.part_text.get()
		customerText = self.customer_text.get()
		retailerText = self.retailer_text.get()
		priceText = self.price_text.get()

		db.update(self.selected_item[0], partText, customerText, retailerText, priceText)
		self.populate_list()

	def clear_text(self):
		self.part_entry.delete(0, tk.END)
		self.customer_entry.delete(0, tk.END)
		self.retailer_entry.delete(0, tk.END)
		self.price_entry.delete(0, tk.END)

# Create window object
root = tk.Tk()
app = Application(master=root)
# Start program
app.mainloop()