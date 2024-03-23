import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import os
import threading
from PIL import Image
import pillow_heif


class HEICToJPGConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG Converter")
        self.file_paths = []
        self.output_directory = ""
        self.setup_ui()

    def setup_ui(self):
        self.btn_select_files = tk.Button(
            self.root, text="Select HEIC Files", command=self.select_files
        )
        self.btn_select_files.pack(pady=5)

        self.btn_select_output = tk.Button(
            self.root,
            text="Select Output Directory",
            command=self.select_output_directory,
        )
        self.btn_select_output.pack(pady=5)

        self.quality_slider = tk.Scale(
            self.root,
            from_=1,
            to=100,
            orient="horizontal",
            label="Image Quality",
        )
        self.quality_slider.set(75)  # Valor inicial da qualidade
        self.quality_slider.pack()

        # Botão para limpar a seleção de arquivos
        self.btn_clear_files = tk.Button(
            self.root, text="Clear Selected Files", command=self.clear_files
        )
        self.btn_clear_files.pack(pady=5)

        self.txt_status = scrolledtext.ScrolledText(self.root, height=10)
        self.txt_status.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.btn_convert = tk.Button(
            self.root,
            text="Convert to JPG",
            command=self.start_conversion_thread,
            state="disabled",
        )
        self.btn_convert.pack(pady=5)

        # FRAME
        # Frame para a barra de progresso e o endereço de output
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        # Label para mostrar o endereço de output, também dentro do bottom_frame
        self.output_directory_label = tk.Label(
            self.bottom_frame, text="Output Directory: Not Selected", anchor="w"
        )
        self.output_directory_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Barra de progresso, agora dentro do bottom_frame
        self.progress_bar = ttk.Progressbar(
            self.bottom_frame, orient="horizontal", length=100, mode="determinate"
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=False, padx=5, pady=5)
        # FIM DO FRAME

    def select_files(self):
        self.file_paths = filedialog.askopenfilenames(
            title="Select HEIC Files",
            filetypes=[("HEIC files", "*.heic"), ("HEIF files", "*.heif")],
        )
        self.txt_status.insert(tk.END, f"Selected {len(self.file_paths)} files.\n")
        self.btn_convert["state"] = "normal" if self.output_directory else "disabled"

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory(title="Select Output Directory")
        if self.output_directory:
            self.output_directory_label.config(
                text=f"Output Directory: {self.output_directory}"
            )
            self.btn_convert["state"] = "normal" if self.file_paths else "disabled"

    def start_conversion_thread(self):
        threading.Thread(target=self.perform_conversion, daemon=True).start()

    def perform_conversion(self):
        self.progress_bar["maximum"] = len(self.file_paths)
        for index, file_path in enumerate(self.file_paths):
            self.convert_image(file_path, index + 1)
        self.reset_ui_after_conversion()

    def convert_image(self, file_path, index):
        jpg_path = os.path.join(
            self.output_directory,
            os.path.splitext(os.path.basename(file_path))[0] + ".jpg",
        )
        try:
            heif_file = pillow_heif.open_heif(file_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            image.save(jpg_path, format="JPEG", quality=self.quality_slider.get())
            self.update_ui(
                f"Converted: {os.path.basename(file_path)} -> {os.path.basename(jpg_path)}\n",
                index,
            )
        except Exception as e:
            self.update_ui(
                f"Error converting {os.path.basename(file_path)}: {e}\n", index
            )

    def update_ui(self, message, progress_value):
        self.txt_status.insert(tk.END, message)
        self.progress_bar["value"] = progress_value
        self.root.update_idletasks()

    def reset_ui_after_conversion(self):
        self.txt_status.insert(tk.END, "Conversion completed!\n")
        self.progress_bar["value"] = 0
        self.root.update_idletasks()

    def clear_files(self):
        self.file_paths = []
        self.txt_status.delete("1.0", tk.END)
        self.btn_convert["state"] = "disabled"
        self.txt_status.insert(tk.END, "Selected files cleared.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = HEICToJPGConverterApp(root)
    root.mainloop()
