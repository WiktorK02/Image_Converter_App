import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import customtkinter 
from PIL import Image, ImageTk

# To check extenxion
import imghdr

file_path = ''
image_tk = ''

def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.configure(text="File: " + file_path)
    else:
        file_label.configure(text="No file selected")

def generate_text():
    global image_tk

    try:
        # To check extenxion
        extension = imghdr.what(file_path)

        if extension == "png":
            # Load PNG image with alpha channel
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            # Resize the image to 128x64
            image = cv2.resize(image, (128, 64))

            # Get the alpha channel from the image
            alpha_channel = image[:, :, 3]

            # Convert alpha values to 0 or 1 (0 if transparency == 0, 1 if not)
            binary_alpha = np.where(alpha_channel == 0, 0, 1)

            # Convert the image to a PIL Image object and apply binary thresholding
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            image = Image.fromarray(image)

            # Convert the PIL Image to a PhotoImage object
            image_pre = ImageTk.PhotoImage(image)
            
            # Update the label's image
            image_preview_label.config(image=image_pre)
            image_preview_label.image = image_pre

        elif extension == "jpeg":
            # Load image
            image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            
            # Resize the image to 128x64
            image = cv2.resize(image, (128, 64))
            
            # Convert RGB image to grayscale
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Compute threshold value to convert grayscale to binary
            _, threshold_value = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Convert the image to a PIL Image object
            image_pre = Image.fromarray(cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])
            
            # Convert the PIL Image to a PhotoImage object
            image_pre = ImageTk.PhotoImage(image_pre)
            
            # Update the label's image
            image_preview_label.config(image=image_pre)
            image_preview_label.image = image_pre
                      
            # Convert grayscale image to binary alpha values
            binary_alpha = np.where(grayscale_image <= threshold_value, 1, 0)

        # Reshape the binary alpha values into 1D array
        binary_alpha = binary_alpha.ravel()

        # Split the binary alpha values into 8-byte arrays
        byte_arrays = np.packbits(binary_alpha)

        # Convert byte arrays to hexadecimal format
        hex_byte_arrays = ['0x' + format(byte, '02x') for byte in byte_arrays]

        cpp_array = ', '.join(hex_byte_arrays)
        # Insert newline after every 10 hexadecimal numbers
        cpp_array = [cpp_array[i:i+2] for i in range(0, len(cpp_array), 2)]  # Split into pairs of hexadecimal numbers
        cpp_array = [''.join(cpp_array[i:i+30]) for i in range(0, len(cpp_array), 30)]  # Join pairs with space, and group every 10 pairs
        cpp_array = '\n'.join(cpp_array)  # Join groups with newline character

        # Generate C++ array
        cpp_array = 'unsigned char my_array[] = {\n' + cpp_array + '\n};'

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
    copied_all_label.configure(text="✓ Copied All")

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  

# Create customtkinter window
root = customtkinter.CTk() 
root.title("Image Converter v1.0")

# Set window size
root.geometry("320x550") # Set width and height as desired

# Label for "Open File" button
open_file_label =  customtkinter.CTkLabel(root, text="Select a file:")
open_file_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

# "Open File" button
open_file_button = customtkinter.CTkButton(root, text="Open Image File", command=open_file)
open_file_button.grid(row=0, column=1, padx=10, pady=5, columnspan=1, sticky="nsew")

# "Generate" button
generate_button = customtkinter.CTkButton(root, text="Generate Code", command=generate_text)
generate_button.grid(row=2, column=0, padx=10, pady=5, columnspan=1, sticky="nsew")

# "Copy All" button
copy_all_button = customtkinter.CTkButton(root, text="Copy All", command=copy_all)
copy_all_button.grid(row=2, column=1, pady=5, padx=10, columnspan=1, sticky="nsew")  # Positioning the button on the right with fixed column value

# Output text for
output_text = customtkinter.CTkTextbox(root, height = 280, width = 300 )   # 25 50
output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Label for displaying "Copied All" text
copied_all_label =  customtkinter.CTkLabel(root, text="")
copied_all_label.grid(row=4, column=0, padx=120, columnspan=3, sticky="nsew")

# Label for displaying selected file path
file_label =  customtkinter.CTkLabel(root, text="No file selected")
file_label.grid(row=5, column=0, padx=10, pady=5, columnspan=3, sticky="nsew")

# Label for "Open File" button
preview_text_label =  customtkinter.CTkLabel(root, text="Preview:")
preview_text_label.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")

# Create a label to display the image
image_preview_label = tk.Label(root, bg='#242424')
image_preview_label.grid(row=7, column=0, padx=10, pady=5, sticky="nsew")
root.mainloop()
