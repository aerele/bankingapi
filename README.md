## Banking API
This is a python library that gives an interface for implementing various API providers.

Reach us out at hello@aerele.in to connect with our team.

#### License

GNU/General Public License (v3) (see [license.txt](license.txt))

The Banking API code is licensed as GNU General Public License (v3) and the copyright is owned by Aerele Technologies Pvt Ltd (Aerele) and Contributors.

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

### Conventions Followed

 - Provider name - Capitalize the first letters eg: Test Provider
 - Provider's python file name - Snake Case eg: test_provider
 - Class name - Camel Case eg: TestProvider

### For new banking api implementation

Just create a provider's api python file inside ```banking_api``` module

#### Add the below functions

 - ```fetch_balance``` 
 - ```fetch_statement```
 - ```initiate_transaction_without_otp``` 
 - ```initiate_transaction_with_otp```
 - ```get_transaction_status```
 - ```send_otp```
 - ```fetch_statement_with_pagination```


#### Note

1. Refer [Common Provider](common_provider.py ) and [Test API Provider](test.py) for request and response format.
2. If ```transaction_type_mapping``` not found for your api provider. Just include it under the ```Common Provider``` init function.

#### TODO
1. Need to test ```fetch_statement_with_pagination``` API.


### Show some ❤️ by starring :star: :arrow_up: our repo!
