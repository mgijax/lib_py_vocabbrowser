# Name: Vocab.py
# Purpose: class representing a vocabulary

class Vocab:
    """
    #  Vocabulary object; may consist of more than one graph (sub-vocabulary)
    """
    
    def __init__(self):

        self.graph = None
        self.etypes = []

    def findNode(self, id):

        pass

    def getParentsOf(self, node):

        return self.graph.getParentsOf(node)

    def getChildrenOf(self, node):

        return self.graph.getChildrenOf(node)

    def getPathsTo(self, node):

        return self.graph.getPathsTo(node)

    def getEdgeTypes(self):

        return self.etypes
