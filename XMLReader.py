from xml.dom import minidom

class XMLReader:

    def get_github_url(self, xml_file):
        xmldoc = minidom.parse(xml_file)
        url_tags = xmldoc.getElementsByTagName('url')
        gh_urls = []
        for tag in url_tags:
            if "github.com/" in tag.firstChild.nodeValue:
                gh_urls.append(tag.firstChild.nodeValue)
                #print(tag.firstChild.nodeValue)
        return gh_urls

    def data_to_xml_file(self, data, file_name="data_to_xml.xml"):
        try:
            file = open(file_name, "w")
            try:
                n = file.write(data)
            except (IOError, OSError):
                print("Error writing to file")
                exit(1)
            file.close()
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening/closing file")
            exit(1)
        #print(f"Written XML into {file} with filename {file_name}")
        return file

    def get_versions_of_artefact(self, file):
        '''
        This function gets all versions available of an artefact. RC, alpha and beta relases are ignored
        File: xml file to be read. It contains XML response from maven search repository
        Returns: list of versions

        '''
        #print("Reading XML = ", file.name)
        xmldoc = minidom.parse(file.name)
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
        #print("\n")
        return versions

    def delete_xml_file(self, file):

        return 0