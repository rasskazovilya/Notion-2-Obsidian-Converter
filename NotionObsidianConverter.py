import csv
import pathlib
import shutil
import typing

from link_conversion import *
from utils import del_symbols, del_uid


def main():
    notionUnzippedPath = pathlib.Path('Export-75a706a2-3467-4a10-9233-507ce6c64957')
    notionConvertedPath = pathlib.Path('NotionConverted')

    if notionConvertedPath.exists():
        shutil.rmtree(notionConvertedPath)
    
    shutil.copytree(notionUnzippedPath, notionConvertedPath)

    bulk_file_rename(notionConvertedPath)

    csvFiles = [file for file in notionConvertedPath.glob('*.csv')]

    csvHeaders = {file.with_suffix('').name:csv.DictReader(file.open('r', encoding='utf-8-sig')).fieldnames for file in csvFiles}

    csv_to_md(notionConvertedPath)

    remove_duplicate_csv_files(notionConvertedPath, csvFiles)

    convert_links(notionConvertedPath, csvHeaders)

    pass


def bulk_file_rename(path: pathlib.Path):
    '''
    Every imported Notion file has 32 characters at the end of a file.
    They should be deleted. After deletion there will be duplicate files with the same name.
    So the function counts dupes in folder and rename every duplicate according to this counter.
    '''

    duplicateFolderCounter = 0
    duplicateFileCounter = 0

    for file in path.glob('*'):
        if file.is_dir():
            bulk_file_rename(file)
        
        filenameClean = pathlib.Path(del_symbols(del_uid(file.with_suffix('').name))).with_suffix(file.suffix)

        newFile = pathlib.Path(file.parent / filenameClean)

        if newFile == file:
            continue
        
        if newFile.exists():
            if newFile.is_file():
                duplicateFileCounter += 1
            if newFile.is_dir():
                duplicateFolderCounter += 1

            newFilename = str(newFile.with_suffix('').name + f'_{duplicateFileCounter}' + file.suffix)
            newFile = pathlib.Path(file.parent / newFilename)
            
        file.rename(newFile)
    return


def remove_duplicate_csv_files(path: pathlib.Path, rootCSVFiles: typing.List[pathlib.Path]):
    '''
    Duplicate .csv files appear if Notion's linked databases are mentioned on a page.
    New folder is created, containing duplicate .csv alongside with .csv from inline tables on page.
    So we need to delete them in order not to mess up backlinks in Obsidian.

    '''

    rootCSVFilenames = [file.name for file in rootCSVFiles]
    
    for file in path.glob('*'):
        if file.is_dir():
            remove_duplicate_csv_files(file, rootCSVFiles)
            if not list(file.glob('*')):
                file.rmdir()
        else:
            if file.name in rootCSVFilenames:
                file.unlink()

    return


def csv_to_md(path: pathlib.Path):
    '''
    In root folder some .csv files are left. We need to make .md files with obsidian links from them.
    .csv files are deleted after creation of .md files.
    '''
    for file in path.glob('*.csv'):
        folderCSV = path / pathlib.Path(file.with_suffix('').name)
        
        filesFromCsv = [fileFromCsv.with_suffix('').name for fileFromCsv in folderCSV.glob('*.md')]
        text = ''.join(['[[' + file.with_suffix('').name + '/' + fileFromCsv + ']]\n' for fileFromCsv in filesFromCsv])

        newMdFile = file.with_suffix('.md')
        newMdFile.write_text(text, encoding='utf-8')
        
        file.unlink()


if __name__ == "__main__":
    main()

