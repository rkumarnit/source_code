import hashlib
import numpy as np
import png
import os
import pydicom
from fpdf import FPDF
import json
import ipfsapi
from time import time
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from urllib.parse import urlparse
from uuid import uuid4

import requests

from flask import Flask, jsonify, request,render_template


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.patient_detail=''
        self.sid=''
        self.sname=''
        self.saddr=''
        self.scourse=''
        self.report_hash=''
        self.filext=''
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100,patient_detail='1',report_hash='1',filext='1')

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash,patient_detail,report_hash,filext):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'patient_detail':patient_detail,
            'filext':filext,
            'report_hash':report_hash		
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Generate "Proof Of Work"

        A very simple `Proof of Work` Algorithm -
            - Find a number such that, sum of the number and previous POW number is divisible by 7
        """

        last_proof = last_block['proof']
        proof= last_block['proof']+1
        #last_hash = self.hash(last_block)

        #proof = 0
        while not self.valid_proof(proof, last_proof):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(proof, last_proof):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        #guess = f'{last_proof}{proof}{last_hash}'.encode()
        #guess_hash = hashlib.sha256(guess).hexdigest()
        return ((proof + (int)(last_proof / 7)) & 7)==0


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    start_time = time()
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)
    print("--- %s Block Mining time in seconds ---" % (time() - start_time))

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
   #blockchain.new_transaction(
        #sender="0",
        #recipient=node_identifier,
        #amount=1,
    #)

    # Forge the new Block by adding it to the chain
    start_time = time()
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash,blockchain.patient_detail,blockchain.report_hash,blockchain.filext)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        #'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'patient_detail':block['patient_detail'],
        'filext':block['filext'],
        'report_hash':block['report_hash']
    }
    print("--- %s Block Creation time in seconds ---" % (time() - start_time))
    return jsonify(response), 200


'''@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201'''


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
	values = request.get_json()
	nodes = values.get('nodes')
	#if nodes is None:
		#return "Error: Please supply a valid list of nodes",400
	#for node in nodes:
	blockchain.register_node(nodes)
	response = {
		'message': 'New nodes have been added',
		'total_nodes': list(blockchain.nodes),
	}
	return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
	#folder_name = request.form['superhero']
	filename=""
	'''
	# this is to verify that folder to upload to exists.
	if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
		print("folder exist")
	'''
	#target = os.path.join(APP_ROOT, 'files/{}'.format(folder_name))
	#print(target)
	#if not os.path.isdir(target):
		#os.mkdir(target)
	#print(request.files.getlist("file"))
	
	filename=request.files['file']
	pid=request.form['pid']
	pname=request.form['pname']
	paddr=request.form['paddr']
	ref_doc=request.form['refdoc']
	per_doc=request.form['perdoc']
	Hospital_Name=request.form['hosname']
	f=secure_filename(filename.filename)
	filename.save(filename.filename)
	abspath1=os.path.realpath(f)
	file_name_to_create_pdf=os.path.splitext(f)[0]
	print("Location----->>>>>>",abspath1)
	print(file_name_to_create_pdf)
	print(f)
	#for upload in request.files.getlist("file"):
		#print(upload)
		#print("{} is the file name".format(upload.filename))
		#filename = upload.filename
		# This is to verify files are supported
	#ext = os.path.splitext(filename)[1]
	#if (ext == ".jpg") or (ext == ".png"):
		#print("File supported moving on...")
	#else:
		#render_template("Error.html", message="Files uploaded are not supported...")
	pdf = FPDF(orientation='P', unit='mm', format='A4')
	pdf.add_page()
	pdf.set_font("Arial", size=12)
	pdf.multi_cell(h=5.0, align='L', w=0, txt=str("Patient ID :"+pid+"\n Patient Name :"+pname+"\n Patient Address :"+paddr+"\n Reffering Doctor :"+ref_doc+"\n Performing Doctor :"+per_doc+"\n Hospital Name :"+Hospital_Name), border=0)
	pdf.output(pid+".pdf")
	start_time = time()
	api = ipfsapi.connect('127.0.0.1', 5001)
	res = api.add(f)
	print("--- %s upload time in seconds ---" % (time() - start_time))
	blockchain.report_hash=res['Hash']
	blockchain.filext=f
	res1=api.add(pid+".pdf")
	blockchain.patient_detail=res1['Hash']
	print("PDF REPORT HASH CREATION:----->>>>",blockchain.patient_detail)
	#m= api.pin_ls(type='all')
	#for h in (m):
		#if ((m[h])!=res):
			#blockchain.shash=m[h]
		#else:
	#blockchain.shash=api.pin_ls(type='all')
	#blockchain.shash=res
	#blockchain.sid=sid
	#blockchain.sname=sname
	#blockchain.saddr=saddr
	#blockchain.scourse=scourse
	print(res)
	
		
	
		#if (m==res):
			#blockchain.shash=res
			#print(m)
			#print(res)
		#else:
			#print("hash already exist in chain")
		#destination = "/".join([target, filename])
		#print("Accept incoming file:", filename)
		#print("Save it to:", destination)
		#upload.save(destination)
		

	# return send_from_directory("images", filename, as_attachment=True)
	
	return render_template("complete.html", image_name=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)
