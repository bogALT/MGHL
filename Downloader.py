import requests
class Downlaoder:
    def __init__(self):
        self.base = "https://repo1.maven.org/maven2/"   # base url

# -----------------------------------------------------------------------------
    def download(self, g, a, v, extension="jar"):
        '''
        This method will manage the different parts of the downloading process
        :param g: groupID
        :param a: artefactID
        :param v: artefact version
        :param ext: set pom if you want to create a link for the pom file,
                    set jar if you want to create a link for the jar file
        :return:
        '''

        self.g = g
        self.a = a
        self.v = v

        url = self.gav_to_url(g, a, v, extension)   # create the url from the GAV format
        url = url.replace(".jar", "-sources.jar")   # specify to download the source files
        #print("jar url = ", url)
        if self.is_downloadable(url):
            return self.perform_download(url)       #return the downloaded file
        else:
            print(f"The url = {url} is not a downloadable URL")
            exit(1)
        return 0

# -----------------------------------------------------------------------------
    def gav_to_url(self, g, a, v, ext):
        '''
        This method creates the JAR or POM file link from G:A:V coordinates
        :param g: groupID
        :param a: artefactID
        :param v: artefact version
        :param ext: set pom if you want to create a link for the pom file,
                    set jar if you want to create a link for the jar file
        :return: url pointing to the desired file: jar or pom
        '''

        gid = g.replace(".", "/")
        ret_url = self.base + gid + "/" + a + "/" + v + "/" + a + "-" + v + "." + ext
        #print(f"g = {g}, \na= {a}, \nv = {v}, \ngid = {gid}, \nurl = {ret_url}")
        return self.base + gid + "/" + a + "/" + v + "/" + a + "-" + v + "." + ext

# -----------------------------------------------------------------------------
    def perform_download(self, url):
        '''
        Do the downlaod of the file
        :param url: url of the file to be downloaded
        :return:  downloaded file
        '''

        filename = url.split("/")[-1]
        try:
            response = requests.get(url, allow_redirects=True)
            open("pom_jar/"+filename, "wb").write(response.content)    # overwritting file in case it exists
        except BaseException as be:
            print(f"Something went wrong while downloading: {url} and the following exception was raised: {be}. Exiting!"
                  f"This operation is mandatory, exiting!")
            exit(1)
        return filename

# -----------------------------------------------------------------------------
    def is_downloadable(self, url):
        """
        Does the url contain a downloadable resource ? Checking it examining only the header
        I am aiming for a POM or JAR file, other files will be ignored
        :param url: url of the file to be checked
        :return: True if a target file is actually a POM or JAR file, False otherwise
        """

        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if "text/xml" in content_type.lower() or "application/java-archive" in content_type.lower():
            return True
        else:
            print(f"this url doesn't point nor to a POM file neighter to a JAR file but to a {content_type.lower()}")
            return False
