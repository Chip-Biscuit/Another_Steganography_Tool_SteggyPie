import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# LSB Steganography tool to hide or retrieve messages in png's using least significant bit steganography in specific
# color channels. By Chip.

# --- LSB Steganography Functions ---

def encode_message(image_path, message, color_channel, output_path):
    image = Image.open(image_path)
    image = image.convert("RGB")  # Ensure it's in RGB format
    pixels = image.load()

    # Convert message to binary and add a stop sequence
    binary_message = ''.join([format(ord(char), '08b') for char in message])
    binary_message += '00000000'  # Stop sequence

    width, height = image.size
    index = 0  # To track position in the binary message

    # Map color channel to RGB index
    channel_map = {'red': 0, 'green': 1, 'blue': 2}
    channel_index = channel_map[color_channel]

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            if index < len(binary_message):
                # Modify the least significant bit of the selected channel
                pixel[channel_index] = (pixel[channel_index] & ~1) | int(binary_message[index])
                index += 1
            pixels[x, y] = tuple(pixel)

    # Save the modified image as PNG to preserve data
    image.save(output_path, format="PNG")  # Save as PNG to avoid compression artifacts
    return output_path


def decode_message(image_path, color_channel):
    image = Image.open(image_path)
    image = image.convert("RGB")  # Ensure it's in RGB format
    pixels = image.load()
    binary_message = ''

    width, height = image.size

    # Map color channel to RGB index
    channel_map = {'red': 0, 'green': 1, 'blue': 2}
    channel_index = channel_map[color_channel]

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            # Extract the least significant bit of the selected channel
            binary_message += str(pixel[channel_index] & 1)

    # Convert binary message to text until the stop sequence
    message = ''
    try:
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            if byte == '00000000':  # Stop sequence (end of message)
                break
            # Convert the byte to a character
            message += chr(int(byte, 2))
    except ValueError as e:
        # Error handling if binary data cannot be converted
        messagebox.showerror("Decoding Error", f"Error decoding the message: {e}")
        return "Decoding error occurred."

    return message if message else "No message found or decoding error."


# --- Tkinter GUI Functions ---

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if file_path:
        input_file_path.set(file_path)


def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        output_file_path.set(file_path)


def browse_decode_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if file_path:
        decode_file_path.set(file_path)


def encode_message_gui():
    file_path = input_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "No base image selected!")
        return

    output_path = output_file_path.get()
    if not output_path:
        messagebox.showerror("Error", "No output file location specified!")
        return

    message = message_entry.get()
    if not message:
        messagebox.showerror("Error", "No message entered!")
        return

    color_channel = encode_color_var.get()
    encode_message(file_path, message, color_channel, output_path)
    messagebox.showinfo("Success", f"Message encoded and saved to {output_path}")


def decode_message_gui():
    file_path = decode_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "No encoded image selected for decoding!")
        return

    color_channel = decode_color_var.get()  # Get the selected decode color channel
    decoded_message = decode_message(file_path, color_channel)
    messagebox.showinfo("Decoded Message", f"Message: {decoded_message}")


# --- Tkinter GUI Setup ---

root = tk.Tk()
root.title("Steggypie (PNG)")

# File selection for encoding
input_file_path = tk.StringVar()
output_file_path = tk.StringVar()
decode_file_path = tk.StringVar()

tk.Label(root, text="Select Base Image for Encoding:").pack(pady = (20,0))
tk.Entry(root, textvariable=input_file_path, width=50).pack()
tk.Button(root, text="Browse", command=browse_input_file).pack(pady=(0,20))

tk.Label(root, text="Select Output Location for Encoded Image:").pack()
tk.Entry(root, textvariable=output_file_path, width=50).pack()
tk.Button(root, text="Browse", command=browse_output_file).pack()

# Color channel selection for encoding
tk.Label(root, text="Select Color Channel for Encoding:").pack()
encode_color_var = tk.StringVar(value="red")
tk.Radiobutton(root, text="Red", variable=encode_color_var, value="red", fg = "red").pack()
tk.Radiobutton(root, text="Green", variable=encode_color_var, value="green", fg = "green").pack()
tk.Radiobutton(root, text="Blue", variable=encode_color_var, value="blue", fg = "blue").pack()

# Message input for encoding
tk.Label(root, text="Enter Message to Encode:").pack(pady=(50,0))
message_entry = tk.Entry(root, width=50)
message_entry.pack()

# encode button
tk.Button(root, text="Encode Message", font = ( 0, 11, "bold"), command=encode_message_gui).pack(pady = (30,50))

# File selection for decoding
tk.Label(root, text="Select Encoded Image for Decoding:").pack()
tk.Entry(root, textvariable=decode_file_path, width=50).pack()
tk.Button(root, text="Browse", command=browse_decode_file).pack()

# Color channel selection for decoding
tk.Label(root, text="Select Color Channel for Decoding:").pack()
decode_color_var = tk.StringVar(value="red")
tk.Radiobutton(root, text="Red", variable=decode_color_var, value="red", fg = "red").pack()
tk.Radiobutton(root, text="Green", variable=decode_color_var, value="green", fg = "green").pack()
tk.Radiobutton(root, text="Blue", variable=decode_color_var, value="blue", fg = "blue").pack()

#Decode button
tk.Button(root, text="Decode Message", font = ( 0, 11, "bold"), command=decode_message_gui).pack(pady=(30,50))

root.mainloop()
