from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

## config start
txtFileName = str(time.time_ns())+'_output.txt' # Name txt file!
excelFileName = str(time.time_ns())+'_output'+'.xlsx' # Name exel file!

keysTableHead = ["table","thead","tr","td"] # keys to find the head table row
keysTableBody = ["tr","td"] # keys to find the body table row

MainIdentifyPos = 2 # Main identificator position around  (Started with 1)
MaxCountItemsInRow = 13 # Max items in row in parse table

bNetworkHtml = False
urls = ["TestTable"]

bSaveHtml = False # Save html's? (False/True)

bSaveDataInTxtFormat = False # Save out data in txt files? (False/True)
bSaveDataInExcelFormat = True # Save out data in exel files? (False/True)
namesSheets = ["Sheet_1",
               "Sheet_2",
               "Sheet_3",
               "Sheet_4",
               "Sheet_4"] # Name of sheet will was smallest 31 character

bUseCustomStartRow = False # Use custom StartRow (config)? (False/True)
bUseHeaderTable = False # Use auto headerer in a table for StartRow? (False/True)
StartRow = [ 
        "№",
        "НОМЕР ЗАЯВЛЕНИЯ",
        "СНИЛС/УИА",
        "ЗАЧИСЛЕНИЕ БЕЗ ВИ",
        "СУММА (ВИ+ИД)",
        "СУММА (ВИ)",
        "ИД",
        "ОБЩЕСТВОЗНАНИЕ",
        "РУССКИЙ ЯЗЫК",
        "МАТЕМАТИКА",
        "ПРЕИМУЩЕСТВЕННОЕ ПРАВО НА ПОСТУПЛЕНИЕ",
        "ЛЬГОТА",
        "ОРИГИНАЛ ДОКУМЕНТА ОБ ОБРАЗОВАНИИ",
        "ПРИОРИТЕТ",
        "ПРОХОДИТЕ ИЛИ НЕ ПРОХОДИТЕ?"] # Start row in all Sheets in excel or text files. Count items in StartRow must be = MaxCountItemsInRow value

## 
##
##
##
##
##
## config end










cooldown = 0.35 # cooldown 
namesFileHtml = []
startData = {}
data = {}

class RowInfo:
    def __init__(self, idendificate):
        self.idendificate = ''
        self.data = ["*" for i in range(MaxCountItemsInRow)] # self.data = ["*" for i in range(countRowItems)]
    def output(self, between):
        result = ''
        for item in self.data:
            result += item + between
        return result
    
def rowTdRecycling(listItemRow, dictionary):
    # check, can MainIdentifyPos out of list range
    if (MainIdentifyPos - 1)  > len(listItemRow):
        #print('func rowTdRecycling(): listItemRow {', str(len(listItemRow)), '} identificatePos: {',str(identificatePos), '}')
        return

    
    identify = listItemRow[MainIdentifyPos-1]
    #add in dictionary. Have dictionary this idendificator?
    if dictionary.get(identify)== None:
        dictionary[identify] = RowInfo(identify) # create new record

    pos = 0
    for item in listItemRow:
        if pos >= MaxCountItemsInRow:
            break
        oldText = dictionary[identify].data[pos]
        dictionary[identify].data[pos] = dictionary[identify].data[pos].replace(oldText, item)
        pos+=1
    
def parseHtml(contents,index):

    bs = BeautifulSoup(contents,"html.parser") # BeautifulSoup(contents, 'html')

    # Parse table head
    if bUseHeaderTable == True:
        parseHtmlWithKeys(bs,0,keysTableHead,startData)

    # CustomStartRow
    if bUseCustomStartRow == True:
        #create
        identify = namesFileHtml[index]
        startData[identify] = RowInfo(identify)
    
        pos = 0
        for item in StartRow:
            oldText = startData[identify].data[pos]
            startData[identify].data[pos] = startData[identify].data[pos].replace(oldText, item)
            pos+=1
                
    # Parse table body
    parseHtmlWithKeys(bs,0,keysTableBody,data)

