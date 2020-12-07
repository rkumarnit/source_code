import pandas as pd
from time import time
from ecdsa import SigningKey
from ecdsa import ECDH, NIST256p
from eth_account.messages import encode_defunct
from web3 import Web3
import ipfsapi
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
#start_time = time()
#api = ipfsapi.connect('127.0.0.1', 5001)
#f="Tx_size-5.txt"
#res = api.add(f)
#value=res['Hash']
#print(value)
#print("--- %s upload time in seconds ---\n" % (time() - start_time))

bytecode =  "608060405234801561001057600080fd5b506102d7806100206000396000f30060806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680631ed83fd414610051578063d13319c4146100ba575b600080fd5b34801561005d57600080fd5b506100b8600480360381019080803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919291929050505061014a565b005b3480156100c657600080fd5b506100cf610164565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561010f5780820151818401526020810190506100f4565b50505050905090810190601f16801561013c5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b8060009080519060200190610160929190610206565b5050565b606060008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156101fc5780601f106101d1576101008083540402835291602001916101fc565b820191906000526020600020905b8154815290600101906020018083116101df57829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061024757805160ff1916838001178555610275565b82800160010185558215610275579182015b82811115610274578251825591602001919060010190610259565b5b5090506102829190610286565b5090565b6102a891905b808211156102a457600081600090555060010161028c565b5090565b905600a165627a7a7230582070ada6f8101de2cf88f3d2e74d7afa27659333b35cc8bb5ac700b639dd59f8390029"
	

ipfsupload1 = web3.eth.contract(abi=abi, bytecode=bytecode)
#print("----%s Tx hash Access time in seconds -----\n" %(time()-star_time2))
userDf=pd.read_csv('data_corr.csv',nrows=1600)
list=userDf.values.tolist();
#print(list)
strval=""
strval2=""
strval3=""
strval4=""
#start_reg_time1=time();
#ecdh = ECDH(curve=NIST256p)
#private_key1=ecdh.generate_private_key()
#local_public_key1 = ecdh.get_public_key()
#end_reg_time1=time();

#private_key="f1be43f2b342582dfd8f03bfc2121eb89ad26662afa30f5edcdedfe208edfa3f"
#strval=[''.join(ele) for ele in list]



strt_time=time();
start_time1 = []
start_time2 = []
start_time3 = []
start_time4=[]
start_time5=[]
start_reg_time=[]
for record in list:
        src_ip=record[1]
        dest_ip=record[2]
        proto=record[3]
        service=record[4]
        #connection_st=record[5]
        #dns_qry=record[6]
        #dns_AA=record[7]
        #dns_RD=record[8]
        #dns_RA=record[9]
        #dns_reject=record[10]
        #http1=record[11]
        #weired=record[12]
        #ts=record[13]
        #src_port=record[14]
        #dst_port=record[15]
        #dns_qtype=record[16]
        #dns_rcode=record[17]
        #http_st=record[18]
        strval4=src_ip,dest_ip,proto,service
        strval3=''.join(str(ele) for ele in strval4)
        strval3=''+strval3
        strval=''.join([str(elem) for elem in record])
        print(strval3)
        strval2=strval2+strval
        #send Transaction
        tx=contract.functions.setHash(strval3).transact()
        start_time1.append(time())
        #signed Transaction
        sk = SigningKey.generate() # uses NIST192p
        vk = sk.verifying_key
        #txstr=str(tx)
        signature = sk.sign(tx)
        #signed = web3.eth.account.signHash(tx,private_key=private_key)
        start_time4.append(time())
        #contract creation and deployement
        tx_hash = ipfsupload1.constructor().transact()
        start_time5.append(time())
        #mined transaction
        web3.eth.waitForTransactionReceipt(tx)
        start_time2.append(time())
        #access transaction
        print('updated value: {}'.format(contract.functions.getHash().call()))
        start_time3.append(time())
        #registration process of IoT node
        ecdh = ECDH(curve=NIST256p)
        private_key1=ecdh.generate_private_key()
        local_public_key1 = ecdh.get_public_key()
        start_reg_time.append(time())

#IPFS Upload Time
#print ('Transaction send time',start_time1)
#print('Transaction mining time', start_time2)
#print('Transaction access time', start_time3)
start_time = time()
api = ipfsapi.connect('127.0.0.1', 5001)
file1 = open("MyFile.txt","w") 
file1.write(strval2)
file_upload1="F:\\Drop-Box material\\Prabhat_Randhir\\IEEE_Transaction_Code\\Ethereum-Connectivity\\MyFile.txt"		
res = api.add(file_upload1)
#value=res['Hash']
#print(value)
print("--- %s upload time in seconds ---\n" % (time() - start_time))

# Python program to get average of a list 
def Average(lst): 
    return sum(lst) / len(lst) 
  
# Driver Code 
#lst = [15, 9, 55, 41, 35, 20, 62, 49] 
average = Average(start_time2) 
# Printing average of the list 
print("Block_Mining Time", time()- round(average, 2))
#print("Block_Mining Time %s" % (strat_time2/200))
average = Average(start_time1)
print("Block_Creation Time",time()- round(average, 2))
#print("Block_Creation Time %s" % (strat_time1/200))
average = Average(start_time3)
print("Block_Access Time ",time()- round(average, 2))
average= Average(start_time4)
print("Transaction Signed Time ",time()- round(average, 2))
average=Average(start_time5)
print("Contract Creation ",time()- round(average, 2))
average=Average(start_reg_time)
print("Registration Time", time()- round(average, 2))
#print("Block_Access Time %s" % (strat_time3/200))
# Build a transaction
#start_time3 = time()
#Tx_value=src_ip,"",dest_ip,"",proto,"",service,"",connection_st,"",dns_qry,"",dns_AA,"",dns_RD,"",dns_RA,"",dns_reject,"",http1,"",weired,"",ts,"",src_port,"",dst_port,"",dns_qtype,"",dns_rcode,"",http_st
#Tx_val1=str(Tx_value)
#Tx_value=str(list);
#print(strval2)
#tx=contract.functions.setHash(strval).transact()
#print("--- %s Block creation or share time in seconds ---\n" % (time() - start_time3))
#wait for transaction to be mined 
#star_time1=time()
#web3.eth.waitForTransactionReceipt(tx)
#print("----%s Block mining time in seconds -----\n" %(time()-star_time1))
#printing the value os Updated Message
#star_time2=time()
#print('updated value: {}'.format(contract.functions.getHash().call()))
        
#print(src_ip,"",dest_ip,"",proto,"",service,"",connection_st,"",dns_qry,"",dns_AA,"",dns_RD,"",dns_RA,"",dns_reject,"",http1,"",weired,"",ts,"",src_port,"",dst_port,"",dns_qtype,"",dns_rcode,"",http_st)
#calculating Reputation of shared Transactions//


#print('data of first five rows')
#print(list,"\n")
