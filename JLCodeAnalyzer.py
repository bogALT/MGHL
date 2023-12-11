import time
import javalang
import timeit   #for testing
import os

from MyException import MyException

class JLCodeAnalyzer:
    '''
    This class offers methods able to analyze recursively the java code contained in a directory
    and prompt the number of methods and avg locs per method using javalang parser
    '''
    def __init__(self, directory):
        self.code_path = directory + "/"
        self.maxLOCsLenMethod = 0           # longest method found in terms of number of LOCs
        self.codelines = 0
    
    def get_max_locs_len(self):
        '''
        This method returns the value of self.maxLOCsLenMethod = 0 
        '''
        print("Returning MAX LEN = ", self.maxLOCsLenMethod)

        return self.maxLOCsLenMethod

    def get_method_start_end(self, method_node, tree):
        '''
        This method will analyze and calculate the length of a method and provide where it starts and ends
        :param method_node: javalang node containing information about the node under exam (ie: class, method, etc.)
        :param tree: javalang parsing structure containing all nodes (classes, methods, declarations, ecc)
        :return: starting position, starting line, ending position and ending line
        '''
        startpos  = None
        endpos    = None
        startline = None
        endline   = None
        i = 0
        for path, node in tree:
            #print("Analyzing path: ", path)
            if startpos is not None and method_node not in path:
                endpos = node.position
                endline = node.position.line if node.position is not None else None
                #print(f"{method_node.name} not in node")
                break
            if startpos is None and node == method_node:
                startpos = node.position
                startline = node.position.line if node.position is not None else None

        #print(f"{method_node.name} -> start = {startline}, end = {endline}")
        return startpos, endpos, startline, endline

    def get_method_text(self, startpos, endpos, startline, endline, last_endline_index, codelines, tree):
        '''
        This method will output the source code belonging to each method
        :param startpos: beginning of the method
        :param endpos: ending of a method
        :param startline: line number where the method starts
        :param endline: line number where the method ends
        :param last_endline_index:
        :param codelines: locs belonging to the method
        :param tree: javalang parsing structure containing all nodes (classes, methods, declarations, ecc)
        :return:
        '''
        if startpos is None:
            return "", None, None, None
        else:
            startline_index = startline - 1
            endline_index = endline - 1 if endpos is not None else None

            # 1. check for and fetch annotations
            if last_endline_index is not None:
                for line in codelines[(last_endline_index + 1):(startline_index)]:
                    if "@" in line:
                        startline_index = startline_index - 1
            meth_text = "<ST>".join(codelines[startline_index:endline_index])
            meth_text = meth_text[:meth_text.rfind("}") + 1]

            # 2. remove trailing rbrace for last methods & any external content/comments
            # if endpos is None and
            if not abs(meth_text.count("}") - meth_text.count("{")) == 0:
                # imbalanced braces
                brace_diff = abs(meth_text.count("}") - meth_text.count("{"))

                for _ in range(brace_diff):
                    meth_text  = meth_text[:meth_text.rfind("}")]
                    meth_text  = meth_text[:meth_text.rfind("}") + 1]

            meth_lines = meth_text.split("<ST>")
            meth_text  = "".join(meth_lines)
            last_endline_index = startline_index + (len(meth_lines) - 1)

            return meth_text, (startline_index + 1), (last_endline_index + 1), last_endline_index

    def get_java_files(self, directory):
        '''
        Search recursively all java files in a specified directory and returns a list
        containing all java files found
        :param directory: path to the root directory of java files
        :return: list of java files found
        '''
        java_files = []
        #print("Retrieving .java files from ", directory)
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".java") and file != "module-info.java":
                    java_files.append(os.path.join(root, file))
        return java_files

    def start(self, file_size_limit):
        '''
        This is the main method that must be run. Very large java files may cause a long execution time.
        :param file_size_limit: limit in MB above which the java file examined will be skipped , default = 1Mb
        :return: it prompts the number of methods and locs calculated in all files contained in the code path
        '''

        java_files = self.get_java_files(self.code_path)
        methods = {}
        avg_locs = 0
        exceptions_count = 0
        analized_files_count = 0

        # open each java file and compute its method length (skip files with size bigger than "slimit" -> file_size_limit)
        for target_file in java_files:
            with open(target_file, 'r') as r:
                #start = timeit.default_timer()
                codelines = r.readlines()
                code_text = ''.join(codelines)
                lex = None
                file_size = os.stat(target_file)
                file_size = round(file_size.st_size/(1024*1024),3)
                if file_size > float(file_size_limit):
                    print(f"     Current file =  {target_file} may take a lot time. ({file_size} MB) -> Skipping File!")
                    continue

                try:
                    tree = javalang.parse.parse(code_text)
                    
                except Exception as e:
                    msg = f"\Error when parsing {(target_file)}: Exception Type = {type(e)}, Containg = {e}. This error is caused when reading a java interface file (Empirically tested)."
                    exceptions_count += 1

                avg_locs = 0
                try:
                    for _, method_node in tree.filter(javalang.tree.MethodDeclaration): # sometimes this may generate a parsing  error
                        startpos, endpos, startline, endline = self.get_method_start_end(method_node, tree)

                        # workaround for methods containing only a return statement
                        if endline is None:
                            empty_method = True
                        else:
                            empty_method = False
                        method_text, startline, endline, lex = self.get_method_text(startpos, endpos, startline, endline, lex, codelines, tree)

                        if empty_method:
                            self.codelines += 2
                            methods[method_node.name] = 2
                        else:
                            methods[method_node.name] = endline - startline
                            self.codelines += endline-startline

                            # check id this method is longer than the current longest method and eventually save it as new longest method
                            if(self.maxLOCsLenMethod < (endline-startline)):
                                self.maxLOCsLenMethod = endline-startline
                                
                except BaseException as be:
                    msg = "Exception while reading methods = ", be
                    #self.exceptions.append(msg)
                    raise MyException(msg)

                #stop = timeit.default_timer()
                #p_time = round((stop - start), 3)
            analized_files_count += 1

        # we accept a maximum of <10% erorr rate
        if exceptions_count > 0 and len(java_files) / exceptions_count < 10:
            msg = f"Too many exceptions: {exceptions_count} amoung {len(java_files)} java files!"
            raise MyException(msg)

        print(f"\nAnalyzed files = {analized_files_count}, Exceptions = {exceptions_count}")
        try:
            avg_locs = self.codelines/len(methods.items())
        except ZeroDivisionError as e:
            msg = f"\Error when calculating AVG methond LOCs: Exception = {e}. Probably the package downloaded has no java files."
            raise MyException(msg)
            
        return round(avg_locs, 2)