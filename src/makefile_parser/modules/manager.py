'''
Created on Jul 28, 2016

@author: iitow
'''
import os
import sys
import re

class Manager(object):
    ''' This class manages
    '''
    def __init__(self,options):
        ''' Manager Constructor
        :param path: String
        :param output: String
        '''
        self.options = options
        self.options.path
        self.mk_objs = []
        self.main()
    
    def _walk(self,path,includes=[]):
        ''' performs scan on all files
        :param path: String
        :param excludes: List, list of excludes
        '''
        paths = []
        for root, directories, filenames in os.walk(path):
            for filename in filenames:
                root = root.replace(path,'')
                filepath =  "%s/%s" % (root, filename)
                if includes:
                    if self._is_include(filepath):
                        paths.append(filepath)
                    else:
                        pass
                else:
                    paths.append(filepath)
        return paths
    
    def _is_include(self,filepath):
        '''
        Check for includes in given file name
        '''
        for include in self.options.include:
            if include in filepath:
                return True
        return False
    
    def main(self):
        makefiles = self._walk(self.options.path, self.options.include)
        for makefile in makefiles:
            mk_obj = Makefile(self.options.path,makefile,self.options)
            self.mk_objs.append(mk_obj)

class Makefile(object):
    def __init__(self,base_path,file_ext,options):
        self.options = options
        self.base_path = base_path
        self.file_ext = file_ext
        self.filepath = "%s/%s" % (self.base_path,self.file_ext)
        self.raw = self._reader(self.filepath)
        self.syn_objs = []
        self._parse()
        if self.options.debug:
            print "\n [loaded] %s" % (self.file_ext)

    def _reader(self,filepath):
        with open(self.filepath) as fp:
            return fp.read()

    def _parse(self):
        syntax = Syntax(self.raw)
        #syntax.includes_are(self.raw)
        #syntax.comments_are(self.raw)
        syntax.variables_are(self.raw)   

class Syntax(object):
    def __init__(self,raw):
        self.raw =raw

    def includes_are(self,line):
        matches = re.findall(r'(?<=\.include) [^\n]*', line)
        print "[includes] " ,matches
        return matches

    def comments_are(self,line):
        matches = re.findall(r'\s*#(.*)\s*#(.*)|#(.*)[^#]*',line,re.MULTILINE)
        print "[comments] " ,matches
        return False
    
    def _variables_are(self,line):
        regex = r'([^\s=]+=)(.*)|([^\s=]+=)?(.*\\\n)|((?<=\\\n).*)'
        matches = re.findall(regex,line,re.MULTILINE)
        for match in matches:
            print match
            yield match
    
    def variables_are(self,matches):
        variables = {}
        matches = self._variables_are(self.raw)
        previous = None
        while True:
            try:
                new = matches.next()
            except:
                break
            if not new[0]=='' and '#' not in new[0]:
                previous = str(new[0]).strip()
                if variables.has_key(previous):
                    val1 = new[1].replace('\\','').strip()
                    variables[previous].append(val1)
                else:
                    val1 = new[1].replace('\\','').strip()
                    variables[previous]=[val1]
            else:
                if not new[3] == '' and ':' not in new[3]:
                    val3 = new[3].replace('\\','').strip()
                    variables[previous].append(val3)
                if not new[4] == '':
                    val4 = new[4].replace('\\','').strip()
                    variables[previous].append(val4)      
        for key,value in variables.iteritems():
            print "*** %s:" % (key)
            for v in value:
                print"    - %s"% v
                         
            
            
                        
        
        

    def commands_are(self,line):
        regexp = re.compile(r'([^=]+)=([^=]+)(?:,|$)')
        if not ".if" in line:
            if regexp.search(line):
                print "[variable] %s" % (line)
                return True
        return False
