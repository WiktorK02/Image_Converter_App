#!/usr/bin/env python3
import tkinter as tk
import customtkinter 
from tkinter            import filedialog
import cv2
import numpy            as np
from PIL                import Image, ImageTk, ImageOps
import os
import imghdr
import time

file_path = ''
image_tk = ''
left_switch_state = False
right_switch_state = False

def main():


    def open_file():
        global file_path
        file_path = filedialog.askopenfilename()
        if file_path:
            # If file name len is greater than 15: return ... + extension
            file_label.configure(
                text="File: "
                + (
                    os.path.basename(file_path)
                    if len(os.path.basename(file_path)) < 15
                    else "..." + imghdr.what(file_path)
                )
            )
        else:
            file_label.configure(text="No file selected")
    def image_conv():

        img = Image.open(file_path).convert("RGBA")
            # Replace transparent pixels with white
        img = Image.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, 255)), img)

        img = img.resize((128, 64))

        img = ImageOps.grayscale(img)
        if left_switch_state == True:
            # Reverse the colors of the image
            img= ImageOps.invert(img)
        # Convert the PIL Image to a NumPy array and apply thresholding
        img_arr = np.array(img)
        _, thresholded_image = cv2.threshold(img_arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Convert the thresholded image to a binary array (0s and 1s)
        binary_array = np.where(thresholded_image > 0, 1, 0)
        
        # Convert the binary array to a 1D array
        one_d_array = binary_array.flatten()

        # Split the binary alpha values into 8-byte arrays
        byte_arrays = np.packbits(one_d_array)

        # Convert byte arrays to hexadecimal format
        hex_byte_arrays = ['0x' + format(byte, '02x') for byte in byte_arrays]

        cpp_array = ', '.join(hex_byte_arrays)
        # Insert newline after every 10 hexadecimal numbers
        cpp_array = [cpp_array[i:i+2] for i in range(0, len(cpp_array), 2)]  # Split into pairs of hexadecimal numbers
        cpp_array = [''.join(cpp_array[i:i+30]) for i in range(0, len(cpp_array), 30)]  # Join pairs with space, and group every 10 pairs
        cpp_array = '\n'.join(cpp_array)  # Join groups with newline character
        
        return cpp_array
    def update_img_pre():
        img = Image.open(file_path).convert("RGBA")
            # Replace transparent pixels with white
        img = Image.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, 255)), img)

        img = img.resize((128, 64))

        img = ImageOps.grayscale(img)
        if left_switch_state == True:
            # Reverse the colors of the image
            img= ImageOps.invert(img)
        # Convert the PIL Image to a NumPy array and apply thresholding
        img_arr = np.array(img)
        _, thresholded_image = cv2.threshold(img_arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        image_preview_label.config(image="")
        bw_img = Image.fromarray(thresholded_image).convert('L')
         # Update image preview
        image_pre = ImageTk.PhotoImage(bw_img)
        image_preview_label.config(image=image_pre)
        image_preview_label.image = image_pre
    def update_gif():
        global image_previews
        frames_list = []
        image_previews = []
        with Image.open(file_path) as im:
            for frame in range(im.n_frames):
                # Select the current frame
                im.seek(frame)
                # Create a new image object from the current frame
                frame_image = im.copy()

                # Resize the image
                frame_image = frame_image.resize((128, 64))
                
                # Convert the image to grayscale
                frame_image = ImageOps.grayscale(frame_image)
                # Set all transparent pixels to white
                photo = ImageTk.PhotoImage(frame_image)
                image_previews.append(photo)
                # Calculate the brightness of each pixel
                brightness = np.array(frame_image)
                # Apply thresholding based on brightness
                thresholded_image = np.where(brightness >= 128, 255, 0).astype('uint8')

                # Invert the image if left switch is on
                if left_switch_state:
                    thresholded_image = cv2.bitwise_not(thresholded_image)

                # Convert the NumPy array to a PIL Image
                bw_img = Image.fromarray(thresholded_image).convert('L')

                # Create a PhotoImage from the PIL Image and add it to the list of image previews
                
                

        # Display the first frame preview
        current_frame = 0
        
        # Function to update the preview with the next frame
        def update_preview():
            nonlocal current_frame
            current_frame = (current_frame+1) % len(image_previews)
            image_preview_label.config(image=image_previews[current_frame])
            image_preview_label.after(100, update_preview)  # Update every 100 ms
        
        # Start updating the preview
        image_preview_label.after(100, update_preview)

    def generate_text():
        global image_tk, switch_var
        if not file_path == '':    
            #try:
                # To check extenxion
                extension = imghdr.what(file_path)
                if  extension == "jpeg" or extension == "png":
                    update_img_pre()
                    if right_switch_state == False:
                        # Generate C++ array
                        cpp_array = 'const unsigned char PROGMEM ' + os.path.splitext(os.path.basename(file_path))[0] + ' [] = {\n' + image_conv()+ '\n};' 
                    elif right_switch_state == True:
                        # Generate full code ready to use 
                        cpp_array = '''#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);
const unsigned char PROGMEM ''' + os.path.splitext(os.path.basename(file_path))[0] + '''[] = {\n''' +  image_conv() + ''' };
void setup() 
{
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    display.display();
    delay(2000);
    display.clearDisplay();}
void loop() 
{
    display.drawBitmap(0, 0, ''' + os.path.splitext(os.path.basename(file_path))[0] + ''', 128, 64, 1); 
    display.display();
    delay(5000);
    display.clearDisplay();
    delay(5000);}'''        

                    output_text.delete(1.0, tk.END)
                    output_text.insert(tk.END, cpp_array)
                elif extension == "gif":
                    update_gif()
            # In case of error or invalid extension         
            #except:
               # output_text.delete(1.0, tk.END)
                #output_text.insert(tk.END, "Error generating text")
        else: 
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Select any file")
    def copy_all():
        if not file_path:
            copied_all_label.configure(text="No text to copy")
            return

        root.clipboard_clear()
        root.clipboard_append(output_text.get(1.0, tk.END))
        copied_all_label.configure(text="✓ Copied")

    def toggle_left_switch():
        global left_switch_state
        left_switch_state = not left_switch_state

    def toggle_right_switch():
        global right_switch_state
        right_switch_state = not right_switch_state

    def clear_all():
        global image_previews
        # Clear output text and image preview
        output_text.delete(1.0, tk.END)
        image_preview_label.config(image="")
        image_previews = []

    customtkinter.set_appearance_mode("dark")  
    customtkinter.set_default_color_theme("dark-blue")  

    # Create customtkinter window
    root = customtkinter.CTk() 
    root.title("Image to arduino")

    # Set window size
    root.geometry("320x550") # Set width and height as desired

    # Label for displaying selected file path
    file_label =  customtkinter.CTkLabel(root, text="No file selected")
    file_label.grid(row=0, column=0, padx=10, columnspan=1, sticky="nsew", pady=5)

    # "Open File" button
    open_file_button = customtkinter.CTkButton(root, text="Open File", command=open_file)
    open_file_button.grid(row=0, column=1, padx=10, pady=5, columnspan=1, sticky="nsew")

    # "Generate" button
    generate_button = customtkinter.CTkButton(root, text="Generate Code", command=generate_text)
    generate_button.grid(row=2, column=0, padx=10, pady=5, columnspan=1, sticky="nsew")

    # "Copy All" button
    copy_all_button = customtkinter.CTkButton(root, text="Copy All", command=copy_all)
    copy_all_button.grid(row=2, column=1, padx=10, pady=5, columnspan=1, sticky="nsew")  

    # Output text 
    output_text = customtkinter.CTkTextbox(root, height = 280, width = 300 )   # 25 50
    output_text.grid(row=3, column=0, padx=10, pady=5, columnspan=3, sticky="nsew")

    # Label for displaying "Copied All" text
    copied_all_label =  customtkinter.CTkLabel(root, text="")
    copied_all_label.grid(row=4, column=1, pady=5,columnspan=3, sticky="nsew")

    # Preview text lael
    preview_text_label = customtkinter.CTkLabel(root, text="Preview")
    preview_text_label.grid(row=5, column=0, pady=5, padx=10)

    # Label to display the image
    image_preview_label = tk.Label(root, bg="#1b1a1b")
    image_preview_label.grid(row=6, column=0, columnspan=1, padx=10)

    # Switch label left
    switch = customtkinter.CTkSwitch(root, text="Reverse colors", command=toggle_left_switch)
    switch.grid(row=1, column=0, padx=10, sticky="nsew")

    # Switch label right 
    switch_right = customtkinter.CTkSwitch(root, text="Full arduino code", command=toggle_right_switch)
    switch_right.grid(row=1, column=1, padx=10, sticky="nsew")

    # "Clear all" button 
    clear_all_button = customtkinter.CTkButton(root, text="Clear All", command=clear_all)
    clear_all_button.grid(row=4, column=0, pady=5, padx=10, columnspan=1, sticky="nsew")  

    # Configure the window to not be resizable
    root.resizable(False, False)

    root.mainloop()
main()