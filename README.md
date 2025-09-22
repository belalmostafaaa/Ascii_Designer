# ASCII Designer

A powerful terminal-based ASCII art generator for creating stunning, readable banners and logos for your CLI tools, scripts, and projects. Inspired by FIGlet, but enhanced with themes, colors, and multiple font styles.


## Features

- **5+ Unique Font Styles**: BigBlock, Slant, Script, Bubble, Gothic
- **9+ Attractive Themes**: Cyber, Retro, Minimal, Fantasy, Neon, Space, Gothic, Industrial, Banner
- **Size Options**: Small, Medium, Large for different visibility needs
- **ANSI Color Support**: Theme-specific colors for vibrant terminal output
- **File Export**: Save designs to text files for easy integration
- **Customizable**: Extensive command-line options for precise control

## Options	Usage
**--font**:	Choose the font for the ASCII design (e.g., slant, block, standard).
**--align**:	Set alignment of the output (left, center, right).
**--color**:	Apply color to the ASCII design (red, green, yellow, blue, magenta, cyan, white).
**--export**:	Export the ASCII design as reusable code (python, json, or raw).
**--theme**:	Pick a theme preset (combination of font + color).
**--embed-color**: If exporting, embed the ANSI color codes inside the exported content
**-h, --help**:	Show help message with all available options.

# Installation:

## Clone the repository
```
git clone https://github.com/belalmostafaaa/Ascii_Designer.git
```
```
cd ascii-designer
```
## Make executable (optional)
```
chmod +x ascii_designer.py
```
## Or install via pip (if packaged)
```
pip install ascii-designer
```

# Basic Usage:

## Simple usage with default settings
```
```
```
python3 ascii_designer.py "YourToolName"
```
```
```
## With custom theme and font
```
python3 ascii_designer.py "YourToolName" --font bigblock --theme banner --color
```
```
```
## Save to file
```
python3 ascii_designer.py "YourToolName" --output design --variations 2
```
