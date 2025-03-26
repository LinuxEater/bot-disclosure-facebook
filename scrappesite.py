import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, filedialog
import openpyxl  

def scrape_links():
    url = url_entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = [link.get('href') for link in soup.find_all("a") if link.get('href')]

        output_text.delete(1.0, tk.END)
        for link in links:
            output_text.insert(tk.END, link + "\n")

    except requests.exceptions.RequestException as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error: {e}\nCheck the URL and your internet connection.")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"An unexpected error occurred: {e}")

def save_to_excel():
    links = output_text.get(1.0, tk.END).splitlines()
    if not links:
        return  # Nothing to save

    filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not filepath:
        return  # User cancelled

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for index, link in enumerate(links):
        sheet.cell(row=index + 1, column=1, value=link)

    workbook.save(filepath)

def clear_output():
    output_text.delete(1.0, tk.END)

# Create main window
window = tk.Tk()
window.title("Buscador de Links")
window.geometry("600x600")

# URL input
url_label = tk.Label(window, text="URL:")
url_label.pack(pady=(10, 0))

url_entry = tk.Entry(window, width=50)
url_entry.insert(0, "")
url_entry.pack(pady=(5, 10))

# Scrape button
scrape_button = tk.Button(window, text="Scrape Links", command=scrape_links)
scrape_button.pack()

# Output area (scrolled text)
output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
output_text.pack(pady=(10, 10))

# Save to Excel button
save_excel_button = tk.Button(window, text="Save to Excel", command=save_to_excel)
save_excel_button.pack(pady=(5, 0))  # Add some vertical padding

# Clear output button
clear_button = tk.Button(window, text="Clear Output", command=clear_output)
clear_button.pack(pady=(5, 10))

window.mainloop()