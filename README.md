# UsageControl-DecentralTrading
This repository contains the code for the ReGov Framework. You can find a detailed description of the ReGov Framework at this  [link](https://arxiv.org/pdf/2301.06919.pdf).

## How to run the framework
### Docker setup
To run the code, we prepared a Docker container containing all the necessary requirements in order to run the framework. 

- Intel sgx sdk
- ubuntu 18.04
- Ganche

First of all you need to have Docker installed, you can do that by following this page. After installation, you can start creating the container to run the framework. 
```
docker pull dave0909/sgx-ubuntu_18.04:latest
```
Once downloaded the image, proceed to create the container. To do this, run the following command: 
```
docker run --name UsageControl_DecentralTrading -v <VOLUME_PATH>:/volume --network host -ti <IMAGE_ID> bash
```
where:
- <VOLUME_PATH> : Path of the folder which will be mounted in the Docker container and contain the executable code.
- <IMAGE\_ID> : Id of the image just pulled with the previous command. The id of the image can be found by running the ```docker images``` command and searching for the image with the name ```dave0909/sgx-ubuntu_18.04``` among the list of images.

Once the Docker container is created, to start it run the following commands:
```
docker start UsageControl_DecentralTrading
docker attach UsageControl_DecentralTrading
```
Clone the repository in the `/volume` folder by using the following commands:
```
cd volume
git clone https://github.com/ValerioGoretti/UsageControl-DecentralTrading.git
```

## Structure of the repository
The repository is composed of two main folders. The ```/contracts``` folder contains the Solidity code of the smart contracts that are part of the blockchain infrastructure. In  ```/node``` you can find the prototype implementation of the data consumption and data provision module, respectively in ```/node/TrustedApplication``` and ```/node/pods```.
### Ganache and smart contracts
In order to setup the blockchain environment you will need to run the Ganache local blockchain and deploy the smart contracts in the ```/contracts``` folder.
Start the Ganache environment by using:
```
ganache-cli -m '<MNEMONIC_SENTENCE>' --db volume/<BLOCKCHAIN_DATA_PATH>
```
where:
- <MNEMONIC_SENTENCE> : A bip39 mnemonic phrase for generating a PRNG seed, which is in turn used for hierarchical deterministic (HD) account generation.
- <BLOCKCHAIN\_DATA\_PATH> : Location in which the blockchain data is stored.

Once Ganache is running you can use tools such as [Remix IDE] to connect to your local blockchain and deploy the smart contracts' code. 

### Intel SGX trusted application
Whenever you start the Docker container, run the following command in order to set the environment variables necessary to execute Intel SGX:
```
source /linux-sgx/linux/installer/bin/sgxsdk/environment
```
Navigate to the folder ```node/DataConsumption/TrustedApplication/``` through:
```
cd /volume/UsageControl-DecentralTrading/node/DataConsumption/TrustedApplication/
```
To build the Intel SGX application use:
```
make SGX_MODE=SIM  
```
The above command builds the application in simulation mode. If you want to run in ```HW``` mode additional steps are required to link the [SGX drivers] with your container. Notice that hardware mode is supported only in [Intel SGX enabled processors](https://www.intel.com/content/www/us/en/support/articles/000028173/processors.html).

To execute the generated binary file:
```
./app 
```

### Personal online datastore
Navigate to the folder ```node/DataProvision/pods/``` through:
```
cd /volume/UsageControl-DecentralTrading/node/DataProvision/pods/
```
The ```DTaddresses.py``` file contains all the addresses of the deployed smart contracts. Set the addresses of your deployed smart contracts. Below there is an example of the file:
```
#Address of the DTindexing smart contract.
DTINDEXING="<DTindexing_ADDRESS>"

#Address of the DTsubscriptions smart contract.
DTSUBSCRIPTION="<DTsubscriptions_ADDRESS>"

#Address of the DTtoken smart contract.
DTTOKEN="<DTtoken_ADDRESS>"
```
Finally, to run the personal online datastore ececute the command:
```
python3 app.py
```
