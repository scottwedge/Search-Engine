#Syed Azeem Ahmed Quadri
import os #Used for 

class NodeClass:
    
     def __init__(self, key = "", value = [], height = 1, left = None, right = None):
        
        self.key = key
        self.value = value
        self.height = height
        self.left = left
        self.right = right

#End of NodeClass
        
#AVLTreeMapClass           
class AVLTreeMapClass:

    #searches for "target" and appends every node that it visits   
    def searchPath(self, node, target, searchList = []):

        if not node:

            return searchList

        elif (target == node.key): #the target has been found

            searchList.append(target)
            return searchList

        elif (target > node.key):

            searchList.append(node.key)
            return self.searchPath(node.right, target, searchList)

        elif (target < node.key):
                  
            searchList.append(node.key)
            return self.searchPath(node.left, target, searchList)

    #Ssearches for "taraget" and returns tha value
    def getValue(self, node, target):

        if not node:

            return ""

        elif (target == node.key): #targer has been found

            return node.value

        elif (target > node.key):

            return self.getValue(node.right, target)

        elif (target < node.key):
                  
            return self.getValue(node.left, target)

    #insets keys and values into the tree. The the nodes are placed based in the keys
    def put(self, node, newKey, newValue):
      
        if not node: 
        
            return NodeClass(newKey, [newValue]) 
            
        elif (node.key > newKey):
        
            node.left = self.put(node.left, newKey, newValue) 
            
        elif (node.key < newKey):
        
            node.right = self.put(node.right, newKey, newValue)
            
        elif (node.key == newKey):

            (node.value).append(newValue)
            
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right)) #calculates the height, default value is 1
  
        balance = self.getBalance(node) #calculate the balance
   
        # Case 1 - Left Left 
        if balance > 1 and newKey < node.left.key: 
            return self.rightRotate(node) #does right rotation
  
        # Case 2 - Right Right 
        if balance < -1 and newKey > node.right.key: 
            return self.leftRotate(node) #does left rotation
  
        # Case 3 - Left Right 
        if balance > 1 and newKey > node.left.key: 
            node.left = self.leftRotate(node.left) #does left rotation
            return self.rightRotate(node) 
  
        # Case 4 - Right Left 
        if balance < -1 and newKey < node.right.key: 
            node.right = self.rightRotate(node.right) #does right rotation
            return self.leftRotate(node) 
  
        return node 
     
    def leftRotate(self, node): 
  
        y = node.right 
        T2 = y.left 
  
        # Perform rotation 
        y.left = node
        node.right = T2 
  
        # Update heights 
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right)) 
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right)) 
  
        # Return the new node 
        return y 
  
    def rightRotate(self, node): 
  
        y = node.left 
        T3 = y.right 
  
        # Perform rotation 
        y.right = node 
        node.left = T3 
  
        # Update heights 
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right)) 
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right)) 
  
        # Return the new node 
        return y
     
    #returns the height
    def getHeight(self, node): 
        if not node: 
            return 0
  
        return node.height 

    #calculates the balance, which is given by height of leftNode - height of rightNode
    def getBalance(self, node): 
        if not node: 
            return 0
  
        return (self.getHeight(node.left) - self.getHeight(node.right)) 

#End of AVLTreeMapClass

#WebPageIndexClass     
class WebPageIndexClass:

    #constructor that takes in a file name
    def __init__(self, fileName):
        
        self.fileName = fileName
        self.fileTree = AVLTreeMapClass() #
        self.root = None
        self.priority = 0 #created a priority attribute to sort each each WebPageIndex Obj on priority, default value is 0

    #takes in a file and inserts everything to a AVLTree    
    def insertToTree(self):
        
        file = open(os.getcwd() + '/websites/' + self.fileName, 'r') #gets the file from the "websites" folder
        text = file.read()
        
        for ch in text:
        
            if (not ch.isalnum()) and (ch!=" "): #is the character is not an alphanumeric or is not a space
                text = text.replace(ch, "") #replace that character with "" (

               
        splitText = text.split() #splits the file into list of strings/words
        
        n = len(splitText)        
        for i in range(0,n):
            
            self.root = self.fileTree.put(self.root, splitText[i].lower(), i) #where 'i' is the position of the word
        
        file.close()

    def getCount(self, word): 

        return len(self.fileTree.getValue(self.root, word)) #finds the length of the "value", which the list of positions of the word


