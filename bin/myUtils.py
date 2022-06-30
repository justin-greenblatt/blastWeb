"""
Developed for python3.8
justingreenblatt@github.com | 09/05/2022
Utils used in more than one object.
"""
from requests import get, packages
from subprocess import Popen, PIPE
from os import listdir, getcwd
from shutil import unpack_archive
from os import listdir
import logging
from time import time
from settings.logs import DOWNLOADS_LOG_PATH, DOWNLOADS_LOG_LEVEL


def downloadFromURL(url, filename = False, decompress = False):
    """
    Download data from a url link to a file.
    if decompress = True, then use gunzip on the file.
    """
    logging.basicConfig(filename=DOWNLOADS_LOG_PATH, level = DOWNLOADS_LEVEL)
    logging.info("Downloading from {}".format(url))

    #dissable warnings
    requests.packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    
    if not filename:
        filename = url.split('/')[-1]
    h = open(filename, 'wb+')

    r = get(url, stream=True, allow_redirects=True, verify=False)
    logging.debug("After requests.get() call : url requestHeaders serverResponseHeaders time [{}, {}, {}, {}]".format(
                   url, str(r.request.headers), str(r.headers), str(time())))
    data = r.content
    h = open(filename, 'wb+')
    h.write(data)
    h.close()
    logging.info("request from url {} copied to {}".format(url, filename))
    logging.debug("request from url copied to file: url filePath [{},{}]".format(url, filename))

    if decompress:
        #MODIFY LATER here for modular decompression
        command = ["gzip","-v", "-d", filename]
        dP = Popen(command, stdin = PIPE, stdout = PIPE)
        logging.debug("Running decompression process: command time processId [{}, {}, {}]".format(" ".join(command), str(time()), dP.pid))
        dP.wait()
        logging.debug("Finished decompression process: command time processId returncode stdin stdout [{}, {}, {}, {}, {}]".format(
        " ".join(command), str(time()), dP.pid, dP.returncode , dP.communicate()[1] , dP.communicate[0]))
        filename = re.match(r'replaced with (?<file>[\w|\.|\_]*)' , dP.communicate()[0]).group("file")
    return filename

def getLinks(link):
    return re.findall(r'href=\"(.*?)\"', requests.get(link, verify = False).text)

def compareDict(old, new):
    out = {}
    out["added"] = {k : new[k] for k in list(set(new.keys()) - set(old.keys()))} 
    out["removed"] = {k: old[k] for k in list(set(old.keys()) - set(new.keys()))}
    out["altered"] = {k : {"old" : old[k], "new" : new[k]} for k in list(set(old.keys()) & set(new.keys())) if old[k] != new[k]}
    out["same"] = {k : old[k]} for k in list(set(old.keys()) & set(new.keys())) if old[k] == new[k]}
    return out
