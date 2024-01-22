from xml.dom import minidom

from MyException import MyException

class XMLReader:
    '''
    This object takes in input a file XML (the POM file downloaded from Maven repository)
    and looks for a github link into it 
    '''

    def get_github_url(self, xml_file):
        ''''
        This method will retrun a list of GH urls found in the POM file taken in input
        :param xml_file: the POM file to be analysed
        :return: list of GH urls
        '''

        xmldoc = minidom.parse(xml_file)
        url_tags = xmldoc.getElementsByTagName('url')   # sometimes github urls may be insert into other tags
        gh_urls = []
        try:
            for tag in url_tags:
                if "github.com/" in tag.firstChild.nodeValue:
                    gh_urls.append(tag.firstChild.nodeValue)
                    #print(tag.firstChild.nodeValue)
        except BaseException as be:
            msg = "Error while looking for tags in the POM file. Syntax error?"
            raise MyException(msg)
        return gh_urls

    def data_to_xml_file(self, data, file_name="data_to_xml.xml"):
        '''
        Write XML data to a file
        :param data: data to be written into the file
        :return: the file created
        '''
        try:
            file = open(file_name, "w")
            try:
                n = file.write(data)
            except (IOError, OSError):
                msg = "Error writing to file: ", file_name
                raise MyException(msg)
            file.close()
        except (FileNotFoundError, PermissionError, OSError):
            msg = "Error opening/closing file: ", file_name
            raise MyException(msg)
        #print(f"Written XML into {file} with filename {file_name}")
        return file

    def get_versions_of_artefact(self, file):
        '''
        This function gets all versions available of an artefact. RC, alpha and beta relases are ignored
        File: xml file to be read. It contains XML response from maven search repository
        Returns: list of versions

        '''
        
        try:
            xmldoc = minidom.parse(file.name)
            strs = xmldoc.getElementsByTagName('str')
        except BaseException as be:
            msg = f"Something went wrong when creating the XML parser or when seeking the element by tag. Error: {be}. "
            raise MyException(msg)
            
        strs = xmldoc.getElementsByTagName('str')
        versions = []
        for s in strs:
            if s.getAttribute("name") == "v":
                #print("Checking version ", s.firstChild.nodeValue)
                ver = s.firstChild.nodeValue

                # exclude alpha, beta and rc versions
                if ver  not in versions and \
                        ver.find("RC") == -1 and \
                        ver.find("alpha") == -1 and\
                        ver.find("beta") == -1:
                    #print(" ------- Adding version ", s.firstChild.nodeValue)
                    versions.append(s.firstChild.nodeValue)
        return versions

    def delete_xml_file(self, file):

        return 0