# archivkompakt
### Python-Wrapper for Aareon Archiv Kompakt REST API

This Python module provides basic access to the Aareon archiv kompakt DMS API.  

#### The following functionalities are implemented:
* Create bearer Token
* Basic document search
* Download binaries of document
* Get document by document id

Currently, there is no upload functionality as my projects do not require them. If you need this, let me know!

#### Installation
Install the module via pip (dependencies are: requests)  

```
pip install archivkompakt
```

#### Example: Search all documents where comment-Field contains "test"
```python
from archivkompakt import ArchivKompakt, ArchivKompaktAuthError, ArchivKompaktError

host = "http://host-of-aak"
user = "username"
password = "password"
scope = "[12345678]_CUSTOMER"
client_id = "abcdef"
client_secret = "XXX-XXX-YYY-YYY"

try:
    aak = ArchivKompakt(hostname=host, user=user, password=password, scope=scope, client_id=client_id,
                        client_secret=client_secret)
    
    document_filter = [
        {
            "ID": 1,
            "Value": "*test*"
        }
    ]

    docs = aak.get_docs_with_payload(index_payload=document_filter)
    print(f"Found {len(docs)} documents")
    
except ArchivKompaktAuthError as err:
    print(f"Error during authentifaction: {err.message}")
except ArchivKompaktError as err:
    print(f"Error during request: {err.message}")
```

#### Remarks
* get_docs_with_payload has a parameter "arc_id" which can be an integer or a list of integers, so you can specify  
archive ids
* The functions return the documents as json, the AAK format remains untouched
* You need to request the values for scope, client_id and client_secret from Aareon support

#### Next steps
* I would like to simplfy the document filter - currently you need to know which ID your index has