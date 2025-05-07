import pymongo
import openpyxl





def LoadData(excelSheet,sheetName,numberOfRecords):

    print("Establishing connection")
    client = pymongo.MongoClient()
    db = client.MoneyLaundering

    try:
        db.bankingTransactions.drop()
        print("Successfully dropped the table bankingTransactions")
        db.mappedTransactions.drop()
        print("Successfully dropped mapped transactions")
        db.tupleList.drop()
        print("Successfully dropped tupleList transactions")
    except Exception as e:
        print("Deletion Unsuccessful : {}".format(str(e)))


    wb = openpyxl.load_workbook(excelSheet)
    sheet = wb.get_sheet_by_name(sheetName)
    #row will contain individual rows of the excel sheet
    row = []
    #row list contains all the rows of excel sheet
    row_list = []
    #from 2nd to 1000th row
    for i in range(2,numberOfRecords):
        row = []
        #from 1st to 11th column
        for j in range(1,11):
            row.append(sheet.cell(row=i, column=j).value)
        row_list.append(row)

    #Defining the Schema with some default values
    document = {
                "hour":0,
                "type":"",
                "amount":0.0,
                "nameOrig":"",
                "oldBalanceOrig":0.0,
                "newBalanceOrig":0.0,
                "nameDest": "",
                "oldBalanceDest":0.0,
                "newBalanceDest":0.0,
                "isFraud":0,
                "isFlaggedFraud":0
                }
    keys = []
    for key in document.keys():
        keys.append(key)
    #Keys List contains all the attributes of Dictionary Object

    #Bulk Data is a List of dictionary objects which will be inserted into MongoDB database as a JSON object.
    bulkData = []
    from tqdm import tqdm
    for row in tqdm(row_list):
        index = 0
        for col in row:
                document[keys[index]] = col
                index +=1
        #Creatinga a shallow copy of the dictionary document
        bulkData.append(document.copy())
    #Inserting bulk Data
    db.bankingTransactions.insert_many(bulkData)
    print("All Data successfully Inserted")