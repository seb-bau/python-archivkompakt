import base64
import hashlib
import json
import shutil

import requests
from datetime import datetime


class ArchivKompaktAuthError(Exception):
    """Raised when there is an error during token creation"""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ArchivKompaktAuthError, {0} '.format(self.message)
        else:
            return 'ArchivKompaktAuthError raised'


class ArchivKompaktError(Exception):
    """Raised when there is an error during token creation"""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ArchivKompaktError, {0} '.format(self.message)
        else:
            return 'ArchivKompaktError raised'


def local_get_doc_with_id(doc_id, doc_json):
    for t_doc in doc_json:
        if t_doc['ID'] == doc_id:
            return t_doc
    return None


def dlinfo_zu_dict(dlinfo: str):
    dlinfo_raw = base64.b64decode(dlinfo)
    dlinfo_list = dlinfo_raw.splitlines()
    try:
        ret_dict = {
            'ak_id': dlinfo_list[1].decode("utf-8"),
            'md5': dlinfo_list[5].decode("utf-8").lower(),
            'typ': dlinfo_list[2].decode("utf-8")

        }
    except UnicodeDecodeError:
        return None

    return ret_dict


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def creation_date_to_dt(ak_create_date: str):
    t_create_timestamp = int(str(ak_create_date).split('(')[1].split(')')[0].split('+')[0]) / 1000
    return datetime.fromtimestamp(t_create_timestamp)


def build_filter(filter_key, filter_value):
    ret_val = [
        {
            "ID": filter_key,
            "Value": filter_value
        }
    ]
    return ret_val


class ArchivKompakt:
    def __init__(self, hostname: str, user: str, password: str, scope: str, client_id: str = None,
                 client_secret: str = None, auth: str = None):
        self.hostname = f"{hostname.rstrip('/')}/AAKRest"
        self.user = user
        self.password = password
        if auth is None:
            self.auth = base64.b64encode("{}:{}".format(client_id, client_secret))
        else:
            self.auth = auth
        self.scope = scope
        self.token = self.create_token()

    def create_token(self):
        url = f"{self.hostname}/Token"

        payload = f"grant_type=password&" \
                  f"username={self.user}&" \
                  f"password={self.password}&" \
                  f"scope={self.scope}"

        headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            raise ArchivKompaktAuthError(response.text)

        response_json = response.json()
        return response_json["access_token"]

    def get_archives(self):
        url = f"{self.hostname}/v1/archives"

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code != 200:
            return False, response.text
        else:
            response_json = response.json()
            return response_json, None

    def get_index_id(self, index_name):
        archives_json, archives_error = self.get_archives()
        for archive in archives_json:
            for prop in archive['Indexes']:
                if prop['Name'] == index_name:
                    return prop['ID']
        return None

    def get_docs_with_payload(self, index_payload, chunk_size=500, arc_id=None):
        url = f"{self.hostname}/v2/search"

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        if index_payload is None:
            t_indexes = []
        else:
            t_indexes = index_payload

        payload = {
            "maxHits": chunk_size,
            "indexes": t_indexes
        }

        if arc_id is not None:
            if type(arc_id) != list:
                arc_id = [arc_id]

            payload["arcIDs"] = arc_id

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise ArchivKompaktError(response.text)
        else:
            return response.json()

    def get_doc_with_id(self, doc_id):
        url = f"{self.hostname}/v1/documents/{doc_id}"

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return False
        else:
            raise ArchivKompaktError(response.text)

    def download_file(self, dlinfo: str, local_path: str):
        expected_md5 = dlinfo_zu_dict(dlinfo)['md5'].lower()
        url = f"{self.hostname}v1/files/{dlinfo}"
        # print(url)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'access_token': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.get(url, stream=True, headers=headers)
        if response.status_code != 200:
            print("ERROR {}".format(response.status_code))
            return False

        with open(local_path, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

        # Hashsumme prüfen
        t_dlhash = md5(local_path)

        if t_dlhash != expected_md5:
            print(f"Error! Datei {local_path} erwartete Checksum {expected_md5} != {t_dlhash}")
            return False

        return True
