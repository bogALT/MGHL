import javalang
import os

class JLCodeAnalyzer:
    '''
    This class offers methods able to analyze recursively the java code contained in a directory
    and prompt the number of methods and avg locs per method using javalang parser
    '''
    def __init__(self, directory):
        self.code_path = directory + "/"
        self.codelines = 0           # not sure why I need this
        self.exceptions_count = 0       # may be removed !!! but be aware
        self.analized_files_count = 0   # may be removed !!! but be aware

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
        print("Retrieving .java files from ", directory)
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".java") and file != "module-info.java":
                    java_files.append(os.path.join(root, file))
        return java_files

    def start(self):
        '''
        This is the main method that must be run
        :return: it prompts the number of methods and locs calculated in all files contained in the code path
        '''

        java_files = self.get_java_files(self.code_path)
        print("Collecting Java files from directory = ", self.code_path)
        methods = {}
        counter = 0
        for target_file in java_files:
            counter += 1
            if counter % 30 != 0:
                print('|', end='')
            else:
                print("\n")
            with open(target_file, 'r') as r:
                codelines = r.readlines()
                code_text = ''.join(codelines)
                lex = None
                #print(" "*5 + "Current file = ", (target_file))
                try:
                    tree = javalang.parse.parse(code_text)
                    self.analized_files_count += 1
                except Exception as e:
                    print(f"\nERROR when parsing {(target_file)}: Exception Type = {type(e)}, Containg = {e}\n"
                          f"This error is caused when reading a java interface file (Empirically tested)."
                          f"This is not a fatal error: Going On!")
                    self.exceptions_count += 1

                avg_locs = 0
                try:
                    print(f"\nCunting methods in {target_file}:")
                    for _, method_node in tree.filter(javalang.tree.MethodDeclaration): # sometimes this may generate a parsing  error
                        startpos, endpos, startline, endline = self.get_method_start_end(method_node, tree)

                        # workaround for methods containing only a return statement
                        if endline is None:
                            empty_method = True
                        else:
                            empty_method = False
                        method_text, startline, endline, lex = self.get_method_text(startpos, endpos, startline, endline, lex, codelines, tree)

                        if empty_method:
                            #print(f"{method_node.name} has 2 locs")
                            self.codelines += 2
                            methods[method_node.name] = 2
                        else:
                            #print(f"{method_node.name} has {endline - startline} locs")
                            methods[method_node.name] = endline - startline
                            self.codelines += endline-startline
                        print('|', end='')
                except BaseException as be:
                    print("Exception while reading methods = ", be)
        print(f"Analyzed files = {self.analized_files_count}, Exceptions = {self.exceptions_count}")
        avg_locs = self.codelines/len(methods.items())
        print(f"Number of methods = {len(methods.items())}, Total LOCS = {self.codelines}")
        return avg_locs