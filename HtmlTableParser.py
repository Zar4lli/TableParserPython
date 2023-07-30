from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

## config start
txtFileName = str(time.time_ns())+'_output.txt' # don't touch!
excelFileName = str(time.time_ns())+'_output'+'.xlsx' # don't touch!

keysTableHead = ["thead","tr","th"] # Max 3 keys. Needed to looping in tHead table. [items, keys]
keysTableBody = ["tbody","tr","td"] # Max 3 keys. Needed to looping in tBody table. [items, keys]

MainIdentifyPos = 2 # Main identificator position around 
MaxCountItemsInRow = 15 # Max items in row in parse table

urls = ["https://pk-vo.mgpu.ru/pk/dictionary/competitive-group-rating?competitiveGroupId=3067",
        "https://pk-vo.mgpu.ru/pk/dictionary/competitive-group-rating?competitiveGroupId=3053",
        "https://pk-vo.mgpu.ru/pk/dictionary/competitive-group-rating?competitiveGroupId=3054",
        "https://pk-vo.mgpu.ru/pk/dictionary/competitive-group-rating?competitiveGroupId=3048"]

bSaveHtml = False # Save html's? (False/True)
namesFileHtml = ["competitiveGroupId3067",
                 "competitiveGroupId3053",
                 "competitiveGroupId3054",
                 "competitiveGroupId3048"] # name's for html files. Only when bSaveHtml = True

bSaveDataInTxtFormat = False # Save out data in txt files? (False/True)
bSaveDataInExcelFormat = True # Save out data in exel files? (False/True)
namesSheets = ["Пед образование(СДПП)",
               "Бизнес-информатика",
               "Педагогическое образование",
               "Гос и муниц управление"] # Name of sheet will was smallest 31 character


bUseHeaderTable = True # Use auto headerer in a table for StartRow? (False/True)
bUseCustomStartRow = False # Use custom StartRow (config)? (False/True)
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

cooldown = 0.35 # cooldown 

## 
##
##
##
##
##
## config end












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
    if MainIdentifyPos > len(listItemRow):
        #print('func rowTdRecycling(): listItemRow {', str(len(listItemRow)), '} identificatePos: {',str(identificatePos), '}')
        return

    
    identify = listItemRow[MainIdentifyPos]
    #add in dictionary. Have dictionary this idendificator?
    if dictionary.get(identify)== None:
        dictionary[identify] = RowInfo(identify) # create new record

    pos = 0
    for item in listItemRow:
        if pos > MaxCountItemsInRow:
            break
        oldText = dictionary[identify].data[pos]
        dictionary[identify].data[pos] = dictionary[identify].data[pos].replace(oldText, item)
        pos+=1


startData = {}
data = {}
def parseHtml(contents,index):

    table = BeautifulSoup(contents,"html.parser").table # BeautifulSoup(contents, 'html')
    #Parse table Head
    
    if bUseHeaderTable == True:
        for thead in table.find_all(keysTableHead[0]):
            for row in thead.find_all(keysTableHead[1]):
                listRow = []
                
                for item in row.find_all(keysTableHead[2]):
                    title = item.text
                    title = title.strip()
                    listRow.append(title)

                rowTdRecycling(listRow, startData)

    

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
                
    #Parse table Body
    for tbody in table.find_all(keysTableBody[0]):
        for row in tbody.find_all(keysTableBody[1]):
            listRow = []
                
            for item in row.find_all(keysTableBody[2]):
                title = item.text
                title = title.strip()
                listRow.append(title)

            rowTdRecycling(listRow,data)
            
    
    
def urlDownload(index):
    ### download page
    r = requests.get(urls[index]) #url - reference
    html = r.text
    ### Save page
    if bSaveHtml == True:
        f = open(namesFileHtml[index],'w', encoding='utf-8')
        f.write(html)
        f.close()
    ###

    
    count = 0
    #with open(namesFileHtml[index], "r", encoding='utf-8') as f:
        #contents = f.read()
    
    #tempNumber = ''
    return html

        

def printFileInTxt(index):
    fw = open(namesFileHtml[index]+'.txt', 'w', encoding='utf-8')
    #write First String
    for startStr in startData:
        fw.write(startData[startStr].output('\t') + '\n')
        break

    #write rows data
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
    df = pd.DataFrame(listExel, columns=StartRow) # index=['one', 'two', 'three']

    dataSheets.append(df)
    #df.to_excel( 'pandas_to_excel_no_index_header.xlsx' , index= False , header= False )

##    printInFile(data, str(time.time_ns())+'output', napravlenii,False)
##    printInFile(data, str(time.time_ns())+'output', napravlenii,True)


def writeSheetsToExcel():
    writer = pd.ExcelWriter(excelFileName, engine='xlsxwriter')
    index = 0
    for sheet in dataSheets:
        sheet.to_excel(writer, sheet_name=namesSheets[index],index=False)
        index += 1
    writer._save()



def parseMain():
    for index in range(len(urls)):
        
        html = urlDownload(index)
        print("[Downloaded] ",urls[index][35:])
        parseHtml(html,index)
        
        if bSaveDataInTxtFormat == True:
            printFileInTxt(index)
            print("[Pass]\t\tTable saved in txt")
        
        if bSaveDataInExcelFormat==True:
            memorySheetsSave(index)
            print("[Pass]\t\tSheet table saved in memory")

        startData.clear() #
        data.clear() #
        
        time.sleep(cooldown)
        
    if bSaveDataInExcelFormat == True:
        writeSheetsToExcel()
        print("[Success] Full excel table saved!")

    input("\n\nPress Enter to continue...")


parseMain()

