# Name: Renderlib.py
# Purpose: contains vocabulary browser rendering classes

import string, types, db, Linklib

class Renderer:
	# Concept:
	#	IS:	an object which prepares (renders) a page of output
	#		for another object
	#	HAS:	a header and a footer
	#	DOES:	see "IS"
	# Implementation:
	#	At this very highest level class, wew only know about the
	#	header and footer.  Subclasses will need to deal with the
	#	details of rendering for particular types of displays and
	#	particular types of objects.

	def __init__ (self,
		header='',	# see setHeader() method for valid types
		footer=''	# see setFooter() method for valid types
		):
		# Purpose: constructor; initializes header and footer of
		#	the object
		# Returns: nothing
		# Assumes: nothing
		# Effects: nothing
		# Throws: nothing

		self.setHeader(header)
		self.setFooter(footer)
		self.colspan = 4        # HTML table colspan value
		return

	def setHeader (self,
		header		# can be a string, a list of strings, or a
				# function which returns either when called
		):
		# Purpose: sets the header info of this object
		# Returns: nothing
		# Assumes: nothing
		# Effects: nothing
		# Throws: nothing

		htype = type(header)
		if htype == types.StringType:
			self.header = header
		elif htype == types.ListType:
			self.header = string.join (header, '\n')
		else:
			self.header = string.join (header(), '\n')
		return

	def setFooter (self,
		footer		# can be a string, a list of strings, or a
				# functions which returns either when called
		):
		# Purpose: sets the footer info of this object
		# Returns: nothing
		# Assumes: nothing
		# Effects: nothing
		# Throws: nothing

		ftype = type(footer)
		if ftype == types.StringType:
			self.footer = footer
		elif ftype == types.ListType:
			self.footer = string.join (footer, '\n')
		else:
			self.footer = string.join (footer(), '\n')
		return

	def printHeader (self):
		# Purpose: prints this object's header to stdout
		# Returns: nothing
		# Assumes: nothing
		# Effects: writes to stdout
		# Throws: nothing

		print self.header
		return

	def printFooter (self):
		# Purpose: prints this object's footer to stdout
		# Returns: nothing
		# Assumes: nothing
		# Effects: writes to stdout
		# Throws: nothing

		print self.footer
		return


class SummaryRenderer (Renderer):
	# Concept:
	#	IS:	an object charged with rendering a summary screen of
	#		results from a query (a subclass of Renderer)
	#	HAS:	?
	#	DOES:	see "IS"
	# Implementation:

	def printSummary (self,
		results,	# set of results from querying vocab
		queryterm	# string; query string entered by the user
		):
		# Purpose: abstract method - print the summary screen for the
		#	given results from searching a vocabulary
		# Returns: nothing
		# Assumes: nothing
		# Effects: writes to stdout
		# Throws: nothing
		# Notes: This is an abstract method.  Subclasses should fill
		#	in the details.

		pass
		return


