## Banking API
This is a python library that helps to access various Banking APIs.

### Installation

To install Python package from github, you need to clone the repository
```
git clone https://github.com/aerele/bankingapi.git
```
Then just run the setup.py file from the repo directory
```
sudo python setup.py install
```

### API Usage
Create the CommonProvider object and you will be ready to call api.

### Basic Usage
The following is an example code block on how to use bankingapi.

```
import banking_api
from banking_api.common_provider import CommonProvider
prov = CommonProvider('Test')
balance = prov.fetch_balance()
stmt = prov.fetch_statement()
print(balance)
print(stmt)
```

### Conventions followed

 - provider name - Capitalize the first letters eg: Test Provider
 - provider's python file name - Snake Case eg: test_provider
 - class name - Camel Case eg: TestProvider

### For new banking api implementation

Just create a provider's api python file inside ```banking_api``` module

### Initial implemented functions

 - ```fetch_balance``` 

    Example response format:
    ```
    {'account_no':'1789123456789', 'date': '03/12/20 09:37:22', 'balance': '960368.91', 'currency': 'INR'}
    ```
  
 - ```fetch_statement```

    Example response format:
    ```
    [{'txn_date':'03-12-2020 08:16:34',
    'txn_id':'S32528713',
    'credit': '92,18,756.36',
    'debit': 0,
    'balance': '1,22,18,756.36',
    'remarks': 'No remarks found'
    },
    {'txn_date':'02-12-2020 08:16:34',
    'txn_id':'S52528715',
    'credit': '12,18,756.36',
    'debit': 0,
    'balance': '1,32,18,756.36',
    'remarks': 'No remarks found'
    }]
    ```