#end of WebPageIndexClass

#WebPagePriorityQueue
class WebpagePriorityQueue:

    #contsructor that takes in query and a webPageIndexList    
    def __init__(self, query, webPageList):
        
        self.query = query
        self.maxHeap = webPageList
    
    #calculates the priority of each webPage index obj in maxHeap
    def calculatePriority(self):
        
        for webPage in self.maxHeap:
            webPage.priority = calculate(self.query, webPage) #helper function defined on line

    #finds the webPage with the highest priority and returns it
    def peek(self):
             
        maxValue = self.maxHeap[0]
        
        for webPage in self.maxHeap:
                
            if (webPage.priority >= maxValue.priority):
                maxValue = webPage
        
        return maxValue, maxValue.fileName, maxValue.priority

    #uses the peek function and returns the highest webpage with the highest priority and removes it     
    def poll(self):
        
        maxValue, fileName, maxPriority = self.peek()
        maxIndex = self.maxHeap.index(maxValue)
        self.maxHeap.pop(maxIndex)
    
        return fileName, maxPriority

    #reheaps the maxHeap if a new query is given
    def reheap(self, newQuery):
        
        self.query = newQuery
        for webPage in self.maxHeap:
                
                webPage.priority = 0

#End of WebPagePriorityQueue

#Helper function used to calculate the priority
def calculate(query, webPage):
        
        splitQuery = query.split() #splits the query into list of string/words
        for word in splitQuery:
            
            webPage.priority = webPage.priority + webPage.getCount(word) #calls the getCount function defined in WebPageIndexClass
    
        return webPage.priority

#PrcoessQueries class        
class PrcoessQueries:

    #calls a constructor that makes a empty webPageIndeList
    def __init__(self):
        
        self.webPageIndexList = []

    #Creates the list of webPage index objects
    def getWebPages(self):  
        
       
       fileList = os.listdir(os.getcwd() + '/test data') #the text files are in the test data folder
                           
       for file in fileList:
            
           webPageObj = WebPageIndexClass(file)
           webPageObj.insertToTree()
           self.webPageIndexList.append(webPageObj)

    #gets the search result      
    def getSearchResults(self, newQuery, limit):
            
          self.getWebPages() 
          queueObj = WebpagePriorityQueue(newQuery, self.webPageIndexList)
          queueObj.calculatePriority()
          
          for i in range(0, limit): #calls the poll function as many times as the user wants
              
              print(queueObj.poll())
              
#End of ProcessQueues class

#Helper function which takes in user query and user limit              
def searchEngine(query, limit):
        
    processObj = PrcoessQueries()
    
    processObj.getSearchResults(query, limit)       

#Helper function to add query to the "queries.txt" file    
def addQuery(query):
    
    file = open(os.getcwd() + '/queries.txt', "a")
    file.write(query + "\n")
    file.close()

#start of main    
def main():
   
   print("Welcome to web search engine.") 
   ans = 'y' 
   while (ans == 'y' or ans == 'Y'): #program runs as many times as the user wants as long as ans is 'y' or 'Y'
      
       print("Please enter your query:")
       query = input()
       query = query.lower()
       print("Please enter limit (Default is 10, Press enter to skip)")
       limit = input()
       
       if (not (limit.isalnum())): #if user presses enter to skip typing the limit, the default limit is 10
           limit = 10
           
       limit = int(limit)
       print("Here are your results: \n")
       searchEngine(query, limit)
       addQuery(query)
       print("Enter y/Y to search for a new query or press enter to exit")
       ans = input() #takes in the answer if the user wishes to search for a new query or to exit the program

       
if  __name__== "__main__":
     main()
