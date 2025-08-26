#!/usr/bin/env python3
"""
PrintCut to SVG GUI Converter

Graphical user interface for converting Caldera/Summa Print and Cut Job Files to SVG format.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
from pathlib import Path

# Import the conversion function from the original module
from printcut_to_svg import convert_jobfile_to_svg


class PrintCutConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PrintCut/CUT to SVG Converter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Set the application icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # Default values
        self.input_file = ""
        self.output_file = ""
        self.scale_factor = tk.DoubleVar(value=25.4)
        self.path_color = tk.StringVar(value="black")
        self.rect_color = tk.StringVar(value="blue")
        self.trim_color = tk.StringVar(value="red")
        self.create_layers = tk.BooleanVar(value=True)

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Title label
        self.title_label = tk.Label(
            self.root,
            text="PrintCut/CUT to SVG Converter",
            font=("Arial", 16, "bold")
        )

        # Input file section
        self.input_frame = tk.LabelFrame(self.root, text="Input File", padx=10, pady=5)
        self.input_entry = tk.Entry(self.input_frame, width=50)
        self.input_browse_btn = tk.Button(
            self.input_frame,
            text="Browse...",
            command=self.browse_input_file
        )

        # Output file section
        self.output_frame = tk.LabelFrame(self.root, text="Output File", padx=10, pady=5)
        self.output_entry = tk.Entry(self.output_frame, width=50)
        self.output_browse_btn = tk.Button(
            self.output_frame,
            text="Browse...",
            command=self.browse_output_file
        )

        # Settings section
        self.settings_frame = tk.LabelFrame(self.root, text="Settings", padx=10, pady=5)

        # Scale factor
        self.scale_label = tk.Label(self.settings_frame, text="Scale Factor (inches to mm):")
        self.scale_entry = tk.Entry(self.settings_frame, textvariable=self.scale_factor, width=10)

        # Colors
        self.path_color_label = tk.Label(self.settings_frame, text="Path Color:")
        self.path_color_entry = tk.Entry(self.settings_frame, textvariable=self.path_color, width=15)

        self.rect_color_label = tk.Label(self.settings_frame, text="Rectangle Color:")
        self.rect_color_entry = tk.Entry(self.settings_frame, textvariable=self.rect_color, width=15)

        self.trim_color_label = tk.Label(self.settings_frame, text="Trim Box Color:")
        self.trim_color_entry = tk.Entry(self.settings_frame, textvariable=self.trim_color, width=15)

        # Layers checkbox
        self.layers_check = tk.Checkbutton(self.settings_frame, text="Create separate layers for different tools",
                                         variable=self.create_layers)

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.convert_btn = tk.Button(
            self.button_frame,
            text="Convert to SVG",
            command=self.convert_file,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2
        )
        self.exit_btn = tk.Button(
            self.button_frame,
            text="Exit",
            command=self.root.quit,
            bg="#f44336",
            fg="white",
            font=("Arial", 12),
            height=2
        )

        # Status/Progress section
        self.status_frame = tk.LabelFrame(self.root, text="Status", padx=10, pady=5)
        self.status_text = tk.Text(self.status_frame, height=8, width=60, state=tk.DISABLED)
        self.status_scrollbar = tk.Scrollbar(self.status_frame, command=self.status_text.yview)
        self.status_text.config(yscrollcommand=self.status_scrollbar.set)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100
        )

    def setup_layout(self):
        """Set up the layout of widgets"""
        # Title
        self.title_label.pack(pady=10)

        # Input file section
        self.input_frame.pack(fill=tk.X, padx=20, pady=5)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.input_browse_btn.pack(side=tk.RIGHT)

        # Output file section
        self.output_frame.pack(fill=tk.X, padx=20, pady=5)
        self.output_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.output_browse_btn.pack(side=tk.RIGHT)

        # Settings section
        self.settings_frame.pack(fill=tk.X, padx=20, pady=5)

        # Scale factor
        self.scale_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.scale_entry.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 20))

        # Colors
        self.path_color_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        self.path_color_entry.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 20))

        self.rect_color_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        self.rect_color_entry.grid(row=2, column=1, sticky=tk.W, pady=2, padx=(10, 20))

        self.trim_color_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        self.trim_color_entry.grid(row=3, column=1, sticky=tk.W, pady=2, padx=(10, 20))

        # Layers checkbox
        self.layers_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))

        # Buttons
        self.button_frame.pack(pady=10)
        self.convert_btn.pack(side=tk.LEFT, padx=(20, 10))
        self.exit_btn.pack(side=tk.LEFT, padx=(10, 20))

        # Progress bar
        self.progress_bar.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Status section
        self.status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def browse_input_file(self):
        """Open file dialog to select input file"""
        file_path = filedialog.askopenfilename(
            title="Select Print and Cut File (.cut) or Job File (.txt)",
            filetypes=[("CUT files", "*.cut"), ("Job files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

            # Auto-suggest output file
            if not self.output_file:
                input_path = Path(file_path)
                output_path = input_path.with_suffix('.svg')
                self.output_file = str(output_path)
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, str(output_path))

    def browse_output_file(self):
        """Open file dialog to select output file"""
        file_path = filedialog.asksaveasfilename(
            title="Save SVG File",
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
        )
        if file_path:
            self.output_file = file_path
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def update_status(self, message):
        """Update the status text area"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()

    def clear_status(self):
        """Clear the status text area"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)

    def convert_file(self):
        """Convert the input file to SVG"""
        # Get values from GUI
        self.input_file = self.input_entry.get().strip()
        self.output_file = self.output_entry.get().strip()

        # Validate inputs
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return

        if not self.output_file:
            messagebox.showerror("Error", "Please specify an output file.")
            return

        if not os.path.exists(self.input_file):
            messagebox.showerror("Error", f"Input file does not exist:\n{self.input_file}")
            return

        # Get settings
        try:
            scale = float(self.scale_factor.get())
            if scale <= 0:
                raise ValueError("Scale factor must be positive")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid scale factor: {e}")
            return

        path_color = self.path_color.get().strip()
        rect_color = self.rect_color.get().strip()
        trim_color = self.trim_color.get().strip()

        if not path_color or not rect_color or not trim_color:
            messagebox.showerror("Error", "Please specify all colors.")
            return

        # Clear previous status and start conversion
        self.clear_status()
        self.update_status("Starting conversion...")
        self.progress_var.set(10)

        try:
            # Perform conversion
            self.update_status(f"Converting: {self.input_file}")
            self.progress_var.set(50)

            # Get layers setting
            create_layers = self.create_layers.get()

            result = convert_jobfile_to_svg(
                input_file=self.input_file,
                output_file=self.output_file,
                scale=scale,
                path_color=path_color,
                rect_color=rect_color,
                trim_color=trim_color,
                create_layers=create_layers
            )

            self.progress_var.set(100)
            self.update_status("Conversion completed successfully!")
            self.update_status(result)

            # Show success message
            messagebox.showinfo("Success", f"SVG file created successfully!\n\n{result}")

        except Exception as e:
            self.progress_var.set(0)
            error_msg = f"Error during conversion: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Conversion Error", error_msg)


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = PrintCutConverterGUI(root)

    # Set a nice theme if available
    try:
        style = ttk.Style()
        style.theme_use('vista')
    except:
        pass

    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()