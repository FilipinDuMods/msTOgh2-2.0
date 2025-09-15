# msTOgh2

**msTOgh2** is a python script for converting **Moonscraper RB2 MIDI exports** into **GH2** with full **animations support**.
With it, you can chart in Moonscraper and automatically generate a GH2 chart that includes all animations.

## Installing Python and Mido

Download and install python using this link:
https://www.python.org/downloads/

*When running the installer, make sure to check the box on the first screen:
*“Add Python to PATH”

Run the command `pip install mido` in cmd to install mido library.

## Usage

1. Create your chart in **Moonscraper**.
2. Export it as an **RB2 MID** at **480** resolution.
3. Run **msTOgh2.py** in the same folder the mid is.
4. The script will produce a new `_gh2.mid` file ready for GH2.

You may still need to drag the mid into **REAPER** and export to make sure the formatting is correct
*(this was an issue in the first msTOgh2, I guess now it's fixed but I'm still not sure)

## Animation Reference

To know which events and notes you need to place in Moonscraper to trigger animations in GH2, please check the reference spreadsheet:


## Validator (WIP)

Script inside the tool that validates local and global events to avoid erros and crashes, made by Naonemeu
*Soon, testing
