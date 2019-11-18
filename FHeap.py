from MazeTools import State

class FHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0
        
    def __str__(self):
        s = ""
        
        for state in self.heapList:
            if state == 0:
                continue
            
            s += state.__str__()
        
        return s 

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i // 2]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
                
            i = i // 2

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[mc] < self.heapList[i]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            
            i = mc

    def minChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i * 2] < self.heapList[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def deleteState(self, state):
        if state in self.heapList:
            self.heapList.remove(state)
            self.currentSize -= 1
            
            if not self.isEmpty():
                tmp = self.heapList
                tmp.pop(0)
                
                self.heapList = None
                self.currentSize = 0
                self.buildHeap(tmp)
    
    def delMin(self):
        try:
            retval = self.heapList[1]
        except:
            return None
            
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        
        return retval
    
    def getMin(self):
        return self.heapList[1]
    
    def buildHeap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        
        while (i > 0):
            self.percDown(i)
            i = i - 1

    def isEmpty(self):
        return len(self.heapList) == 1
    

def main():    
    bh = FHeap()
    
    bh.insert(State((0,2), f = 3))
    bh.insert(State((0,0), f = 1))
    bh.insert(State((0,1), f = 2))
    print(bh.isEmpty())
    print(bh.getMin())
    print(bh.delMin())
    print(bh.delMin())
    print(bh.isEmpty())
    print(bh.delMin())
    print(bh.isEmpty())
    print(bh.delMin())
    print(bh.delMin())

if __name__=="__main__":
    main()