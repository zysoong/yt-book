import os.path

import hashlib
from urllib.parse import urlparse, parse_qs


def get_tmp_directory(url: str, tmp_basedir: str) -> str:
    if "youtube" not in url:
        sha = hashlib.sha256(url.encode('utf-8')).hexdigest()
        return os.path.join(tmp_basedir, sha)

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get('v', [None])[0]
    list_id = query_params.get('list', [None])[0]

    if video_id is None:
        sha = hashlib.sha256(url.encode('utf-8')).hexdigest()
        return os.path.join(tmp_basedir, sha)

    if list_id:
        return os.path.join(tmp_basedir, f"{list_id}_{video_id}")
    else:
        return os.path.join(tmp_basedir, video_id)