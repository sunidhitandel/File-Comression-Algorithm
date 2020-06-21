
#   huffman compression algorithm                                              #


import re
import heapq

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return "(char: "+self.char+" freq: "+str(self.freq)+")"

class Huffman:

    def encode(self, root, str, hcode):
        if root == None:
            return
        if root.left == None and root.right == None:
            hcode[root.char] = str
        self.encode(root.left, str + '0', hcode)
        self.encode(root.right, str + '1', hcode)

    def decode(self, root, index, e_str):
        if root == None:
            return index
        if root.left == None and root.right == None:
            #print(root.char, end="")
            self.d_str += root.char
            return index
        index+=1
        if index > len(e_str)-1 or index < 0:
            #print("Error: "+str(index) +" index out of range")
            return "error"
        if e_str[index] == '0':
            index = self.decode(root.left, index, e_str)
        else:
            index = self.decode(root.right, index, e_str)
        return index

    def compress(self, txt):
        freq = {}
        for char in txt:
            if not char in freq:
                freq[char] = 0
            freq[char] += 1
            
        pq = []
        h_str = ""
        for key,value in freq.items():
            h_str += key+str(value)
            heapq.heappush(pq, Node(key,value))

        while len(pq) != 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            heapq.heappush(pq, Node('\0', left.freq+right.freq, left, right))

        root = pq[0]
        hcode = {}
        self.encode(root, "", hcode)
        
        # huffman codes:
        #for key,value in hcode.items():
            #h_str += key+value
            #print(key+" "+value)
        #print(h_str)
        
        e_str = ""
        for i in range(len(txt)):
            e_str += hcode[txt[i]]
        return h_str,e_str          
    
    def decompress(self, txt):
        header,_,txt = txt.partition("  ")
        header = re.split('(\d+)',header)[:-1]
        pq = []
        for i in range(0, len(header), 2):
            key = header[i]
            value = int(header[i+1]) 
            heapq.heappush(pq, Node(key,value))

        while len(pq) != 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            heapq.heappush(pq, Node('\0', left.freq+right.freq, left, right))

        root = pq[0]
        index = -1
        self.d_str = ""
        while index < len(txt)-2:
            index = self.decode(root, index, txt)
            if index == "error":
                break        
        return self.d_str
