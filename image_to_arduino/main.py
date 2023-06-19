#!/usr/bin/env python3
import tkinter as tk
import customtkinter 
from tkinter            import filedialog
import cv2
import numpy            as np
from PIL                import Image, ImageTk, ImageOps
import os
import imghdr
import traceback


file_path = ''
image_tk = ''
left_switch_state = False
right_switch_state = False
png_switch_state = False

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
        if not png_switch_state:
            img = Image.open(file_path).convert("RGBA")
            img = img.resize((128, 64))
            img = ImageOps.grayscale(img)
            if left_switch_state:
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
        else:
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            image = cv2.resize(image, (128, 64))
            
            # Split the image into channels
            b, g, r, a = cv2.split(image)
        
            
            # Convert the thresholded image to a binary array (0s and 1s)
            binary_array = np.where(a > 0, 1, 0)
            
            # Convert the binary array to a 1D array
            one_d_array = binary_array.flatten()
            
            if left_switch_state:
                one_d_array = 1 - one_d_array
            
            # Split the binary alpha values into 8-bit arrays
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
        if not png_switch_state:
            img = Image.open(file_path).convert("RGBA")
            
            img = img.resize((128, 64))
            img = ImageOps.grayscale(img)
            
            if left_switch_state:
                # Reverse the colors of the image
                img = ImageOps.invert(img)
            
            # Convert the PIL Image to a NumPy array and apply thresholding
            img_arr = np.array(img)
            _, thresholded_image = cv2.threshold(img_arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            image_preview_label.config(image="")
            bw_img = Image.fromarray(thresholded_image)
            
            # Update image preview
            image_pre = ImageTk.PhotoImage(bw_img)
            image_preview_label.config(image=image_pre)
            image_preview_label.image = image_pre
        else:    
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            # Split the image into channels
            b, g, r, a = cv2.split(image)
            # Check if the image has an alpha channel
            if image.shape[2] == 4 and left_switch_state:
                
                # Set transparent pixels to white
                white_mask = (a == 0)
                b[white_mask] = 255
                g[white_mask] = 255
                r[white_mask] = 255
                
                # Set non-transparent pixels to black
                non_transparent_mask = (a > 0)
                b[non_transparent_mask] = 0
                g[non_transparent_mask] = 0
                r[non_transparent_mask] = 0
                # Set white pixels to non-transparent (alpha to 255)
                white_pixels = (b == 255) & (g == 255) & (r == 255)
                a[white_pixels] = 255
                
            elif not left_switch_state:
                # Set transparent pixels to white
                white_mask = (a == 0)
                b[white_mask] = 0
                g[white_mask] = 0
                r[white_mask] = 0
                
                # Set non-transparent pixels to black
                non_transparent_mask = (a > 0)
                b[non_transparent_mask] = 255
                g[non_transparent_mask] = 255
                r[non_transparent_mask] = 255
                white_pixels = (b == 0) & (g == 0) & (r == 0)
                a[white_pixels] = 255
                
            # Merge the channels back into a single image
            image = cv2.merge((b, g, r, a))
            # Convert the image to a NumPy array
            img_arr = np.array(image)

            image_preview_label.config(image="")
            resized_image = cv2.resize(img_arr, (128, 64))
            bw_img = Image.fromarray(resized_image)
            
            # Update image preview
            image_pre = ImageTk.PhotoImage(bw_img)
            image_preview_label.config(image=image_pre)
            image_preview_label.image = image_pre
   
    def update_gif():
        global image_previews
        frames_list = []
        image_previews = []
        # open the GIF file
        gif_file = Image.open(file_path)

        # loop through each frame of the GIF
        for frame in range(0, gif_file.n_frames):
            gif_file.seek(frame)

            # extract the transparency mask if it exists
            transparency_mask = gif_file.convert("RGBA").split()[-1] if gif_file.info.get("transparency") else None

            # create a new RGBA image with the same size as the original
            new_image = Image.new("RGBA", gif_file.size)

            # paste the current frame onto the new image, preserving transparency
            new_image.paste(gif_file, (0, 0), transparency_mask)

                # Replace transparent pixels with white
            new_image = Image.alpha_composite(Image.new("RGBA", new_image.size, (255, 255, 255, 255)), new_image)

            new_image = new_image.resize((128, 64))

            new_image = ImageOps.grayscale(new_image)
            if left_switch_state == True:
                # Reverse the colors of the image
                new_image= ImageOps.invert(new_image)
            # Convert the PIL Image to a NumPy array and apply thresholding
            img_arr = np.array(new_image)
            _, thresholded_image = cv2.threshold(img_arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            image_preview_label.config(image="")
            bw_img = Image.fromarray(thresholded_image).convert('L')
            photo = ImageTk.PhotoImage(bw_img)
            image_previews.append(photo)

        # Display the first frame preview
        current_frame = 0


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
            try:
                # To check extenxion
                extension = imghdr.what(file_path)
                if  extension == "jpeg" or extension == "png":
                    update_img_pre()
                    if right_switch_state == False:
                        # Generate C++ array
                        cpp_array = 'const unsigned char PROGMEM ' + os.path.splitext(os.path.basename(file_path))[0] + ' [] = {\n' + image_conv() + '\n};' 
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
            except:
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, "Error generating text")
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
    
    def toggle_png_switch():
        global png_switch_state
        png_switch_state = not png_switch_state

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
    root.geometry("340x600") # Set width and height as desired

    # Label for displaying selected file path
    file_label =  customtkinter.CTkLabel(root, text="No file selected")
    file_label.grid(row=0, column=0, padx=10, columnspan=1, sticky="nsew", pady=5)

    # "Open File" button
    open_file_button = customtkinter.CTkButton(root, text="Open File", command=open_file)
    open_file_button.grid(row=0, column=1, padx=10, pady=5, columnspan=1, sticky="nsew")

    # "Generate" button
    generate_button = customtkinter.CTkButton(root, text="Generate Code", command=generate_text)
    generate_button.grid(row=3, column=0, padx=10, pady=5, columnspan=1, sticky="nsew")

    # "Copy All" button
    copy_all_button = customtkinter.CTkButton(root, text="Copy All", command=copy_all)
    copy_all_button.grid(row=3, column=1, padx=10, pady=5, columnspan=1, sticky="nsew")  

    # Output text 
    output_text = customtkinter.CTkTextbox(root, height = 280, width = 300 )   # 25 50
    output_text.grid(row=4, column=0, padx=10, pady=5, columnspan=3, sticky="nsew")

    # Label for displaying "Copied All" text
    copied_all_label =  customtkinter.CTkLabel(root, text="")
    copied_all_label.grid(row=5, column=1, pady=5,columnspan=3, sticky="nsew")

    # Preview text lael
    preview_text_label = customtkinter.CTkLabel(root, text="Preview")
    preview_text_label.grid(row=6, column=0, pady=5, padx=10)

    # Label to display the image
    image_preview_label = tk.Label(root, bg="#1b1a1b")
    image_preview_label.grid(row=7, column=0, columnspan=1, padx=10)

    # Switch label left
    switch = customtkinter.CTkSwitch(root, text="Reverse colors", command=toggle_left_switch)
    switch.grid(row=1, column=0, padx=10, sticky="nsew")

    # Switch label png
    switch = customtkinter.CTkSwitch(root, text="Remove background", command=toggle_png_switch)
    switch.grid(row=2, column=0, padx=10, sticky="nsew")

    # Switch label right 
    switch_right = customtkinter.CTkSwitch(root, text="Full arduino code", command=toggle_right_switch)
    switch_right.grid(row=1, column=1, padx=10, sticky="nsew")

    # "Clear all" button 
    clear_all_button = customtkinter.CTkButton(root, text="Clear All", command=clear_all)
    clear_all_button.grid(row=5, column=0, pady=5, padx=10, columnspan=1, sticky="nsew")  

    # Configure the window to not be resizable
    root.resizable(False, False)

    root.mainloop()
