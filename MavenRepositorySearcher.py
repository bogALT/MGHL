import math
import requests
import re
from XMLReader import XMLReader

class MavenRepositorySearcher:

    def do_request(self, url):
        '''
        This method executes GET method on maven repository search page and returns the response's content
        :param url: url to be requested in GET
        :return: responses content (XML)
        '''
        try:
            response = requests.get(url)
            data = response.content.decode("utf-8")
        except BaseException as be:
            print(f"Something went wrong when searching on maven for url = {url} the following exception was raised: {be}. "
                  f"This point is mandatory, exiting!")
            exit(1)
        return data

    def search_last_version(self, g, a):

        '''
        This method takes in input a G:A:V sequence and prompts it precedent version.
        It reads the paginated result: page per page and merges all results
        :param g: group id
        :param a: artefact id
        :param v: version
        :return: version - 1
        '''
        if g == "" or a == "":
            print("You did not specify all of GAV values")
            return 1

        # create search url
        search_url = "https://search.maven.org/solrsearch/select?q="
        search_parameters = f"g:{g}&a:{a}&core=gav&start=0&wt=jso"

        # do request
        data = self.do_request(search_url+search_parameters)

        # get the number of pages
        pages_number = math.ceil(int(self.get_total_number_of_versions(data))/20)
        print(f"GPages to be read = {pages_number}. This may take prox {pages_number} seconds.")

        # retrieve all versions available reading every page
        versions = []
        counter = 0

        while pages_number >= 0:
            if counter % 30 != 0:
                print('|', end = '')
            else:
                print(f' Missing: {pages_number}')

            counter += 1

            versions += self.read_xml(data)

            # create search url
            search_parameters = f"g:{g}&a:{a}&core=gav&start={pages_number*20}&wt=jso"
            #print(f"\nPages left = {pages_number}, url = {search_url+search_parameters}")

            # do request
            data = self.do_request(search_url+search_parameters)
            pages_number -= 1

        print(versions)
        if len(versions) > 1:   # manually sort versions because of the VERSIONING PROBLEM
            versions.sort(reverse=True)

        print("Versions found = ",len(versions))
        print("    ----> ", versions)
        return versions[0]

    def search_GAV(self, g, a, v):
        '''
        This method takes in input a G:A:V sequence and prompts it precedent version.
        It reads the paginated result: page per page and merges all results
        :param g: group id
        :param a: artefact id
        :param v: version
        :return: version - 1
        '''
        if g == "" or a == "" or v == "":
            print("You did not specify all of GAV values")
            return 1

        # create search url
        search_url = "https://search.maven.org/solrsearch/select?q="
        search_parameters = f"g:{g}&a:{a}&v:{v}&core=gav&start=0&wt=jso"

        # do request
        data = self.do_request(search_url+search_parameters)

        # get the number of pages
        pages_number = math.ceil(int(self.get_total_number_of_versions(data))/20)
        print(f"GPages to be read = {pages_number}. This may take prox {pages_number} seconds.")

        # retrieve all versions available reading every page
        versions = []
        counter = 0

        while pages_number >= 0:
            if counter % 30 != 0:
                print('|', end = '')
            else:

                print(f' Missing: {pages_number}')

            counter += 1

            versions += self.read_xml(data)

            # create search url
            search_parameters = f"g:{g}&a:{a}&v:{v}&core=gav&start={pages_number*20}&wt=jso"
            #print(f"\nPages left = {pages_number}, url = {search_url+search_parameters}")

            # do request
            data = self.do_request(search_url+search_parameters)
            pages_number -= 1

        if len(versions) > 1:   # manually sort versions
            versions.sort()

        print("Versions found = ",len(versions))
        print("    ----> ", versions)
        return versions[versions.index(v)-1]

    def read_xml(self, data):
        '''
        This function will take a string containing XML, write it on a file
        and then read it to extract information about all the versions of the package
        :param data: string containing XML
        :return: vector containing read versions from XML
        '''

        xml_file = "test2.xml"
        xr = XMLReader()
        f = xr.data_to_xml_file(data, "test3.xml")
        versions = xr.get_versions_of_artefact(f)
        #print(versions)
        return versions

    def get_total_number_of_versions(self, string):
        '''
        This method will retrieve the total number of version of our search in order to paginate correctly
        :param string: xml string from the requests.get method in search_GAV method
        :return: integer indicating the total number of versions
        '''
        pattern = r'numFound="\d+"'
        match = re.search(pattern, string)      # extract the tag attribute containing numFound
        if match:
            match = match.group(0)
            number = re.search(r'\d+', match)   # extract the number
            return number.group(0)              # return the number
        else:
            return None