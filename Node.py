# Name: Node.py
# Purpose: contains a Node class, independent of graph representation

class Node:
    """
    #  Node object, independent of graph membership
    """
    
    def __init__(self, id, label):
        """
        #  Requires:
        #    id: string
        #    label: string
        #  Effects:
        #    constructor
        #  Modifies:
        #    self.id, self.label
        #  Returns:
        #  Exceptions:
        """
        
       	self.id = id
       	self.label = label

    def getId(self):
        """
        #  Requires:
        #  Effects:
        #    Returns node's id
        #  Modifies:
        #  Returns:
        #    self.id
        #  Exceptions:
        """
        
       	return self.id

    def getLabel(self):
        """
        #  Requires:
        #  Effects:
        #    Returns node's label
        #  Modifies:
        #  Returns:
        #    self.label
        #  Exceptions:
        """

        return self.label

    def addSynonyms(self, syns):
        """
        #  Requires:
        #    syns: list of strings
        #  Effects:
        #    Adds a list of synonyms to the node
        #  Modifies:
        #    self.synonyms: list
        #  Returns:
        #  Exceptions:
        """

        self.synonyms = syns

    def getSynonyms(self):
        """
        #  Requires:
        #  Effects:
        #    Returns node's synonyms
        #  Modifies:
        #  Returns:
        #    self.synonyms
        #  Exceptions:
        """

        return self.synonyms
