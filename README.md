# HEIC to JPG Converter

This application is a graphical tool developed in Python that allows users to easily convert images from HEIC format to JPG. It leverages the `pillow_heif` library to read HEIC files and the PIL (Pillow) library to convert and save the images in JPG format.

## Project Structure

The project is organized as follows:

- `convert_heic_to_jpg.py`: The main application file containing the graphical interface logic and the image conversion functionality.
- `requirements.txt`: A list of dependencies needed to run the application.

## Building the Application

To build an executable for the application, follow these steps:

### Setting Up the Environment

It's recommended to use a virtual environment to install dependencies and run the application. To create and activate a virtual environment, run:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
pip install -r requirements.txt
```

#### Installing Dependencies

```bash
pip install -r requirements.txt
```

#### Generating the Executable

```bash
pyinstaller --onefile --windowed convert_heic_to_jpg.py
```

#### Usage

```bash
python convert_heic_to_jpg.py
```
