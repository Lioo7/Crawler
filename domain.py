from urllib.parse import urlparse


# get domain name (example.com)
def get_domain_name(url):
    try:
        # gets a list of the subdomain name
        results = get_sub_domain_name(url).split('.')
        # returns the last two words of the domain
        return results[-2] + '.' + results[-1]
    except:
        return ''


# get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        # returns the network location of the given url
        return urlparse(url).netloc
    except:
        return ''
