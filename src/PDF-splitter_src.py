import tkinter as tk
from tkinter import ttk, messagebox
import os
import PyPDF2

# Function to split the PDF based on user inputs
def split_pdf():
    file_path = pdfPath.get()  # Gets the file path from the input field
    chunk_size = pageCount.get()  # Gets the number of pages per split from the input field
    output_folder = f"{file_path[:-4]}_output"  # Defines the output folder name

    # Check if the specified file exists and is a PDF
    if not os.path.exists(f"{file_path[:-4]}.pdf"):
        if not os.path.exists(file_path):
            messagebox.showerror("Fejl", f"Kunne ikke finde en fil kaldet \"{file_path}\"")
            return
        else:
            messagebox.showerror("Fejl", " Den oplyste fil er ikke en PDF")
            return

    # Check that the number of pages per split is greater than 0
    if chunk_size <= 0:
        messagebox.showerror("Fejl", "Sidetal skal være større end 0")
        return

    # Check if the output folder already exists, if not, create it
    if os.path.exists(output_folder):
        messagebox.showerror("Fejl", f"En mappe kaldet \"{output_folder}\" findes allerede.")
        return
    else:
        os.makedirs(output_folder)

    # Update window title to indicate the splitting process
    window.title("I gang med at splitte...")

    # Read the PDF and determine the total number of pages
    pdf_reader = PyPDF2.PdfReader(open(file_path, 'rb'))
    total_pages = len(pdf_reader.pages)

    # Split the PDF into chunks
    for start in range(0, total_pages, chunk_size):
        pdf_writer = PyPDF2.PdfWriter()
        end = min(start + chunk_size, total_pages)

        for page in range(start, end):
            pdf_writer.add_page(pdf_reader.pages[page])

        output_filename = f"{output_folder}/side_{start+1}_til_{end}.pdf"
        
        with open(output_filename, 'wb') as output_file:
            pdf_writer.write(output_file)

    # Update window title and show a success message
    window.title("PDF-splitter")
    messagebox.showinfo("Succes!", f"PDF blev splittet!\nOpdelte filer er gemt her:\n{output_folder}")

# Create a Tkinter window
window = tk.Tk()
window.title("PDF-splitter")
window.geometry('500x250')
window.resizable(False, False)

# Define color scheme
primary_color = '#f18c4d'  # Orange
secondary_color = '#B5693A'  # Darker orange
bg_color = '#112A3A'  # Dark blue
text_color = 'white'  # Text color

# Configure styles for Tkinter widgets
style = ttk.Style()
style.theme_use('default')
style.configure('TLabel', background=bg_color, foreground=text_color, font=('Calibri', 12))
style.configure('TFrame', background=bg_color)
style.configure('TEntry', padding=5)
style.configure('TButton', font=('Calibri', 12, 'bold'), borderwidth='4')
style.map('TButton', background=[('active', '!disabled', primary_color), ('pressed', secondary_color)],
          foreground=[('active', text_color), ('pressed', text_color)])

# Add a title label
title_label = ttk.Label(window, text="PDF-splitter", font=('Calibri', 30, 'bold'), background=bg_color, foreground=text_color)
title_label.pack(side='top', pady=(20, 0))

# Create a frame for input fields
input_frame = ttk.Frame(window, padding=(20, 10, 20, 10))
input_frame.pack(fill='both', expand=True)
input_frame['style'] = 'TFrame'

# Add labels and entry fields for file path and page count
ttk.Label(input_frame, text="Sti til PDF, som skal splittes:", style='TLabel').grid(row=0, column=0, sticky='w')
pdfPath = tk.StringVar()
pdfPath_entry = ttk.Entry(input_frame, textvariable=pdfPath, width=50)
pdfPath_entry.grid(row=1, column=0, sticky='ew')
ttk.Label(input_frame, text="Antal sider pr. split:", style='TLabel').grid(row=2, column=0, sticky='w')
pageCount = tk.IntVar()
pageCount_entry = ttk.Entry(input_frame, textvariable=pageCount, width=10)
pageCount_entry.grid(row=3, column=0, sticky='w')

# Add a button to trigger PDF splitting
split_button = ttk.Button(input_frame, text="SPLIT!", command=split_pdf)
split_button.grid(row=4, column=0, pady=(20, 0), sticky='ew')
split_button['style'] = 'TButton'

# Configure grid layout
input_frame.columnconfigure(0, weight=1)

# Set the main window's background color
window.configure(bg=bg_color)

# Run the Tkinter main loop
while 1:
    window.mainloop()

"""
Skrevet og udviklet af Lucas Hjort Rahr Hartung 
lhhar@aabenraa.dk
02/05/2024

"""