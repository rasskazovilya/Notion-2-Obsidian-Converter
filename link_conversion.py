import pathlib
import typing
import re
from utils import del_uid,  del_symbols
from unicodedata import normalize
from urllib.parse import unquote


def convert_links(path: pathlib.Path, properties: typing.Dict[str, typing.Sequence[str]]):
    for file in path.glob('**/*.md'):
        fileProperty = []

        for parent in file.parts[:-1]:
            if parent in properties:
                fileProperty = list(properties[parent])

        with open(file, mode='r', encoding='utf-8') as convertingFile:
            fileText = list(map(lambda line: del_uid(normalize('NFC', unquote(line))), convertingFile.readlines()))

        fileText = convert_link_to_database(fileText)
        fileText = convert_page_properties(fileText, fileProperty)
        fileText = convert_attachment(fileText, file.parts[-2])
        fileText = convert_notion_links(fileText)
        #fileText = convert_blank_links(fileText)

        with open(file, mode='w', encoding='utf-8') as convertedFile:
            [print(line, file=convertedFile) for line in fileText]
            pass


def convert_link_to_database(text: typing.List[str]):
    # Unfortunately, Notion does not export filter settings for linked DBs,
    # so there is no point in converting links to .csv files to somewhat comprehensible for Obsidian
    # Therefore we should look for .md references and convert them to [[]] type of links
    regexBacklinkPage = re.compile('^.*\[(.+)\]\(([^\(]*)(?:\.md)\)$')

    for index, line in enumerate(text):
        if '.csv' in line:
            line = ''

        matchBacklinksPage = regexBacklinkPage.findall(line)

        if matchBacklinksPage is not None:
            for match in matchBacklinksPage:
                linkTitle = match[0]
                linkPage = match[1]

                if linkTitle in linkPage:
                    line = '[[' + del_symbols(linkTitle) + ']]'
                    #line = line.replace('[' + linkTitle + ']', '[[' + del_symbols(linkTitle) + ']]')
                    #line = line.replace('(' + linkPage + '.md)', '')
                else:
                    linkPage = linkPage[linkPage.rfind('/') + 1:]
                    line = '[[' + del_symbols(linkPage) + '|' + linkTitle + ']]'
                    #line = line.replace('[' + linkTitle + ']', '[[' + del_symbols(linkPage) + '|')
                    #line = line.replace('(' + match[1] + '.md)', linkTitle + ']]')

        text[index] = line

    return text


def convert_attachment(text: typing.List[str], folder: str):
    # 
    regexAttachment = re.compile("!\[(.*)\]\((.*)\)") # [^\[\]\(\)]
    
    for i, line in enumerate(text):
        matchAttachment = regexAttachment.match(line)
        
        if matchAttachment is not None:
            folderAttachment = del_symbols(matchAttachment.group(1).partition('/')[0])
            nameAttachment = matchAttachment.group(1).partition('/')[2]

            name, *suffix = nameAttachment.split('.')

            nameAttachment = nameAttachment.replace(name, del_symbols(name))
            
            line = f'![[{folder}/{folderAttachment}/{nameAttachment}]]'

        text[i] = line
    return text


def convert_notion_links(text: str):
    return text


def convert_blank_links(text: str):
    regexBlankLink = re.compile("\[(.[^\[\]\(\)]*)\]\(about:blank#.[^\[\]\(\)]*\)")

    for i, line in enumerate(text):
        matchBlank = regexBlankLink.match(line)
        
        if matchBlank is not None:
            blankName = matchBlank.group(1)
            
            line = '![[' + blankName + ']]'

        text[i] = line
    return text


def convert_page_properties(text: typing.List[str], properties: typing.List[str]):
    # Converts page properties to Dataview plugin inline format (with ::)
    # Links from relations are converted simply to Obsidian [[]] type of links
    
    # number of property lines equals length of property list + 1 line of note header and 1 blank line 
    numberOfPropertyLines = len(properties) + 2

    for index, line in enumerate(text[2:numberOfPropertyLines], 2):
        splitted = line.split(':', maxsplit=1)

        if len(splitted) == 1:
            text[index] = line
            continue
        else:
            pageProperty, values, *other = splitted

        if pageProperty in properties:
            if '../' in values:
                newValues = ''
                values += ','

                for value in values.split('d,')[:-1]:
                    value = convert_linked_property(value, pageProperty)
                    newValues += ' ' + value

                values = newValues
            line = convert_property(pageProperty) + values

        text[index] = line

    return text


def convert_linked_property(line: str, pageProperty: str):
    # "Relation" property exports to list of all connected pages' names
    # So we just need to replace "../path/" with empty strings
    # and leave only links to files
    line = line.replace('../' + pageProperty + '/', '')
    line = del_symbols(line.replace('.m', ''))

    return '[[' + line + ']]'


def convert_property(line: str) -> str:
    # Page properties other than relations stay as they are
    line = line + ':: -'
    return line

