# Name: Renderlib.py
# Purpose: contains vocabulary browser rendering classes

import string, types, regex, regsub, db, Linklib

###--- Constants ---###

NBSP = '&nbsp;'		# non-breaking space
NL = '\n'		# newline
HR = '<HR>'		# HTML horizontal rule
BR = '<BR>'		# HTML line break

###--- Functions ---###

def inBlue (s):
	# Purpose: return the HTML markup needed to display the contents of
	#	's' in blue
	# Returns: string
	# Assumes: nothing
	# Effects: nothing
	# Throws: nothing

	return '<FONT COLOR="blue">%s</FONT>' % s

###--- Classes ---###

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

    def __init__(self, header='', footer='', colspan=8):
        """
        #  Requires:
	#    header: string
	#    footer: string
	#    colspan: integer (number of spaces to indent at each level)
        #  Effects:
        #    constructor
        #  Modifies:
	#    self.colspan
        #  Returns:
        #  Exceptions:
        """

	Renderer.__init__(self, header, footer)
	self.setColspan (colspan)

	# depth in the tree of the most recently printed node
	self.depth = 0
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
	#    colspan: integer (number of spaces to indent at each level)
        #  Effects:
        #    see Modifies
        #  Modifies:
        #    self.colspan, self.indent
        #  Returns:
        #  Exceptions:
        """

        self.colspan = colspan
	self.indent = NBSP * colspan
	return
	
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

        return NBSP * 2

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

        return NBSP + inBlue('+')

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

	return inBlue(label)

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

    def htmlAncestors(self, path):
        """
        #      Private
        #
        #  Requires:
        #    path: list of Node objects
        #  Effects:
        #    Generates a string of all ancestors of a node, indented
        #    by HTML non-breaking spaces
        #  Modifies:
        #  Returns:
        #    doc: string
        #  Exceptions:
        """
        
        doc = []
        firstNode = 1
	targetNode = str(self.node.getId())

        if len(path) > 1:
            for ancestor in path:
                node, etype = ancestor[0], ancestor[1]
                label = node.getLabel()
                id = str(node.getId())
                # handle root node
                if firstNode:
                    doc.append (self.htmlRoot(label))
                    firstNode = 0
                    continue

                # target node will be printed among siblings
                if id != targetNode:
                    self.depth = self.depth + 1
                    link = self.linkBuilder.build(node)

		    doc.append ('%s%s%s' % (
			self.indent * self.depth,
			self.htmlEdgePrefix(etype),
			link.getHTML()
		    	) )

        return string.join(doc, BR)

    def htmlChildren(self):
        """
        #      Private
        #
        #  Requires:
        #    nothing
        #  Effects:
        #    Generates an HTML string for all children of the target node
        #  Modifies:
	#    Increments self.depth
        #  Returns:
        #    doc: string
        #  Exceptions:
        """

        self.depth = self.depth + 1
        doc = []
        for child in self.vocab.getChildrenOf(self.node):
            node, etype = child[0], child[1]
            name = node.getLabel()
            id = str(node.getId())
            kids = self.vocab.getChildrenOf(node)
            link = self.linkBuilder.build(node)

	    plus = ''
	    if len(kids):
	    	plus = self.htmlPlus()
            
	    doc.append('%s%s%s%s' % (
		self.depth * self.indent,
		self.htmlEdgePrefix(etype),
		link.getHTML(),
		plus
	    	) )

        return string.join(doc, BR)

    def htmlSibs(self, sibs):
        """
        #      Private
        #
        #  Requires:
        #    sibs: list of Node objects
        #  Effects:
        #    Generates an HTML string for all siblings of and including the
        #    target node
        #  Modifies:
        #  Returns:
        #    doc: string
        #  Exceptions:
        """

        doc = []
        self.depth = self.depth + 1
	targetNode = self.node.getLabel()

        for sib in sibs:
            node, etype = sib[0], sib[1]
            sibName = node.getLabel()
            id = str(node.getId())
            kids = self.vocab.getChildrenOf(node)
            link = self.linkBuilder.build(node)
            
	    label = link.getHTML()
	    if sibName == self.node.getLabel():
	    	label = self.htmlNode()

	    plus = ''
	    if len(kids) and (sibName != self.node.getLabel()):
	    	plus = self.htmlPlus()
            
	    doc.append ('%s%s%s%s' % (
	    	self.depth * self.indent,
		self.htmlEdgePrefix(etype),
		label,
		plus
		) )
            
            if sibName == targetNode:
		childrenHtml = self.htmlChildren()
		if childrenHtml:
			doc.append (childrenHtml)

		# back out to the sibling indentation level, rather than the
		# children's level
		self.depth = self.depth - 1

        return string.join(doc, BR)

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
	
        doc = []
	for path in self.paths:
            sibs = []
            if len(path) > 1:
                parent = path[-2][0]
                for sib in self.vocab.getChildrenOf(parent):
                    sibs.append(sib)
            else:
                sibs.append(path[0])
                
	    self.depth = 0
            doc.append (self.htmlAncestors(path))
            doc.append (self.htmlSibs(sibs))
	    doc.append (HR)

        return string.join (doc, BR)
    
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
# Copyright (c) 1996, 1999, 2002 by The Jackson Laboratory
# All Rights Reserved
#