class DetailRenderer(Renderer):

    def printEdgePrefix(self, etype):

        return ''

    def setColspan(self, colspan):
        """
        #  Requires:
        #    colspan: integer - HTML table colspan value
        #  Effects:
        #    Sets the HTML table colspan value
        #  Modifies:
        #    self.colspan
        #  Returns:
        #  Exceptions:
        """

        self.colspan = colspan
	
    def printSpace(self):

        return '&nbsp;&nbsp;'

    def printPlus(self):

        return '&nbsp;<FONT COLOR=blue>+</FONT>'

    def printRoot(self, label):

        return '<TR><TD COLSPAN=4><FONT COLOR=blue>%s</FONT></TD>\n' % label

    def printNode(self):

        return ''

    def printAncestors(self, path, pad):
        """
        #      Private
        #
        #  Requires:
        #    path: list of Node objects
        #    pad: integer (number of trailing HTML table cells)
        #  Effects:
        #    Generates a string of all ancestors of a node, indented
        #    by HTML non-breaking spaces
        #  Modifies:
        #  Returns:
        #    doc: string
        #  Exceptions:
        """
        
        doc = ''
        firstNode = 1
        if len(path) > 1:
            for ancestor in path:
                node, etype = ancestor[0], ancestor[1]
                label = node.getLabel()
                id = str(node.getId())
                # handle root node
                if firstNode:
                    doc = doc + self.printRoot(label)
                    firstNode = 0
                    continue

                # target node will be printed among siblings
                if id != str(self.node.getId()):
                    depth = path.index(ancestor)
                    link = self.linkBuilder.build(node)

                    doc = doc + '<TR><TD COLSPAN=%d>' % self.colspan \
                          + (depth * self.printSpace()) \
                          + self.printEdgePrefix(etype) + link.getHTML() \
                          + '</TD>' + (pad * '<TD></TD>') + '</TR>\n'

        return doc

    def printChildren(self, pad):
        """
        #      Private
        #
        #  Requires:
        #    pad: integer (number of trailing HTML table cells)
        #  Effects:
        #    Generates an HTML string for all children of the target node
        #  Modifies:
        #  Returns:
        #    doc: string
        #  Exceptions:
        """

        depth = 2
        doc = ''
        for child in self.vocab.getChildrenOf(self.node):
            node, etype = child[0], child[1]
            name = node.getLabel()
            id = str(node.getId())
            kids = self.vocab.getChildrenOf(node)
            link = self.linkBuilder.build(node)
            
            doc = doc + '<TR>' + (depth * '<TD></TD>') \
		  + '<TD COLSPAN=%d>' % self.colspan
            doc = doc + self.printEdgePrefix(etype) + link.getHTML()
            if len(kids):
                doc = doc + self.printPlus()
            doc = doc + '</TD>' + (pad * '<TD></TD>') + '</TR>\n'

        return doc

    def printSibs(self, sibs, pad):
        """
        #      Private
        #
        #  Requires:
        #    sibs: list of Node objects
        #    pad: integer - number of trailing HTML table cells
        #  Effects:
        #    Generates an HTML string for all siblings of and including the
        #    target node
        #  Modifies:
        #  Returns:
        #    doc: string
        #  Exceptions:
        """

        doc = ''
        for sib in sibs:
            node, etype = sib[0], sib[1]
            sibName = node.getLabel()
            id = str(node.getId())
            kids = self.vocab.getChildrenOf(node)
            depth = 1
            link = self.linkBuilder.build(node)
            
            doc = doc + '<TR>' + (depth * '<TD></TD>')
            doc = doc + '<TD COLSPAN=%d>' % self.colspan
            
            doc = doc + self.printEdgePrefix(etype)
            if sibName == self.node.getLabel():
                doc = doc + self.printNode()
            else:
                doc = doc + link.getHTML()
            if (len(kids)) and (sibName != self.node.getLabel()):
                doc = doc + self.printPlus()
            doc = doc + '</TD>' + (pad * '<TD></TD>') + '</TR>\n'
		
            if sibName == self.node.getLabel():
                pad = pad - 1
                doc = doc + self.printChildren(pad)

        return doc

    def printInfo(self):

        pass

    def printTrees(self):
        """
        #      Private
	#
        #  Requires:
        #  Effects:
        #    Constructs an HTML string for tree display
        #  Modifies:
        #  Returns:
        #    doc: string
        #  Exceptions:
        """
	
        doc = ''
	for path in self.paths:
            sibs = []
            if len(path) > 1:
                parent = path[-2][0]
                for sib in self.vocab.getChildrenOf(parent):
                    sibs.append(sib)
            else:
                sibs.append(path[0])
                
            doc = doc + '<TABLE>\n'
                
            pad = len(path)
            doc = doc + self.printAncestors(path, pad)
                
            pad = pad - 1
            doc = doc + self.printSibs(sibs, pad)
                
            doc = doc + '</TABLE>\n<HR>\n'

        return doc
    
    def printDetail(self, vocab, node):

        pass
        return


        




