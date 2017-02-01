from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import time


"""Class to scrap gov websites.  epa.gov will be the pilot site."""

#constants
STARTING_URL = "www.epa.gov"


class Node:

    def __init__(self,root_url, distance=0, prev_node=None):
        self.distance = distance #distance from root node
        self.root_url = root_url
        self.prev_nodes = prev_node #[[nodeClass, distance],[nodeClass2,distance],etc]
        self.branch = {}

    def buildTree(self):
        link = urlopen(self.root_url)
        soup = BeautifulSoup(link)
        for x in soup.findAll('a'):
            content = str(x.contents)
            url = str(x['href'])
            if url.startswith(''):
                if url.endswith(('.png','.svg')):
                    #ignore images for now
                    pass
                elif self.fillWeb(content) == True:
                    #If this function returns true, then the url already has an instance
                    print('web filled')
                    pass
                else:
                    #if self.fillWeb() returns false, then this will create an instance of that link
                    self.branch[content] = Node(url,distance = self.distance + 1,
                                                    prev_node=[[self,self.distance]])
        for x in self.branch:
            self.branch[x].buildTree()

    def fillWeb(self, content, **kwargs):
        if 'retreat' in kwargs:
            curr_node = kwargs['retreat']
        else:
            curr_node = self
            if content in curr_node.branch.keys():
                return True
        node = self
        if curr_node.prev_nodes != None:
            self.fillWeb(content, node=node,retreat=curr_node.prev_nodes[0][0])
        else:
            return self.scourTree(content,node,curr_node)

    def scourTree(self,content,node,curr_node):
        for x in curr_node.branch:
            if content == x:
                curr_node.branch[content].prev_nodes.append([node,node.distance])
                return True
            if len(curr_node.branch[x].branch) > 0:
                self.scourTree(content,node,curr_node.branch[x])
            else:
                return False

        return False

    def traverseTree(self):
        pass






if __name__ == "__main__":
    time1 = time()
    node = Node(STARTING_URL)
    tree = node.buildTree()
    time2 = time()
    finaltime = time2 - time1
    print(finaltime)