import time , http.client , re , sys

class url_lib:
    def __init__(self,url="url str"):
        if url[:4] == "http":
            self.url=url
        else:
            self.url=""
        self.Headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            }
    
    def Get(self,key=[["key","value"]],port=80,url=None):
        if not url:
            url=self.url
        HTTPS_FLAG=False
        if url[-1]!="?":
            url+="?"
        if r"http://" in url:
            host=re.compile(r"http://[^/]*").findall(url)[0].replace("http://","")
        elif r"https://" in url:
            host=re.compile(r"https://[^/]*").findall(url)[0].replace("https://","")
            port=443
            HTTPS_FLAG=True
            for i in key:
                url +="&" + i[0] + "=" + i[1]
        if HTTPS_FLAG:
            h=http.client.HTTPSConnection(host,port)
        else:
            h=http.client.HTTPConnection(host,port)
        h.request("GET",url,headers=self.Headers)
        return h.getresponse()

    def Post(self,data={"keyname":"keyword",},port=80,url=None):
        if not url:
            url=self.url
        HTTPS_FLAG=False
        if r"http://" in url:
            host=re.compile(r"http://[^/]*").findall(url)[0].replace("http://","")
        elif r"https://" in url:
            host=re.compile(r"https://[^/]*").findall(url)[0].replace("https://","")
            port=443
            HTTPS_FLAG=True
        post_data_str = urlencode(data)

        if HTTPS_FLAG:
            h=http.client.HTTPSConnection(host,port)
        else:
            h=http.client.HTTPConnection(host,port)
        h.request("POST",url,post_data_str,headers=self.Headers)
        return h.getresponse()
    
    def Head(self,port=80,url=None):
        url=self.url
        host=re.compile(r"http://[^/]*").findall(url)[0].replace("http://","")
        h=http.client.HTTPConnection(host,port)
        h.request("HEAD",url,headers=self.Headers)
        res=h.getresponse()
        h.close();h=None
        return res.getheaders()



_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                         b'abcdefghijklmnopqrstuvwxyz'
                         b'0123456789'
                         b'_.-')
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)
def quote(string, safe='/', encoding=None, errors=None):
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return quote_from_bytes(string, safe)

def quote_plus(string, safe='', encoding=None, errors=None):
    if ((isinstance(string, str) and ' ' not in string) or
        (isinstance(string, bytes) and b' ' not in string)):
        return quote(string, safe, encoding, errors)
    if isinstance(safe, str):
        space = ' '
    else:
        space = b' '
    string = quote(string, safe + space, encoding, errors)
    return string.replace(' ', '+')

def quote_from_bytes(bs, safe='/'):
    if not isinstance(bs, (bytes, bytearray)):
        raise TypeError("quote_from_bytes() expected bytes")
    if not bs:
        return ''
    if isinstance(safe, str):
        safe = safe.encode('ascii', 'ignore')
    else:
        safe = bytes([c for c in safe if c < 128])
    if not bs.rstrip(_ALWAYS_SAFE_BYTES + safe):
        return bs.decode()
    try:
        quoter = _safe_quoters[safe]
    except KeyError:
        _safe_quoters[safe] = quoter = Quoter(safe).__getitem__
    return ''.join([quoter(char) for char in bs])

def urlencode(query, doseq=False, safe='', encoding=None, errors=None,
              quote_via=quote_plus):

    if hasattr(query, "items"):
        query = query.items()
    else:
        try:
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
        except TypeError:
            ty, va, tb = sys.exc_info()
            raise TypeError("not a valid non-string sequence "
                            "or mapping object").with_traceback(tb)

    l = []
    if not doseq:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_via(k, safe)
            else:
                k = quote_via(str(k), safe, encoding, errors)

            if isinstance(v, bytes):
                v = quote_via(v, safe)
            else:
                v = quote_via(str(v), safe, encoding, errors)
            l.append(k + '=' + v)
    else:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_via(k, safe)
            else:
                k = quote_via(str(k), safe, encoding, errors)

            if isinstance(v, bytes):
                v = quote_via(v, safe)
                l.append(k + '=' + v)
            elif isinstance(v, str):
                v = quote_via(v, safe, encoding, errors)
                l.append(k + '=' + v)
            else:
                try:
                    # Is this a sufficient test for sequence-ness?
                    x = len(v)
                except TypeError:
                    # not a sequence
                    v = quote_via(str(v), safe, encoding, errors)
                    l.append(k + '=' + v)
                else:
                    # loop over the sequence
                    for elt in v:
                        if isinstance(elt, bytes):
                            elt = quote_via(elt, safe)
                        else:
                            elt = quote_via(str(elt), safe, encoding, errors)
                        l.append(k + '=' + elt)
    return '&'.join(l)