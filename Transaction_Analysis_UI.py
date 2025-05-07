from tkinter import *
from MongoConnection import LoadData
import FrequentTransactions as ft

def createDatabase():
    excelSheet = e1.get()
    sheetName = e6.get()
    numberOfRecords = e7.get()
    LoadData(str(excelSheet),str(sheetName),int(numberOfRecords))

def showFrequentTransactions():
    print("Tuple List")
    tupleList = ft.mapCustomers()
    print("Total Number of Transactions : ", len(tupleList))

    print("Actual Frequency of Transactions : ")
    actualTransFreq = ft.actualCount(tupleList)

    print("Hash Based Bucket Count : ")
    bucketContainer = ft.hashBasedBucketCount(tupleList)

    bucketThreshold = e2.get()
    print("Filtered transactions(On Basis of Bucket Count) : ")
    filteredBucketTuples = ft.filterOnBucketCount(tupleList, bucketContainer, int(bucketThreshold))
    e4.insert(0,len(filteredBucketTuples))

    actualCountThreshold = e3.get()
    print("Filtered Transactions(On Basis of actual Frequency) : ")
    actualCount = ft.filterOnActualCount(filteredBucketTuples, actualTransFreq, int(actualCountThreshold))
    e5.insert(0,len(actualCount))

    print(actualCount)

    for k,v in actualCount.items():
        list1.insert(END, k)


window = Tk()
window.geometry("600x600")
window.title("Transaction Analysis")

topFrame = Frame(window)
topFrame.pack(side = LEFT)


l1 = Label(topFrame,text = "Enter Excel Sheet")
l1.grid(row = 0, column = 0,columnspan = 2,pady = 10)
t1 = StringVar()
e1 = Entry(topFrame,textvariable=t1)
e1.grid(row = 0,column = 2,pady = 10,padx = 10)

l5 = Label(topFrame,text = "Enter Sheet Name")
l5.grid(row = 1, column = 0,columnspan = 2,pady = 10)
t6 = StringVar()
e6 = Entry(topFrame,textvariable=t6)
e6.grid(row = 1,column = 2,pady = 10,padx = 10)

l6 = Label(topFrame,text = "Number of Records")
l6.grid(row = 2, column = 0,columnspan = 2,pady = 10)
t7 = StringVar()
e7 = Entry(topFrame,textvariable=t7)
e7.grid(row = 2,column = 2,pady = 10,padx = 10)

button1 = Button(topFrame, text = "Create Database",command = createDatabase)
button1.grid(row = 3,column = 2,columnspan = 1,pady = 5)

# Frequent Transaction Frame first row
l2 = Label(topFrame,text = "Bucket count threshold:")
l2.grid(row = 4, column = 0,columnspan = 2,pady = 5)
t2 = StringVar()
e2 = Entry(topFrame,textvariable=t2)
e2.grid(row = 4,column = 2,pady = 5)


# Frequent Transaction Frame second row
l3 = Label(topFrame,text = "Transaction frequency threshold : ")
l3.grid(row = 5, column = 0,columnspan = 2,pady = 5)
t3 = StringVar()
e3 = Entry(topFrame,textvariable=t3)
e3.grid(row = 5,column = 2,pady = 5)

#Get Frequent Transactions
button2 = Button(topFrame, text = "Get frequent transactions",command = showFrequentTransactions)
button2.grid(row = 6,column = 2,pady = 5)

l3 = Label(topFrame,text = "Number of filtered Transactions from Bucket : ")
l3.grid(row = 7, column = 0,columnspan = 2,pady = 5)
t4 = StringVar()
e4 = Entry(topFrame,textvariable=t4)
e4.grid(row = 7,column = 2,pady = 5)

l4 = Label(topFrame,text = "Number of filtered Transactions based on actual count : ")
l4.grid(row = 8, column = 0,columnspan = 2,pady = 5)
t5 = StringVar()
e5 = Entry(topFrame,textvariable=t5)
e5.grid(row = 8,column = 2,pady = 5)


l4 = Label(topFrame,text = "List of Frequent Transactions:")
l4.grid(row = 9, column = 0,columnspan = 2,pady = 5)
list1 = Listbox(topFrame,width = 40,height = 15)
list1.grid(row = 9,column = 2,columnspan=2)

sb1 = Scrollbar(topFrame)
sb1.grid(row = 9,column = 4, rowspan = 15)
list1.configure(yscrollcommand = sb1.set)
sb1.configure(command = list1.yview)

window.mainloop()