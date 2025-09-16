# msTOgh2

**msTOgh2** is a python script for converting **Moonscraper RB2 MIDI exports** into **GH2** with full **animations support**.
With it, you can chart in Moonscraper and automatically generate a GH2 chart that includes all animations.

## Installing Python and Mido

Download and install python: https://www.python.org/downloads/

When running the installer, make sure to check the box on the first screen: `Add Python to PATH`

Run the command `pip install mido` in cmd to install mido library.

## Usage

1. Create your chart in **Moonscraper**.
2. Export it as an **RB2 MID** at **480** resolution.
3. Run **msTOgh2.py** in the same folder the mid is.
4. The script will produce a new `_gh2.mid` file ready for GH2.

If you encounter errors or the MIDI conversion doesn’t work as expected, try
running `run.bat` instead of the python file directly

You may still need to drag the mid into **REAPER** and export to make sure the formatting is correct
*(this was an issue in the first msTOgh2, I guess now it's fixed but I'm still not 100% sure)*

## Animation Reference

To know which events and notes you need to place in Moonscraper to trigger animations in GH2, please check the reference spreadsheet:  
https://docs.google.com/spreadsheets/d/1_l0bjYNhPV2ditcbrW0UQlz_jqsaiQSn/edit?usp=sharing&ouid=116981090282877738182&rtpof=true&sd=true

or:  

https://drive.google.com/file/d/1y79LLlE5AnLvHCzaFQibd3NPAmb0keS3/view?usp=sharing

## Adding GH2 Events to Moonscraper

You can replace the files: `global_events.txt` and `local_events.txt` inside "MS Events" folder to "Config" folder of your Moonscraper installation.  
This way, all events will be listed and ready to use for global and local events.

## Validator

Function inside the script that checks local events to avoid erros and crashes, made by Naonemeu *https://github.com/naonemeu*  
If there is any problems with your MIDI related to local events,
the script will show a warning in the prompt at the end of each individual MIDI conversion.

## Animation Tutorials

Dump of animation references and tutorials you can read in the internet:

https://archives.somnolescent.net/web/mari_v3/games/gh2/tutorials/animation-reference/  
*by mariteaux: https://www.youtube.com/@mariteaux*

https://www.scorehero.com/forum/viewtopic.php?t=1179  
*by Riff: https://www.youtube.com/channel/UCEo6wS1tSl9e7_zdUhGt3Ew*

https://drive.google.com/file/d/1QTKDJxASvlqpkMWguREhy5do_XtDwFdc/view  
*by Stanley Jones: https://www.youtube.com/@S%C3%B3tanoRockerosGamers*

https://github.com/naonemeu/gh2_tutorial/wiki/%5BX1%5D-Chart-%E2%80%90-Anima%C3%A7%C3%A3o-e-luzes  
*by Naonemeu: https://www.youtube.com/@Naonemeugh2*
