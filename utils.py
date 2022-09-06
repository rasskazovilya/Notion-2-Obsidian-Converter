import re

def del_uid(line):
    '''
    Deletes 32 character UID after the file name
    Replace "%20" with space
    Replace space+slash with just slash
    '''
    
    regexUID = re.compile('\s+\w{32}')
    regex20 = re.compile("%20")
    regexSlash = re.compile("\s\/")

    line = regex20.sub(" ", line)
    line = regexUID.sub("", line)
    line = regexSlash.sub("/", line).strip()
    
    return line


def del_symbols(line):
    '''
    Delete all symbols that are not word or whitespace character
    It is needed to avoid illegal characters in filenames
    '''
    regexSymbols = re.compile('[^\w\s]')
    line = regexSymbols.sub(' ', line).strip()
    return re.sub(' {2,}', ' ', line)

