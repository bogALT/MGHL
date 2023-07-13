from xml.dom import minidom

from MyException import MyException

class XMLReader:

    def get_github_url(self, xml_file):
        xmldoc = minidom.parse(xml_file)
        url_tags = xmldoc.getElementsByTagName('url')
        gh_urls = []
        try:
            for tag in url_tags:
                if "github.com/" in tag.firstChild.nodeValue:
                    gh_urls.append(tag.firstChild.nodeValue)
                    #print(tag.firstChild.nodeValue)
        except BaseException as be:
            msg = "Error while looking for tags in the POM file. Not every pom file is correctly compiled"
            raise MyException(msg)
        return gh_urls

    def data_to_xml_file(self, data, file_name="data_to_xml.xml"):
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
        #print("Reading XML = ", file.name)
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