class Login:
    """


    DO I REALLY NEED THIS?



    This is just for authentification, contains username and access token in order to use github APIs
    """

    # constructor: inizializzating obj properties
    def __init__(self):
        self.username = "bogalt"
        self.access_token = "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"

    # get username method
    def get_username(self):
        return self.username

    # get access token method
    def get_access_token(self):
        return self.access_token
