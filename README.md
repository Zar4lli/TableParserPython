<h1 align="right">#TablePythonParser</h1>
<h4 align="left">This script is needed to parse information from web pages. The data can be immediately used in text format or in an excel.</h4>

<p align="center"> <img src="https://github.com/Zar4lli/TableParserPython/blob/main/gifMaker.gif" width="100%"> </p>


## Install
To use the script, you need to install [Python](https://www.python.org/downloads/) . Select the following options in the **customizize install**:

> Choose "add python.exe to PATH"

> Choose "pip install"

> Choose "add python to environment variables"



After successfully installing python, you need to install packages on the command line: 

> pip install beautifulsoup4

> pip install pandas

> pip install openpyxl xlsxwriter xlrd

## Configuration 

The global script settings(config) located in *HtmlTableParser.py*.
Here are the main settings that will come in handy in your work with this script.

>**keysTableHead = ["thead","tr","th"] # Max 3 keys. Needed to looping in tHead table. [items, keys]**
> <p># These keys are needed for web page parsing (bUseHeaderTable). </p>
> <p>!! Max 3 keys. !!</p>

>**keysTableBody = ["tbody","tr","td"] # Max 3 keys. Needed to looping in tBody table. [items, keys]**
> <p> These keys are needed for web page parsing. </p>
> <p>!! Max 3 keys. !!</p>

> **MainIdentifyPos = 5**
> <p> Used to identify each row in a table. </p>

> **MaxCountItemsInRow = 6**
> <p> Max items in row in parse table </p>
> <p>!! The value of this parameter must be equal to the number items in row (startRow) </p>

>**urls = ["https://google.com","https://google.com","https://google.com","https://google.com"]**
> <p> Links with tables for parsing </p>

> **bSaveHtml = False**
> <p>Save html's? </p>

> **namesFileHtml = ["google1","google2","google3","google4"]**
> <p> Your invented names for web pages (if you enable the download option)   </p>

> **bSaveDataInTxtFormat = False**
><p>Save out data in txt files?</p>

> **bSaveDataInExcelFormat = True**
><p>Save out data in exel files? </p>

> **namesSheets = ["googleSite1","googleSite2","googleSite3", "googleSite4"]**
> <p>Your invented names for excel tabs </p>
> <p>!! Name should be less 31 character !! </p>

> **bUseHeaderTable = True**
> <p>Whether to use the automatically generated form of the beginning of the table/txt?</p>

> **bUseCustomStartRow = False**
> <p>Whether to use your custom blank at the beginning of the table/txt?</p>

> **StartRow = ["№", "id","name", "age","last name", "last seen"]**
> <p>Start row in all Sheets in excel or text files. </p>
> <p> !! The number of elements must be equal to MaxCountItemsInRow !!</p>














