# ASCII Designer

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/badge/downloads-100%2B-green)](https://github.com/username/ascii-designer/releases)

A powerful terminal-based ASCII art generator for creating stunning, readable banners and logos for your CLI tools, scripts, and projects. Inspired by FIGlet, but enhanced with themes, colors, and multiple font styles.

<div align="center">
  <img src="https://via.placeholder.com/800x200/0066cc/ffffff?text=ASCII+Designer" alt="ASCII Designer Banner">
</div>

## Features

- **5+ Unique Font Styles**: BigBlock, Slant, Script, Bubble, Gothic
- **9+ Attractive Themes**: Cyber, Retro, Minimal, Fantasy, Neon, Space, Gothic, Industrial, Banner
- **Size Options**: Small, Medium, Large for different visibility needs
- **ANSI Color Support**: Theme-specific colors for vibrant terminal output
- **Random Variations**: Generate multiple design options automatically
- **File Export**: Save designs to text files for easy integration
- **Customizable**: Extensive command-line options for precise control

## Options


**--theme**: Choosing the theme of designing
--size TEXT,Design size,--size large
**--font**: Selecting the font style - Choose ASCII character design
**--variations**: Number of design variations to generate
**--color**: Enable ANSI color output - Add theme-specific colors
**--output**: Save designs to files - Export to text files
**--random**: Add random decorative elements
**-h**: Display help information

## Demo

   ______      __              ____                      
  / ____/_  __/ /_  ___  _____/ __ \___  _________  ____ 
 / /   / / / / __ \/ _ \/ ___/ /_/ / _ \/ ___/ __ \/ __ \
/ /___/ /_/ / /_/ /  __/ /  / _, _/  __/ /__/ /_/ / / / /
\____/\__, /_.___/\___/_/  /_/ |_|\___/\___/\____/_/ /_/ 
     /____/                                              


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
python3 ascii_designer.py "YourToolName"
```
## With custom theme and font
```
python3 ascii_designer.py "YourToolName" --font bigblock --theme banner --color
```
## Multiple variations
```
python3 ascii_designer.py "YourToolName" --variations 3 --random
```
## Save to file
```
python3 ascii_designer.py "YourToolName" --output design --variations 2
```
