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

    def __init__(self):
        """
        #  Requires:
        #  Effects:
        #    constructor
        #  Modifies:
        #    self.baseURL: string
        #    self.args: dictionary (parameters for a CGI script)
        #  Returns:
        #  Exceptions:
        """

        self.baseURL = ''
        self.args = {}
        
    def build(self, node):
        """
        #  Requires:
        #    node: Node object
        #  Effects:
        #    Abstract method to build a Link object - defined in subclasses
        #  Modifies:
        #  Returns:
        #  Exceptions:
        """

        pass
        return
    
    
    
