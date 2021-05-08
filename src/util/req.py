import requests
import json
from typing import Union
import logging
logger = logging.getLogger(__name__)

def request_get(url: str) -> Union[dict,None]:
    """get request function

    Args:
        url (str): URL

    Returns:
        dict: received data in dictionary
    """ 
    try:
        headers = {
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
        }
        url_result = requests.get(url,headers=headers)
        rec_data = json.loads(url_result.text)
        return rec_data
    except Exception as e:
        logger.error(str(e))
        return None
