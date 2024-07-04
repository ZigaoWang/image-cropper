import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.root.geometry("800x600")

        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        self.load_button = tk.Button(self.frame, text="Load Image", command=self.open_image)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.crop_button = tk.Button(self.frame, text="Crop Image", command=self.crop_image, state=tk.DISABLED)
        self.crop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(root, cursor="cross", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.image = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.crop_coords = None
        self.displayed_image = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)
            self.crop_button.config(state=tk.NORMAL)

    def display_image(self, image):
        self.canvas.delete("all")
        max_width, max_height = self.root.winfo_width(), self.root.winfo_height() - 100  # Adjust for control panel height
        self.displayed_image = image.copy()
        self.displayed_image.thumbnail((max_width, max_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.displayed_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.crop_coords = self.canvas.coords(self.rect)

    def crop_image(self):
        if self.rect and self.crop_coords:
            x1, y1, x2, y2 = [int(coord) for coord in self.crop_coords]
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(self.displayed_image.width, x2)
            y2 = min(self.displayed_image.height, y2)
            if x1 < x2 and y1 < y2:
                self.cropped_image = self.image.crop((x1, y1, x2, y2))
                self.display_image(self.cropped_image)
                self.save_button.config(state=tk.NORMAL)
            else:
                messagebox.showerror("Error", "Invalid crop area. Please select a valid area within the image bounds.")

    def save_image(self):
        if hasattr(self, 'cropped_image'):
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"), ("BMP files", "*.bmp"), ("TIFF files", "*.tiff")])
            if save_path:
                self.cropped_image.save(save_path)
                messagebox.showinfo("Image Cropper", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropper(root)
    root.mainloop()
