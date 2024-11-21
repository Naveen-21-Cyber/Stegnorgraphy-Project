import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import stepic
import fitz  

# Function to select the input image file
def select_image_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    print(f"Selected file path: {file_path}")
    
    # Check if the user selected a file
    if file_path:
        image_file_entry.delete(0, tk.END)  
        image_file_entry.insert(0, file_path)  
    else:
        messagebox.showwarning("Warning", "No image file selected!")

# Function to select the text or PDF file to hide
def select_text_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
    text_file_entry.delete(0, tk.END)
    text_file_entry.insert(0, file_path)

# Function to read text from a file (supports .txt and .pdf)
def read_text_from_file(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:  # Ensure UTF-8 encoding for text files
            return file.read()
    elif file_path.endswith('.pdf'):
        pdf_document = fitz.open(file_path)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        return text
    else:
        raise ValueError("Unsupported file type")

# Function to perform steganography
def perform_steganography():
    try:
        image_path = image_file_entry.get().strip()
        output_filename = output_entry.get().strip()
        print(f"Image Path: {image_path}")
        print(f"Output Filename: {output_filename}")

        # Check if the image and output filename fields are filled
        if not image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        if not output_filename:
            messagebox.showerror("Error", "Please enter an output filename.")
            return

        selected_option = option.get()
        if selected_option == "password":
            password = password_entry.get().strip()
            if not password:
                messagebox.showerror("Error", "Please enter a password.")
                return
            hidden_content = password.encode()  # Convert password to bytes
        elif selected_option == "file":
            text_path = text_file_entry.get().strip()
            if not text_path:
                messagebox.showerror("Error", "Please select a text or PDF file.")
                return
            hidden_content = read_text_from_file(text_path).encode()
        else:
            messagebox.showerror("Error", "Invalid option selected.")
            return

        # Perform steganography
        image = Image.open(image_path)
        encoded_image = stepic.encode(image, hidden_content)

        # Save the encoded image
        encoded_image.save(output_filename, 'PNG')
        messagebox.showinfo("Success", f"Steganography completed. Output saved as '{output_filename}'.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to select the steganography image file for decoding
def select_steg_image_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    steg_image_file_entry.delete(0, tk.END)
    steg_image_file_entry.insert(0, file_path)

# Function to decode the hidden message from the image
def decode_steganography():
    try:
        steg_image_path = steg_image_file_entry.get().strip()
        output_text_filename = decode_output_entry.get().strip()

        # Debugging: Print paths
        print(f"Steg Image Path: {steg_image_path}")
        print(f"Output Text Filename: {output_text_filename}")

        if not steg_image_path or not output_text_filename:
            messagebox.showerror("Error", "Please fill all the fields")
            return

        steg_image = Image.open(steg_image_path)
        hidden_text = stepic.decode(steg_image)

        with open(output_text_filename, 'w', encoding='utf-8') as file:  # Ensure UTF-8 encoding for text output
            file.write(hidden_text)

        messagebox.showinfo("Success", f"Hidden content extracted and saved as {output_text_filename}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to refresh/reset the input fields
def refresh_fields():
    image_file_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    text_file_entry.delete(0, tk.END)
    output_entry.delete(0, tk.END)
    steg_image_file_entry.delete(0, tk.END)
    decode_output_entry.delete(0, tk.END)
    option.set("password")

# Set up the GUI
root = tk.Tk()
root.title("Steganography Tool")

# Set up colors and styles
bg_color = "#f0f0f0"
button_color = "#4caf50"
button_fg_color = "#ffffff"
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")

root.configure(bg=bg_color)

# Image file selection
tk.Label(root, text="Select Image File:", bg=bg_color, font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
image_file_entry = tk.Entry(root, width=50, font=entry_font)
image_file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_image_file, bg=button_color, fg=button_fg_color, font=button_font).grid(row=0, column=2, padx=10, pady=10)

# Option selection for password or file
option = tk.StringVar(value="password")
tk.Radiobutton(root, text="Hide Password", variable=option, value="password", bg=bg_color, font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Radiobutton(root, text="Hide Text/PDF File", variable=option, value="file", bg=bg_color, font=label_font).grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Password entry
tk.Label(root, text="Enter Password:", bg=bg_color, font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky="e")
password_entry = tk.Entry(root, width=50, show='*', font=entry_font)
password_entry.grid(row=2, column=1, padx=10, pady=10)

# Text or PDF file selection
tk.Label(root, text="Select Text/PDF File:", bg=bg_color, font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky="e")
text_file_entry = tk.Entry(root, width=50, font=entry_font)
text_file_entry.grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_text_file, bg=button_color, fg=button_fg_color, font=button_font).grid(row=3, column=2, padx=10, pady=10)

# Output file name for steganography
tk.Label(root, text="Output Filename:", bg=bg_color, font=label_font).grid(row=4, column=0, padx=10, pady=10, sticky="e")
output_entry = tk.Entry(root, width=50, font=entry_font)
output_entry.grid(row=4, column=1, padx=10, pady=10)

# Perform steganography button
tk.Button(root, text="Perform Steganography", command=perform_steganography, bg=button_color, fg=button_fg_color, font=button_font).grid(row=5, column=0, columnspan=3, pady=20)

# Steganography image file selection for decoding
tk.Label(root, text="Select Steganography Image:", bg=bg_color, font=label_font).grid(row=6, column=0, padx=10, pady=10, sticky="e")
steg_image_file_entry = tk.Entry(root, width=50, font=entry_font)
steg_image_file_entry.grid(row=6, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_steg_image_file, bg=button_color, fg=button_fg_color, font=button_font).grid(row=6, column=2, padx=10, pady=10)

# Output file name for decoded text
tk.Label(root, text="Output Text Filename:", bg=bg_color, font=label_font).grid(row=7, column=0, padx=10, pady=10, sticky="e")
decode_output_entry = tk.Entry(root, width=50, font=entry_font)
decode_output_entry.grid(row=7, column=1, padx=10, pady=10)

# Decode steganography button
tk.Button(root, text="Decode Steganography", command=decode_steganography, bg=button_color, fg=button_fg_color, font=button_font).grid(row=8, column=0, columnspan=3, pady=20)

# Refresh/Reset button
tk.Button(root, text="Reset", command=refresh_fields, bg="red", fg=button_fg_color, font=button_font).grid(row=9, column=0, columnspan=3, pady=10)

root.mainloop()
