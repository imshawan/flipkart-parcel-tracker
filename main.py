import tkinter as tk
from tkinter import *
from tkinter import Text
import requests, sys
import pandas as pd
from tkinter import messagebox
from bs4 import BeautifulSoup

root = tk.Tk()
root.title('Ekart Tracker - Track Your Flipkart Parcels')
root.resizable(0,0)

def outputconsole(response):
	for things in outputconsole1.winfo_children():
		things.destroy()
	output = tk.Text(outputconsole1, width=650)
	output.insert(tk.INSERT, f'{response}')
	output.config(state='disabled')
	output.place(x=1,y=1)

def outputconsolee(response_detailed):
	for things in outputconsole2.winfo_children():
		things.destroy()
	output = tk.Text(outputconsole2, width=650)
	output.insert(tk.INSERT, f'{response_detailed}')
	output.config(state='disabled')
	output.place(x=1, y=1)

def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
		return [td.get_text(strip=True) for td in tr.find_all(coltag)]

def track():
	rows1 = []
	rows = []
	trackingID = textbox.get("1.0", 'end-1c')
	if trackingID == "":
		messagebox.showwarning('Warning!', "Enter Tracking ID first!")
		return
	try:
		r = requests.get(f'https://ekartlogistics.com/track/{trackingID}/').text
	except:
		messagebox.showerror('Error!', "No Internet! Retry after connecting to the internet")
		return

	soup = BeautifulSoup(r, 'html.parser')
	table1 = soup.find( "table", { 'class' : 'col-md-12 table-bordered table-striped table-condensed cf width-100' } )
	table = soup.findAll( "table", { 'class' : 'col-md-12 table-bordered table-striped table-condensed cf width-100' } )

	try:
		trsf = table1.find_all('tr')
	except AttributeError:
		messagebox.showerror('Error!', "Invalid Tracking ID!")
		return
	headerow1 = rowgetDataText(trsf[0], 'th')
	if headerow1: 
		rows1.append(headerow1)
		trsf = trsf[1:]
	for tr in trsf: 
		rows1.append(rowgetDataText(tr, 'td') )     
	headerow1 = rowgetDataText(trsf[0], 'th')
	dftable1 = pd.DataFrame(rows1[1:], columns=rows1[0])
	outputconsole(dftable1)

	#-------------------Detailed Tracking info:----------------------
	for tables in table:
		trs1 = tables.findAll('tr')
	trs = trs1
	headerow = rowgetDataText(trs[0], 'th')
	if headerow: # if there is a header row include first
		rows.append(headerow)
		trs = trs[1:]
	for tr in trs: # for every table row
		rows.append(rowgetDataText(tr, 'td') ) # data row       
	headerow = rowgetDataText(trs[0], 'th')

	dftable = pd.DataFrame(rows[1:], columns=rows[0])

	outputconsolee(dftable)

def reset():
	for things in outputconsole1.winfo_children():
		things.destroy()
	for things in outputconsole2.winfo_children():
		things.destroy()
	textbox.delete("1.0", "end")

def close():
	sys.exit()
#User Interface design

Canvas = tk.Canvas(root, height=580, width=800)
Canvas.pack()
master = tk.Frame(root)
master.config(borderwidth=1, highlightthickness=1, highlightbackground='#bebebe', bg='#f0f0f0')
master.place(height=470, width=760, x=21, y=75)

head = tk.Label(root, text="Ekart Package Tracker")
head.config(font=('Rockwell',30), fg='black')
head.place(x=185, y=10)
text1 = tk.Label(master, text="Enter your Tracking ID: ")
text1.config(font=('AdobeClean-Bold',11))
text1.place(x=50, y=20)
textbox = Text(master, height=1, width=21)
textbox.config(highlightthickness=0.5, highlightbackground='grey')
textbox.place(x=212, y=21)
Button = tk.Button(master,text="Track", width=10, bd=1, command=track)
Button.config(bg='#e1e1e1')
Button.place(x=416, y=20)
resetbtn = tk.Button(master,text="Reset", width=10, bd=1, command=reset)
resetbtn.config(bg='#e1e1e1')
resetbtn.place(x=513, y=20)
closebtn = tk.Button(master,text="Close", width=10, bd=1, command=close)
closebtn.config(bg='#e1e1e1')
closebtn.place(x=610, y=20)

outLabel = tk.Label(master, text="Current Tracking Status:")
outLabel.place(x=28, y=60)
outputconsole1 = tk.Frame(master, height=80, width=700, bg='white')
outputconsole1.place(x=28, y=90)
outLabe2 = tk.Label(master, text="Detailed Tracking Information:")
outLabe2.place(x=28, y=190)
outputconsole2 = tk.Frame(master, height=200, width=700, bg='white')
outputconsole2.place(x=28, y=230)
copyryt = tk.Label(root, text=" © 2020 Shawan Mandal ", fg='grey')
copyryt.place(x=325, y=535)
root.mainloop()
