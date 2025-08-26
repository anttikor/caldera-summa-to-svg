# PrintCut to SVG Converter

A graphical user interface application for converting Caldera/Summa Print and Cut Job Files to SVG format with layered output support.

## Features

- **File Support**: Converts both `.cut` and `.txt` Print and Cut job files to SVG
- **Layered Output**: Automatically creates separate layers for different tools/colors
- **GUI Interface**: User-friendly graphical interface with file selection and settings
- **Configurable Settings**: Adjustable scale factor and color settings
- **Progress Tracking**: Real-time progress indicators and status updates
- **Standalone Executable**: No Python installation required - runs as a single .exe file

## Layered Output Structure

When "Create separate layers" is enabled, the application organizes elements into distinct layers:

- **PDFTrimBox Layer**: Contains trim box elements
- **Cut Layer**: Contains cutting tool paths and registration marks
- **Tool-Specific Layers**: Additional layers for other detected tools/colors

Each layer is a separate SVG group (`<g>`) with meaningful IDs and classes for easy manipulation in vector graphics software.

## Installation & Usage

### Option 1: Standalone Executable (Recommended)

1. Download `PrintCut_to_SVG_Converter.exe` from the `dist` folder
2. Double-click the executable to run the application
3. Alternatively, use the provided batch file: `Run_PrintCut_Converter.bat`

### Option 2: From Source Code

1. Ensure you have Python 3.7+ installed
2. Install dependencies: `pip install -r requirements.txt`
3. Run the GUI: `python printcut_to_svg_gui.py`

## How to Use

1. **Launch the Application**
   - Double-click `PrintCut_to_SVG_Converter.exe`
   - Or run `python printcut_to_svg_gui.py` if using source

2. **Select Input File**
   - Click "Browse..." next to "Input File"
   - Choose your `.cut` or `.txt` job file
   - The output filename will be auto-suggested

3. **Configure Settings** (Optional)
   - **Scale Factor**: Default 25.4 (inches to mm conversion)
   - **Colors**: Customize path, rectangle, and trim box colors
   - **Layers**: Check "Create separate layers for different tools" (recommended)

4. **Convert**
   - Click "Convert to SVG"
   - Monitor progress in the status area
   - The SVG file will be created in your specified location

## File Structure

```
├── dist/
│   └── PrintCut_to_SVG_Converter.exe    # Standalone executable
├── printcut_to_svg_gui.py              # Main GUI application
├── printcut_to_svg.py                  # Conversion engine
├── Run_PrintCut_Converter.bat          # Launch batch file
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Building the Executable

To create your own executable from source:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "PrintCut_to_SVG_Converter" printcut_to_svg_gui.py
```

The executable will be created in the `dist` folder.

## System Requirements

- **Standalone Executable**: Windows 7+ (no additional software required)
- **Source Code**: Python 3.7+ with tkinter (included in most Python installations)

## Technical Details

- **Input Formats**: Caldera/Summa Print and Cut Job Files (v1.0)
- **Output Format**: SVG with optional layered structure
- **Scale Conversion**: Configurable unit conversion (default: inches to mm)
- **Dependencies**: svgwrite (for SVG generation), tkinter (for GUI)

## Troubleshooting

### Application won't start
- Make sure you're running the executable from the `dist` folder
- Try running as administrator
- Check that antivirus software isn't blocking the executable

### Conversion fails
- Verify the input file is a valid Print and Cut job file
- Check file permissions on the output directory
- Ensure the input file isn't corrupted

### Layers not working
- Enable "Create separate layers for different tools" in the settings
- Different tools/colors must be present in the job file for layers to be created

## License

This software is provided as-is for converting Print and Cut job files to SVG format.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your input files are valid Print and Cut job files
3. Ensure you have proper file permissions

## Version History

- **v1.0**: Initial release with GUI and layered output support
- Added standalone executable packaging
- Improved file format detection and error handling