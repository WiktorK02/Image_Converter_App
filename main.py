import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import customtkinter 

# To check extenxion
import imghdr

file_path = ''

def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.configure(text="File: " + file_path)

    else:
        file_label.configure(text="No file selected")

def generate_text():
    global file_path

    if not file_path:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No file selected")
        return

    try:
        # To check extenxion
        extension = imghdr.what(file_path)

        if extension == "png":
            # Load PNG image with alpha channel
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

            # Resize image to 128x64
            image = cv2.resize(image, (128, 64))

            # Get the alpha channel from the image
            alpha_channel = image[:, :, 3]

            # Convert alpha values to 0 or 1 (0 if transparency == 0, 1 if not)
            binary_alpha = np.where(alpha_channel == 0, 0, 1)

        elif extension == "jpeg":
            # Load JPEG image
            image = cv2.imread(file_path, cv2.IMREAD_COLOR)

            # Resize image to 128x64
            image = cv2.resize(image, (128, 64))

            # Convert RGB image to grayscale
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Compute threshold value to convert grayscale to binary
            _, threshold_value = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Convert grayscale image to binary alpha values
            binary_alpha = np.where(grayscale_image <= threshold_value, 0, 1)

        # Reshape the binary alpha values into 1D array
        binary_alpha = binary_alpha.ravel()

        # Split the binary alpha values into 8-byte arrays
        byte_arrays = np.packbits(binary_alpha)

        # Convert byte arrays to hexadecimal format
        hex_byte_arrays = ['0x' + format(byte, '02x') for byte in byte_arrays]

        # Convert hex byte arrays to C++ array format
        cpp_array = ', '.join(hex_byte_arrays)

        # Generate C++ array
        cpp_array = 'unsigned char my_array[] = {' + cpp_array + '};'
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, cpp_array)
    
    # In case of error or invalid extension 
    except:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Error generating text")

def copy_all():
    global file_path
    if not file_path:
        copied_all_label.configure(text="No text to copy")
        return

    root.clipboard_clear()
    root.clipboard_append(output_text.get(1.0, tk.END))
    copied_all_label.configure(text="Copied All")

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  

# Create customtkinter window
root = customtkinter.CTk() 
root.title("Image Converter v1.0")

# Set window size
root.geometry("400x450") # Set width and height as desired

# Label for "Open File" button
open_file_label =  customtkinter.CTkLabel(root, text="Select a file:")
open_file_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

# "Open File" button
open_file_button = customtkinter.CTkButton(root, text="Open File", command=open_file)
open_file_button.grid(row=0, column=1, pady=5, columnspan=1, sticky=tk.W)

# "Generate" button
generate_button = customtkinter.CTkButton(root, text="Generate", command=generate_text)
generate_button.grid(row=2, column=0, padx=10, pady=5, columnspan=1, sticky=tk.W)

# "Copy All" button
copy_all_button = customtkinter.CTkButton(root, text="Copy All", command=copy_all)
copy_all_button.grid(row=2, column=1, pady=5, columnspan=1, sticky=tk.W)  # Positioning the button on the right with fixed column value

# Label for displaying selected file path
file_label =  customtkinter.CTkLabel(root, text="No file selected")
file_label.grid(row=5, column=0, padx=10, pady=5, columnspan=3, sticky=tk.W)

# Output text form
output_text = tk.Text(root, height = 25, width = 72)
output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

# Label for displaying "Copied All" text
copied_all_label =  customtkinter.CTkLabel(root, text="")
copied_all_label.grid(row=4, column=0, padx=150, columnspan=3, sticky=tk.W)

root.mainloop()

