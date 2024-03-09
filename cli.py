import os
import re
import requests

class CookieTester:
    @staticmethod
    def parseCookieFile(cookiefile):
        """Parse a cookies.txt file and return a dictionary of key value pairs
        compatible with requests.
    
        not using cookielib because not in python3 : https://stackoverflow.com/a/54659484
        
        Return : 
            1. dict : Cookies dictionary 
            2. str : if error occur while parsing, return text to display or print"""
    
        cookies = {}
        with open(cookiefile, 'r') as fp:
            for line in fp:
                if not re.match(r'^\#', line):
                    lineFields = re.findall(r'[^\s]+', line)  # capturing anything but empty space
                    try:                           
                        cookies[lineFields[5]] = lineFields[6]
                    except Exception as e:
                        if len(lineFields) == 7: # lineFields[6] not exists because length is not 7(index 6)
                            return f"There is no value for {lineFields[5]} given in cookie file {cookiefile}"
                        return f"Error parsing {cookiefile}: {e}"

        return cookies
    
    @staticmethod
    def test_cookie(cookie_file, url, send_out):
        """Tests if a cookies file is working by sending a GET request to a URL with the cookie.
    
        Args:
            cookie_file: The path to the file containing the Netscape cookie.
            url: The URL to which the GET request should be sent.
    
        Returns:
            1. Boolean : True if the cookie is working, False otherwise.
            2. str : if error occur while parsing, return text to display or print (in this case, used to pass file move command)
        """
    
        r = CookieTester.parseCookieFile(cookie_file)
        
        if isinstance(r, str):
          send_out(r)
          return r
        
        cookies = r
    
        r = requests.get(url, cookies=cookies)
    
        if "Sign in" not in r.text:
            return True
        else:
            return False
    
    @staticmethod
    def run(directory, url, send_out = print):
        """Iterates over all files in a directory and tests if the cookies in Netscape format are working by sending a GET request to a URL with the cookie.
    
        Args:
            directory: The path to the directory containing the Netscape cookie files.
            url: The URL to which the GET request should be sent.
            send_out: a method that take text and perform task, default is print so it will print out. can be replace with LOGGER or put text in TEXTBOX.
        """
        
        listdir = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]
    
        out_dir = os.path.join(directory, "works/")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        dead_dir = os.path.join(directory, "dead_cookies/")
        if not os.path.exists(dead_dir):
            os.makedirs(dead_dir)
    
        i = 0
        for filename in listdir:
            if filename.endswith(".txt"):
                cookie_file = os.path.join(directory, filename)
                
                r = CookieTester.test_cookie(cookie_file, url, send_out)
                if isinstance(r,str):
                    pass
                elif r:
                    send_out(f"Cookie in file {filename} is working.")
                    os.rename(cookie_file, os.path.join(out_dir, filename))
                    i += 1
                else:
                    os.rename(cookie_file, os.path.join(dead_dir,filename))
    
        send_out("="*50)
        send_out(f"Total cookies file checked: {len(listdir)}")
        send_out(f"Only {i} file working")
        
if __name__ == '__main__':
  directory = input("Enter directory path where cookies .txt are located : ")
  url = "https://netflix.com"
  CookieTester.run(directory, url)
