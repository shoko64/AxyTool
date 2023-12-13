# AxyTool
Tool for editing AxySnake textures (also kinda works with AirXonix)

![image](https://github.com/shoko64/AxyTool/assets/24816370/98a7cbcf-d447-4520-85d3-6e0364542a3f)

# Installation
1. Clone the repository
 ```git clone https://github.com/shoko64/AxyTool.git```
3. Install the requirements
 ```pip install -r requirements.txt```
4. Run the program
 ```python main.py```

# Usage

## Opening a pack file (AxySnake)
1. Press the open file button in the program
2. Locate your AxySnake installation directory
3. Select the file: ```bmppack.bin```

## Opening a pack file (AirXonix)
1. Locate your AirXonix installation directory
2. Open the file: ```program.exe``` using a hex editor
3. Find the hard-coded pack file within the hex data of the EXE file (should be 0x44730-0xB4180 in the latest version)
4. Create a new file with the data and then select it in the program

#
### Replacing BMP files
When replacing a BMP file you must verify that:
- The imported file is a 16 bit BMP file
- The imported file has the same dimensions as the texture that you are replacing
- The imported file is flipped vertically
