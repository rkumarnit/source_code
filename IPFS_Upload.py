from web3 import Web3
import ipfsapi
from time import time
import json
#infura_url="https://mainnet.infura.io/v3/aac3565adf2445c4b4ad9801389d92ad"
url="http://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(url))
print(web3.isConnected())
web3.eth.defaultAccount='0x81460888b6072d6eC909E4C932E470Ae1c15461B'
contract_address=web3.toChecksumAddress("0xBfc5fa1AdD6f536A25843575618B36c74ED03352")

abi=json.loads('[ 	{ 		"constant": false, 		"inputs": [ 			{ 				"name": "hash", 				"type": "string" 			} 		], 		"name": "setHash", 		"outputs": [], 		"payable": false, 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [], 		"name": "getHash", 		"outputs": [ 			{ 				"name": "", 				"type": "string" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	} ]')
#abi=json.loads('[ 	{ 		"constant": false, 		"inputs": [ 			{ 				"name": "_name", 				"type": "string" 			}, 			{ 				"name": "_age", 				"type": "uint256" 			}, 			{ 				"name": "_designation", 				"type": "uint256" 			}, 			{ 				"name": "_hash", 				"type": "string" 			} 		], 		"name": "add_agent", 		"outputs": [], 		"payable": false, 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"constant": false, 		"inputs": [ 			{ 				"name": "addr", 				"type": "address" 			} 		], 		"name": "permit_access", 		"outputs": [], 		"payable": true, 		"stateMutability": "payable", 		"type": "function" 	}, 	{ 		"constant": false, 		"inputs": [ 			{ 				"name": "paddr", 				"type": "address" 			}, 			{ 				"name": "daddr", 				"type": "address" 			} 		], 		"name": "remove_patient", 		"outputs": [], 		"payable": false, 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"constant": false, 		"inputs": [ 			{ 				"name": "daddr", 				"type": "address" 			} 		], 		"name": "revoke_access", 		"outputs": [], 		"payable": true, 		"stateMutability": "payable", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "", 				"type": "uint256" 			} 		], 		"name": "doctorList", 		"outputs": [ 			{ 				"name": "", 				"type": "address" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "addr", 				"type": "address" 			} 		], 		"name": "get_accessed_doctorlist_for_patient", 		"outputs": [ 			{ 				"name": "", 				"type": "address[]" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "addr", 				"type": "address" 			} 		], 		"name": "get_accessed_patientlist_for_doctor", 		"outputs": [ 			{ 				"name": "", 				"type": "address[]" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "addr", 				"type": "address" 			} 		], 		"name": "get_doctor", 		"outputs": [ 			{ 				"name": "", 				"type": "string" 			}, 			{ 				"name": "", 				"type": "uint256" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [], 		"name": "get_doctor_list", 		"outputs": [ 			{ 				"name": "", 				"type": "address[]" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "paddr", 				"type": "address" 			} 		], 		"name": "get_hash", 		"outputs": [ 			{ 				"name": "", 				"type": "string" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "addr", 				"type": "address" 			} 		], 		"name": "get_patient", 		"outputs": [ 			{ 				"name": "", 				"type": "string" 			}, 			{ 				"name": "", 				"type": "uint256" 			}, 			{ 				"name": "", 				"type": "uint256[]" 			}, 			{ 				"name": "", 				"type": "address" 			}, 			{ 				"name": "", 				"type": "string" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "paddr", 				"type": "address" 			}, 			{ 				"name": "daddr", 				"type": "address" 			} 		], 		"name": "get_patient_doctor_name", 		"outputs": [ 			{ 				"name": "", 				"type": "string" 			}, 			{ 				"name": "", 				"type": "string" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [], 		"name": "get_patient_list", 		"outputs": [ 			{ 				"name": "", 				"type": "address[]" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"constant": true, 		"inputs": [ 			{ 				"name": "", 				"type": "uint256" 			} 		], 		"name": "patientList", 		"outputs": [ 			{ 				"name": "", 				"type": "address" 			} 		], 		"payable": false, 		"stateMutability": "view", 		"type": "function" 	} ]')
#address="0x1d3309416D544Baa3894502691153d5f9d31eaa9"
contract=web3.eth.contract(address=contract_address,abi=abi)
print(contract)
start_time = time()
api = ipfsapi.connect('127.0.0.1', 5001)
f="Tx-5.txt"
res = api.add(f)
value=res['Hash']
print(value)
print("--- %s upload time in seconds ---\n" % (time() - start_time))
# Build a transaction 
start_time3 = time()
tx=contract.functions.setHash(value).transact()
print("--- %s Block creation or share time in seconds ---\n" % (time() - start_time3))
#wait for transaction to be mined 
star_time1=time()
web3.eth.waitForTransactionReceipt(tx)
print("----%s Block mining time in seconds -----\n" %(time()-star_time1))
#printing the value os Updated Message
star_time2=time()
print('updated value: {}'.format(contract.functions.getHash().call()))

print("----%s Tx hash Access time in seconds -----\n" %(time()-star_time2))

