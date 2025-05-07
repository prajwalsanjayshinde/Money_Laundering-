import pymongo
#import numpy as np
#from pandas import Series,DataFrame

#Connecting with the database

client = pymongo.MongoClient()
db = client.MoneyLaundering

#Mapping CustomerId with Number
#Forming a tuple List
def mapCustomers():

    """
    Description: Maps the customer ID with a number

    Input: All the transactions from MongoDB database
    (nameOrig : Id of Customer from whom the transfer is done)
    (nameDest : Id of Customer to whom the transfer is done)

    Output:  A map of customer Id with a number
            customerMap :
            { 'C1231006815' : 0,
              'M1979787155' : 1}
            tupleList :
            [(0,1),(1,2)...]
    """
    try:
        customerMap = {}
        edgeList = []
        transactions = db.bankingTransactions #Contains all the banking Transactions
        mappedTransactions = db.mappedTransactions #Contains all the mapped Transactions
        tuple_list_db=db.tupleList
        rowInsert = {}
        """
        [
        {"customerId" : nameOrig,
         "tupleId" : 1},
        {"customerId" : nameDest,
         "tupleId" : 2}
        ]
        """
        fromToTuple = transactions.find({},{'nameOrig':1,'nameDest':1,'_id':0})
        count = 0
        for transaction in fromToTuple:
             if transaction['nameOrig'] not in customerMap.keys():
                customerMap[transaction['nameOrig']] = count
                #Insertion into Mapped Transactions Database
                rowInsert["customerId"] = transaction['nameOrig']
                rowInsert["tupleId"] = count 
                mappedTransactions.insert_one(rowInsert)
                count += 1
                rowInsert = {}
                

             if transaction['nameDest'] not in customerMap.keys():
                customerMap[transaction['nameDest']] = count
                # Insertion into Mapped Transactions Database
                rowInsert["customerId"] = transaction['nameDest']
                rowInsert["tupleId"] = count
                mappedTransactions.insert_one(rowInsert)
                count += 1
                rowInsert = {}
                

            #print("%d -> %d" % (customerMap[transaction['nameOrig']], customerMap[transaction['nameDest']]))
             trans = (customerMap[transaction['nameOrig']],customerMap[transaction['nameDest']])
             try:
                edgeList.append(trans)
             except Exception as e:
                edgeList = [trans]

        # for keys in customerMap.keys():
        #     #print(keys,customerMap[keys])
        print("Edge List : {}".format(edgeList))
        tuple_list_db.insert_one({"tupleList": edgeList})        
        return edgeList
    except:
        print("Error in Mapping !!")
        print("Please check if MongoDb server is On")


def get_tuple_list():
    return db.tupleList.find({},{"tupleList":1,'_id':0})

class BucketContainer():
    """
    Description : It is a class containing bucket and bucketCount.
                  bucket contains the list of transactions mapped to a bucket.
                  bucketCount contains the count of transactions in each bucket.
    """
    def __init__(self):
        self.bucket = {}
        self.bucketCount = {}


def hashBasedBucketCount(tupleList):
    """
        Description : Hashes the transaction(obtained after mapping)to a bucket
                      based on the hashing formula.
                      Also maintains the count of transactions in each bucket using
                      bucketCount.
        Input  : transactions in tuple list [(1,2),(1,3),(2,3)(2,5)]
        Output :   b
                    {
                     bucket  = { 2:[(1,2)], 3:[(1,3),(2,3)] , 5:[(2,5)] }
                     bucketCount = {2 : 1 , 3 : 2, 5 : 1}
                    }
    """
    b = BucketContainer()
    for trans in tupleList:
        bucketIndex = ((trans[0]*10) + trans[1]) % 10
        try:
            if trans not in b.bucket:
                b.bucket[bucketIndex].append(trans)
        except:
            b.bucket[bucketIndex] = [trans]
    #print(b.bucket)
    for keys in b.bucket.keys():
        print(keys,b.bucket[keys])
        b.bucketCount[keys] = len(b.bucket[keys])
    for keys in b.bucketCount.keys():
        print(keys,b.bucketCount[keys])
    return b

def actualCount(tupleList):
    """
    Description : Frequency of individual Transactions
    input : tupleList containing all the transactions [(1,2),(2,3),(1,2),(3,4)]
    output : actualCount = {(1,2) : 2, (2,3) : 1, (3,4) : 1}
    """
    actualCount = {}
    for tuple in tupleList:
        if tuple not in actualCount.keys():
            actualCount[tuple] = 1
        else:
            actualCount[tuple] += 1
    #for keys in actualCount.keys():
    #    print(keys,actualCount[keys])
    return actualCount

def filterOnActualCount(filteredBucketTuples,actualCount,minSupportCount):
    """
    Description : Filters the transactions from the obtained filtered Buckets
                  based on the minimum support count defined for transactions
    """
    filteredActualCount = {}
    count = 0
    for keys in actualCount.keys():
        if actualCount[keys] > minSupportCount and keys in filteredBucketTuples.keys():
            filteredActualCount[keys] = actualCount[keys]
            count +=1
    print("Number of Transactions based on Actual Frequency : ",count)
    return filteredActualCount

def filterOnBucketCount(tupleList,bucketContainer,minSupportCount):
    """
    Description : Filters the bucket on basis of minimum
                  Support Count defined for buckets
    """
    itemSetCount = {}
    count = 0
    for tuple in tupleList:
        #Used List Comprehension
        key = [k for k, v in bucketContainer.bucket.items() if tuple in v]
        if(bucketContainer.bucketCount[key[0]] > minSupportCount):
            itemSetCount[tuple] = bucketContainer.bucketCount[key[0]]
            count += 1
    #for keys in itemSetCount.keys():
        #print(keys,itemSetCount[keys])
    print("Number of filtered Transactions : ",count)
    return itemSetCount

