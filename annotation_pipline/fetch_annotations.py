import json
from typing import List, Dict

from requests import get
from retry import retry

ANNOTATION_URL = "https://hypothes.is/api/search?limit=50&user=niklas_thesis"


@retry(tries=3, delay=2)
def fetch_annotations() -> List[Dict]:
    """TODO: Check how to fetch all annotations (can I just omit the limit?)"""

    r = get(ANNOTATION_URL)
    annotations = json.loads(r.text)["rows"]
    return annotations
