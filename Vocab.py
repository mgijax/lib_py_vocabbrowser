# Name: Vocab.py
# Purpose: class representing a vocabulary

class Vocab:
    """
    #  Vocabulary object; may consist of more than one graph (sub-vocabulary)
    """
    
    def __init__(self):
        """
        #  Requires:
        #  Effects:
        #    constructor
        #  Modifies:
        #    self.graph: DAG object
        #    self.etypes: list (of edge types)
        #  Returns:
        #  Exceptions:
        """

        self.graph = None
        self.etypes = []

    def findNode(self, id):
        """
        #  Requires:
        #    id: string
        #  Effects:
        #    Abstract method to be overridden by subclasses
        #  Modifies:
        #  Returns:
        #  Exceptions:
        """

        return None

    def getParentsOf(self, node):
        """
        #  Requires:
        #    node: Node object
        #  Effects:
        #    If self.graph exists, returns the node's parents; otherwise
        #    returns an empty list
        #  Modifies:
        #  Returns:
        #    list of tuples containing nodes and edge types
        #  Exceptions:
        """

        if self.graph == None:
            return []
        else:
            return self.graph.getParentsOf(node)

    def getChildrenOf(self, node):
        """
        #  Requires:
        #    node: Node object
        #  Effects:
        #    If self.graph exists, returns the node's children; otherwise
        #    returns an empty list
        #  Modifies:
        #  Returns:
        #    list of tuples containing nodes and edge types
        #  Exceptions:
        """

        if self.graph == None:
            return []
        else:
            return self.graph.getChildrenOf(node)

    def getPathsTo(self, node):
        """
        #  Requires:
        #    node: Node object
        #  Effects:
        #    If self.graph exists, calls its methods to return all paths
        #    to node; otherwise returns an empty list
        #  Modifies:
        #  Returns:
        #    list of lists, each containing tuples of nodes and edge types
        #  Exceptions:
        """

        if self.graph == None:
            return []
        else:
            return self.graph.getPathsTo(node)

    def getEdgeTypes(self):
        """
        #  Requires:
        #  Effects:
        #    Returns a list of edge types defined for the vocabulary
        #  Modifies:
        #  Returns:
        #    self.etypes
        #  Exceptions:
        """

        return self.etypes
