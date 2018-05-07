"""this will attempt to import domains2.py, and failing to, will grab it from my pub github
   and then import it"""
import urllib, os

def domains():
    RAW_DOMAINS = 'https://raw.githubusercontent.com/imightbelying63/python/master/cpanel/domains2.py'
    try:
        import domains2
    except ImportError:
        try:
           urllib.urlretrieve(RAW_DOMAINS, 'domains2.py')
           import domains2
           domains2_file = RAW_DOMAINS.split(os.path.sep)[-1]
           if os.path.exists(domains2_file):
               os.remove(domains2_file)
               if os.path.exists(domains2_file + 'c'):
                   os.remove(domains2_file + 'c')
        except:
            print 'unable to retrieve required script'    
    return None

if __name__ == "__main__":
    domains()
