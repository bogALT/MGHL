from GitManager import GitManager
from MyException import MyException


def main():
    
    #urls = ['http://github.com/mbosecke/pebble.git']    
    # urls ending with .git are not recognised as valid because they redirect you to a different page
    # in fact the above url goes to https://github.com/PebbleTemplates/pebble (only in web browser, not here)
    
    urls = ['https://github.com/Netflix/conductor', 'https://github.com/Netflix/conductor']
    urls = ['https://github.com/lucee/Lucee']

    cv = "5.4.2.19"
    pv = "5.3.11.7"

    try: 
        gm = GitManager(urls, cv, pv)   #cv = current ver, pv = precedent vers
        repo_url = gm.start()       # start GH manager 
    except MyException as me:
        # handle here the exception
        print("Caught exception in Main GH= ", me)

if __name__ == "__main__":
    main()
