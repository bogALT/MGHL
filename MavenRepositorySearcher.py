import math
import requests
import re
from MyException import MyException
from XMLReader import XMLReader

class MavenRepositorySearcher:
    def __init__(self):
        self.gav = None

    def do_request(self, url):
        '''
        This method executes GET method on maven repository search page and returns the response's content
        :param url: url to be requested in GET
        :return: responses content (XML)
        '''
        try:
            #print("Requesting versions at = ", url)
            response = requests.get(url)
            data = response.content.decode("utf-8")
        except BaseException as be:
            msg = f"Something went wrong when searching on maven for url = {url} the following exception was raised: {be}. "\
                  f"This point is mandatory, "
            #self.exceptions.append(msg)
            raise MyException(msg)
        return data

    def search_last_version(self, g, a):
        '''
        This method takes in input a G:A sequence and returns the newest version.
        It reads the paginated result: page per page and merges all results
        :param g: group id
        :param a: artefact id
        :return: newer version
        '''
        '''if g == "" or a == "":
            print("You did not specify all of GAV values")
            return 1

        # create search url
        search_url = "https://search.maven.org/solrsearch/select?q="
        search_parameters = f"g:{g}&a:{a}&core=gav&start=0&wt=jso"

        # do request
        data = self.do_request(search_url+search_parameters)

        # get the number of pages
        pages_number = math.ceil(int(self.get_total_number_of_versions(data))/20)
        print(f"Searching amoung {pages_number} pages. This may take more than {pages_number*2} seconds.")

        # retrieve all versions available reading every page
        versions = []
        counter = 0

        while pages_number >= 0:
            if counter % 30 != 0:
                print('|', end = '')
            else:
                print(f'Missing: {pages_number} pages')

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
        return versions[0]'''
        return 0

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
            raise MyException("You did not specify all of GAV values, one or more are missing. This is the GAV i got {g} : {a} : {v}")
        else: 
            self.gav = f"{g}_{a}_{v}.xml"
        # create search url
        search_url = "https://search.maven.org/solrsearch/select?q="
        search_parameters = f"g:{g}&a:{a}&v:{v}&core=gav&start=0&wt=jso"

        # do request
        try:
            data = self.do_request(search_url+search_parameters)
        except BaseException as be:
            msg = f"Error while querying the maven repository. Exception: {be}. "\
                  f"The error is often caused by the maven server which returns a 503 error due to outage."

            raise MyException(msg)

        # get the number of pages
        try:
            pages_number = math.ceil(int(self.get_total_number_of_versions(data))/20)
            print(f"Searching among {pages_number} pages. This may take more than {pages_number} seconds according to your internet speed and maven central server status.")
        except BaseException as be:
            msg = f"I wasn't able to retrive versions from maven server, the following exception was raised: {be}. "\
                f"This may be caused by a Maven server malfunction (or not). The server returned an error: {data}. \nThis point is mandatory, "
            raise MyException(msg)
        # retrieve all versions available reading every page
        versions = []
        counter = 0

        while pages_number >= 0:
            if counter % 30 != 0:
                print('|', end = '')
            else:
                print(f'Pages left = {pages_number}')
            counter += 1
            versions += self.read_xml(data)

            # create search url
            search_parameters = f"g:{g}&a:{a}&v:{v}&core=gav&start={pages_number*20}&wt=jso"

            # do request
            data = self.do_request(search_url+search_parameters)
            pages_number -= 1

        if len(versions) > 1:   # manually sort versions UPDATE THE SORTING ALG
            versions.sort()
            try:
                v = versions[versions.index(v)-1]
                return v
            except Exception as e:
                msg = f"Version {v} has not been found on MVN. Available versions are : {versions}"
                raise MyException(msg)
        else:
            msg = f"I wasn't able to retrieve versions from MVN repo server!"
            raise MyException(msg)
            return -1
        #print("Versions found = ",len(versions))
        #print("MVN----> ", versions)

    def read_xml(self, data):
        '''
        This function will take a string containing XML, write it on a file
        and then read it to extract information about all the versions of the package
        :param data: string containing XML
        :return: vector containing read versions from XML
        '''

        if self.gav != None:
            xml_file = self.gav
        else:
            xml_file = "versions.xml"
        xr = XMLReader()
        #print("Writting to XML = ", data)
        f = xr.data_to_xml_file(data, "xml_files/"+xml_file)
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