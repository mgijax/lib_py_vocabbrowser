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

#
# Warranty Disclaimer and Copyright Notice
# 
#  THE JACKSON LABORATORY MAKES NO REPRESENTATION ABOUT THE SUITABILITY OR 
#  ACCURACY OF THIS SOFTWARE OR DATA FOR ANY PURPOSE, AND MAKES NO WARRANTIES, 
#  EITHER EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY AND FITNESS FOR A 
#  PARTICULAR PURPOSE OR THAT THE USE OF THIS SOFTWARE OR DATA WILL NOT 
#  INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS, OR OTHER RIGHTS.  
#  THE SOFTWARE AND DATA ARE PROVIDED "AS IS".
# 
#  This software and data are provided to enhance knowledge and encourage 
#  progress in the scientific community and are to be used only for research 
#  and educational purposes.  Any reproduction or use for commercial purpose 
#  is prohibited without the prior express written permission of the Jackson 
#  Laboratory.
# 
# Copyright © 1996, 1999, 2002 by The Jackson Laboratory
# All Rights Reserved
#
