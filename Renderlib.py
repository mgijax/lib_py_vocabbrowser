# Name: Renderlib.py
# Purpose: contains vocabulary browser rendering classes

import string, types, regex, regsub, Linklib

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

	def highlight (self, label, to_highlight):

		# Requires: label, string
		#           to_highlight, substring to highlight
		# Purpose: highilights given substring with HTML bold tags,
		#          ignores text within angle brackets
		# Returns: s, string with <B> tags inserted
		# Assumes: nothing
		# Effects: nothing
		# Throws: nothing

		tag = regex.compile ('\([^<]*\)\(<[^>]+>\)')

		s = ''
		highlighted = '<B>%s</B>' % to_highlight
		start = tag.search (label)
		end = 0
		while start != -1:
			s = s + regsub.gsub (to_highlight, highlighted,
					     tag.group(1)) + tag.group(2)
			end = tag.regs[0][1]
			start = tag.search (label, end)
		if end < len(label):
			s = s + regsub.gsub (to_highlight, highlighted, \
					     label[end:])
		return s

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
    """
    #  Object representing the vocabulary term detail display
    """

    def __init__(self, header='', footer='', colspan=4):
        """
        #  Requires:
	#    header: string
	#    footer: string
	#    colspan: integer (HTML table colspan)
        #  Effects:
        #    constructor
        #  Modifies:
	#    self.colspan
        #  Returns:
        #  Exceptions:
        """

	Renderer.__init__(self, header, footer)
	self.colspan = colspan
	return

    def htmlEdgePrefix(self, etype):
        """
        #  Requires:
        #    etype: string (denoting edge type)
        #  Effects:
        #    Abstract method for returning HTML edge prefix
        #  Modifies:
        #  Returns:
	#    string of HTML
        #  Exceptions:
        """

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
	
    def htmlSpace(self):
        """
        #  Requires:
        #  Effects:
        #    Returns HTML for two non-breaking spaces
        #  Modifies:
        #  Returns:
	#    string of HTML
        #  Exceptions:
        """

        return '&nbsp;&nbsp;'

    def htmlPlus(self):
        """
        #  Requires:
        #  Effects:
        #    Returns HTML for a non-breaking space and a blue '+'
        #  Modifies:
        #  Returns:
	#    string of HTML
        #  Exceptions:
        """

        return '&nbsp;<FONT COLOR=blue>+</FONT>'

    def htmlRoot(self, label):
        """
        #  Requires:
	#    label: string
        #  Effects:
        #    Returns HTML for displaying the root node
        #  Modifies:
        #  Returns:
	#    string of HTML
        #  Exceptions:
        """

        return '<TR><TD COLSPAN=%d><FONT COLOR=blue>%s</FONT></TD>\n' \
	       % (self.colspan, label)

    def htmlNode(self):
        """
        #  Requires:
        #  Effects:
        #    Abstract method that returns HTML for displaying the
	#    selected node
        #  Modifies:
        #  Returns:
	#    string of HTML
        #  Exceptions:
        """

        return ''

    def htmlAncestors(self, path, pad):
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
                    doc = doc + self.htmlRoot(label)
                    firstNode = 0
                    continue

	        # adjust spacing at greater depths
		if (len(path) > 6) and (len(path) < 9):
			self.setColspan(3)
		elif (len(path) > 8) and (len(path) < 11):
			self.setColspan(2)
		elif len(path) > 10:
			self.setColspan(1)

                # target node will be printed among siblings
                if id != str(self.node.getId()):
                    depth = path.index(ancestor)
                    link = self.linkBuilder.build(node)

                    doc = doc + '<TR><TD COLSPAN=%d>' % self.colspan \
                          + (depth * self.htmlSpace()) \
                          + self.htmlEdgePrefix(etype) + link.getHTML() \
                          + '</TD>' + (pad * '<TD></TD>') + '</TR>\n'

        return doc

    def htmlChildren(self, pad):
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
            doc = doc + self.htmlEdgePrefix(etype) + link.getHTML()
            if len(kids):
                doc = doc + self.htmlPlus()
            doc = doc + '</TD>' + (pad * '<TD></TD>') + '</TR>\n'

        return doc

    def htmlSibs(self, sibs, pad):
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
            
            doc = doc + self.htmlEdgePrefix(etype)
            if sibName == self.node.getLabel():
                doc = doc + self.htmlNode()
            else:
                doc = doc + link.getHTML()
            if (len(kids)) and (sibName != self.node.getLabel()):
                doc = doc + self.htmlPlus()
            doc = doc + '</TD>' + (pad * '<TD></TD>') + '</TR>\n'
		
            if sibName == self.node.getLabel():
                pad = pad - 1
                doc = doc + self.htmlChildren(pad)

        return doc

    def htmlInfo(self):
        """
        #  Requires:
        #  Effects:
        #    Abstract method that returns HTML for displaying attributes
	#    of the selected node
        #  Modifies:
        #  Returns:
	#    string of HTML
        #  Exceptions:
        """

        return ''

    def htmlTrees(self):
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
            doc = doc + self.htmlAncestors(path, pad)
                
            pad = pad - 1
            doc = doc + self.htmlSibs(sibs, pad)
                
            doc = doc + '</TABLE>\n<HR>\n'

        return doc
    
    def printDetail(self, vocab, node):
        """
        #  Requires:
	#    vocab: Vocab object
	#    node: Node object
        #  Effects:
        #    Abstract method for printing the term detail display
        #  Modifies:
        #  Returns:
        #  Exceptions:
        """

        print ''
        return

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
