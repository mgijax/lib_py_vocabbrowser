# Name: Linklib.py
# Purpose: contains classes for generating HTML links

import string

class Link:
    """
    #  Object representing an HTML link
    """

    def __init__(self, label, action, args):
        """
        #  Requires:
        #    label: string - text string displayed
        #    action: string - name of CGI script
        #    args: dictionary - parameters for CGI
        #  Effects:
        #    constructor
        #  Modifies:
        #    self.prog, self.args
        #  Returns:
        #  Exceptions:
        """

        self.label = label
        self.action = action
        self.args = args
        
        args_vals = []              # list of argument/value strings

        for arg in self.args.keys():
            val = args[arg]
            val = string.join(string.split(val, ' '), '+')
            arg_val = '%s=%s' % (arg, val)
            args_vals.append(arg_val)

        arg_string = string.join(args_vals, '&')
        if arg_string != '':
            arg_string = '?' + arg_string
        self.url = self.action + arg_string

    def getURL(self):
        """
        #  Requires:
        #  Effects:
        #    Returns the link's URL
        #  Modifies:
        #  Returns:
        #    self.url: string
        #  Exceptions:
        """
        
        return self.url
        
    def getLabel(self):
        """
        #  Requires:
        #  Effects:
        #    Returns the link's displayed text
        #  Modifies:
        #  Returns:
        #    self.label: string
        #  Exceptions:
        """

        return self.label

    def getHTML(self):
        """
        #  Requires:
        #  Effects:
        #    Returns the HTML for a link
        #  Modifies:
        #  Returns:
        #    html: string
        #  Exceptions:
        """

        html = '<A HREF="%s">%s</A>' % (self.url, self.label)
        return html

class LinkBuilder:
    """
    #  Factory class for instantiating Link objects
    """

    def __init__(self, baseURL):
        """
        #  Requires:
        #  Effects:
        #    constructor
        #  Modifies:
        #    self.baseURL: string (URL to CGI)
        #  Returns:
        #  Exceptions:
        """

        self.baseURL = baseURL
        
    def build(self, node):
        """
        #  Requires:
        #    node: Node object
        #  Effects:
        #    Abstract method to build a Link object - override in subclasses
        #  Modifies:
        #  Returns:
        #  Exceptions:
        """

        return None

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
