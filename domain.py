from urllib.parse import urlparse


# get the number of dots in the url to determine the extension of the website
def get_num_of_dots(url):
    return url.count('.')


# get domain name (example.com)
def get_domain_name(url):
    try:
        # gets a list of the subdomain name
        results = get_sub_domain_name(url).split('.')
        if get_num_of_dots(url) == 2:
            # .com /.io... extension
            return results[-2]
        else:
            # .co.il/.co.uk... extension
            return results[-3]
    except:
        print('ERROR: Could extract domain name')
        return ''


# get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        # returns the network location of the given url
        return urlparse(url).netloc
    except:
        return ''
