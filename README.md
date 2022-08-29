## Notion 2 Obsidian converter
In this repo I tried to write my own notion to obsidian converter. A lot of code was written when I was studying Python so it may seem a bit messy. Anyway, it gets job done as far as I can tell. 

Parsing links with RegExp was taken from [this repo](https://github.com/visualcurrent/Notion-2-Obsidan). Basically, all the Notion links should work properly in Obsidian after conversion.

I tweaked a bit of code to work with extended unicode (tested on russian, can't tell if it works for other languages).

Also I wanted to add a support for [Dataview plugin for Obsidian](https://github.com/blacksmithgu/obsidian-dataview):
- custom delimiter for inline fields;
- generating notion-like tables with Dataview queries.
Consider it as Work In Progress.

## Usage
1. Download data from Notion>Settings & Members>Settings>Export content>Export all workspace content
2. Unzip archive to the script folder
3. Change the directory on 11 line in `NotionObsidianConverter.py`
4. Run `python NotionObsidianConverter.py`
5. Copy your converted data from `NotionConverted` in script folder to your Obsidian vault
6. Check if links work correctly and naming is right.

## TODO
- [ ] Command line arguments
- [ ] OOP rewrite
- [ ] Custom Dataview delimiter
- [ ] Proper Dataview queries for Notion linked databases