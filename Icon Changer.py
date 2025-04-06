import cv2
import numpy as np
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys

# Get the correct icon path
if getattr(sys, 'frozen', False):  # If running as an EXE
    ICON_PATH = os.path.join(sys._MEIPASS, "app_icon.ico")  # Use lowercase & avoid spaces
else:
    ICON_PATH = "app_icon.ico"

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
POPPINS_REGULAR = ("Poppins", 12)

def hex_to_bgr(hex_color):
    """Convert HEX to BGR format."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return (255, 255, 255)  # Default to white if invalid
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb[::-1]  # Convert RGB to BGR

def change_all_colors(image_path, output_path, new_color):
    """Replace all non-transparent pixels with a new color."""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Error: Could not load image {image_path}.")
        return
    
    if image.shape[2] == 4:  # Check if image has an alpha channel
        alpha_channel = image[:, :, 3]  # Extract alpha channel
        mask = alpha_channel > 0  # Detect non-transparent pixels
    else:
        mask = np.ones(image.shape[:2], dtype=np.uint8)  # Assume no transparency
    
    result = image.copy()
    result[mask > 0, :3] = new_color  # Replace color where pixels are non-transparent
    
    # Save output image
    cv2.imwrite(output_path, result)
    print(f"Image saved: {output_path}")

def select_images():
    return filedialog.askopenfilenames(filetypes=[("PNG Images", "*.png")])

def select_output_folder():
    return filedialog.askdirectory()

def browse_images():
    files = select_images()
    if files:
        image_entry.delete(0, "end")
        image_entry.insert(0, ", ".join(files))

def browse_output_folder():
    folder = select_output_folder()
    if folder:
        output_entry.delete(0, "end")
        output_entry.insert(0, folder)

def process_images():
    image_paths = image_entry.get().split(", ")
    output_folder = output_entry.get()
    
    # Get new color from user
    new_hex = new_color_entry.get().strip()
    new_color = hex_to_bgr(new_hex)

    if image_paths and output_folder:
        for image_path in image_paths:
            file_name = os.path.basename(image_path)
            output_path = os.path.join(output_folder, file_name)
            change_all_colors(image_path, output_path, new_color)
        
        # Show success message
        messagebox.showinfo("Process Completed", "All images have been successfully processed!")

def clear_fields():
    image_entry.delete(0, "end")
    output_entry.delete(0, "end")
    new_color_entry.delete(0, "end")

def exit_app():
    root.quit()

def validate_hex_input(value):
    return len(value) <= 6 and all(c in "0123456789ABCDEFabcdef" for c in value)

def on_new_color_change(event):
    text = new_color_entry.get().upper()
    if not validate_hex_input(text):
        new_color_entry.delete(0, "end")
        new_color_entry.insert(0, text[:6])

# GUI Setup
root = ctk.CTk()
root.title("Bulk Icon Color Changer")

# Set app icon
if os.path.exists(ICON_PATH):
    root.iconbitmap(ICON_PATH)

frame = ctk.CTkFrame(root, corner_radius=10)
frame.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Select Images:", font=POPPINS_REGULAR).pack(pady=10)
image_entry = ctk.CTkEntry(frame, width=400, font=POPPINS_REGULAR)
image_entry.pack()
ctk.CTkButton(frame, text="Browse", command=browse_images, font=POPPINS_REGULAR).pack(pady=10)

ctk.CTkLabel(frame, text="Select Output Folder:", font=POPPINS_REGULAR).pack(pady=10)
output_entry = ctk.CTkEntry(frame, width=400, font=POPPINS_REGULAR)
output_entry.pack()
ctk.CTkButton(frame, text="Browse", command=browse_output_folder, font=POPPINS_REGULAR).pack(pady=10)

# Color Selection with Validation
ctk.CTkLabel(frame, text="Enter New Color (Hex, 6-digits only):", font=POPPINS_REGULAR).pack(pady=5)
new_color_entry = ctk.CTkEntry(frame, width=100, font=POPPINS_REGULAR)
new_color_entry.pack()

# Bind input validation
new_color_entry.bind("<KeyRelease>", on_new_color_change)

# Buttons
ctk.CTkButton(frame, text="Process Images", command=process_images, font=POPPINS_REGULAR).pack(pady=8)
ctk.CTkButton(frame, text="Clear", command=clear_fields, font=POPPINS_REGULAR).pack(pady=8)
ctk.CTkButton(frame, text="Exit", command=exit_app, font=POPPINS_REGULAR).pack(pady=8)

# Copyright label at the bottom
copyright_label = ctk.CTkLabel(
    frame, 
    text="© 2025 Tghanafiazmi", 
    font=POPPINS_REGULAR
)
copyright_label.pack(pady=(5, 0))

# Automatically resize window to fit content
root.update_idletasks()  # Update layout
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")  # Fit to content

root.mainloop()