def parseHtmlWithKeys(html, index, keysTable, dictionary):
    if index == len(keysTable):
        return None
    if html.find_all(keysTable[index]) == None:
        print('Error key for parse: ' + keysTable[index])
        exit(-1)
    
    if index == (len(keysTable)-1): # ['tr','td']
        listRow = []
        for item in html.find_all(keysTableBody[len(keysTable)-1]):
            title = item.text
                        
            title = title.strip()
            listRow.append(title)
                
        rowTdRecycling(listRow,data)
            
    else:
        pos = 0
        for htmlChild in html.find_all(keysTable[index]):
            if index == 1:
                print(index, pos)
            parseHtmlWithKeys(htmlChild, index+1, keysTable, dictionary)
            pos += 1


def SiteDownload(index):
    ### Download page
    r = requests.get(urls[index]) #url - reference
    html = r.text
    ### Save page
    if bSaveHtml == True:
        f = open(namesFileHtml[index]+'.html','w', encoding='utf-8')
        f.write(html)
        f.close()
    return html

def printFileInTxt(index):
    fw = open(txtFileName, 'w', encoding='utf-8')
    # Write head row data
    for startStr in startData:
        fw.write(startData[startStr].output('\t') + '\n')
        break

    # Write body Rows data
    for row in data:
        fw.write(data[row].output('\t') + '\n')
        
    fw.close()


def converterToExelData():
    # data = {class, class}
    # class.data = ['info1', 'info2', 'info3']

    # listExel  [ col-x1 = [col-x1y1,col-x1y2,col-x1y3,col-x1y4]]
    #           [ col-x2 = [col-x2y1,col-x2y2,col-x2y3,col-x2y4]]
    listExel = []
    for clasY in data.values():
        listClass = clasY.data
        listExel.append(clasY.data)
    return listExel

dataSheets = []
def memorySheetsSave(index):

    listExel = converterToExelData()
    if bUseCustomStartRow == True:
        df = pd.DataFrame(listExel, columns=StartRow) # index=['one', 'two', 'three']
    elif bUseHeaderTable == True:
        df = pd.DataFrame(listExel, columns=startData[namesFileHtml[index]])
    else:
        df = pd.DataFrame(listExel)

    dataSheets.append(df)


def writeSheetsToExcel():
    writer = pd.ExcelWriter(excelFileName, engine='xlsxwriter')
    index = 0
    for sheet in dataSheets:
        if (bUseCustomStartRow == True) and (bUseHeaderTable == True):
            sheet.to_excel(writer, sheet_name=namesSheets[index],index=False)
        else:
            sheet.to_excel(writer, sheet_name=namesSheets[index],index=False, columns=None)
        index += 1
    writer._save()



def parseMain():
    if len(namesFileHtml) == 0:
        for pos in range(len(urls)):
            namesFileHtml.append('site'+str(pos+1))
            
    for index in range(len(urls)):
        html = ''
        
        if bNetworkHtml == True:
            html = SiteDownload(index)
            print("[Downloaded] ",urls[index][35:])
        else:
            fileHtml = open(urls[index]+'.html','r',encoding='utf-8')
            html = fileHtml.read()
            print("[Open File Html] Open: ",urls[index])
            fileHtml.close()
            
        parseHtml(html,index)
        
        if bSaveDataInTxtFormat == True:
            printFileInTxt(index)
            print("[Pass]\t\tTable saved in txt")
        
        if bSaveDataInExcelFormat==True:
            memorySheetsSave(index)
            print("[Pass]\tSheet table saved in memory")

        startData.clear() 
        data.clear() 
        
        time.sleep(cooldown)
        
    if bSaveDataInExcelFormat == True:
        writeSheetsToExcel()
        print("[Success] Full excel table saved!")

    input("\n\nPress Enter to continue...")


parseMain()

