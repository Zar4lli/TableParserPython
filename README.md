<h1 align="right">#TablePythonParser</h1>
<h4 align="left">This script is needed to parse information from web pages. The data can be immediately used in text format or in an excel.</h4>

<p align="center"> <img src="https://github.com/Zar4lli/TableParserPython/blob/main/gifMaker.gif" width="100%"> </p>


# Install
To use the script, you need to install [Python](https://www.python.org/downloads/) . 
Select the following options in the `CUSTOMIZIZE INSTALL`:
- Choose `add python.exe to PATH`
- Choose `pip install`
- Choose `add python to environment variables`



After successfully installing python, you need to install packages. 

Enter these commands on the `Command Prompt`: 

> pip install requests

> pip install beautifulsoup4

> pip install pandas

> pip install openpyxl xlsxwriter xlrd

# Usage
## Online Use
In the `HtmlTableParser.py`, edit the following lines:

> bNetworkHtml = `True`

// Switches the script to online parsing mode

> bSaveDataInExcelFormat = `True`

// Switch to save file to excel spreadsheet

> urls = ["`https://your-target-site.com/table1.html`",
        "`https://your-target-site.com/table2.html`",
        "`https://your-target-site.com/table3.html`"]

// Enter addresses where you want to parse the table in the urls list

> MainIdentifyPos = `1`

// This must be the number of the unique column in the row. which must not be repeated

> MaxCountItemsInRow = `15`

 // Enter max count rows in the line

## Ofline Use
In the `HtmlTableParser.py`, edit the following lines:

> bNetworkHtml = `False`

// Switches the script to offline parsing mode

> bSaveDataInExcelFormat = `True`

// Switch to save file to excel spreadsheet

> urls = ["`downloadHtmlFile1`",
        "`downloadHtmlFile2`",
        "`downloadHtmlFile3`"]

// Move the HTML to a folder next to the script. And enter file names in the urls list (without .html format)

> MainIdentifyPos = `1`

// This must be the number of the unique column in the row. which must not be repeated

> MaxCountItemsInRow = `15`

// max count rows in the line

## In Future

- Add the ability to combine lists into one table









