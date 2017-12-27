#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib as hasher
import datetime as date
import glob

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode(
            'utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

# Generate genesis block
def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0")

# Simple smart contract in order to validate
# the block data (year of document > 2000)
def smart_contract(block):
    data = block[1]
    a, b = data.split(":")
    a, b, c = b.split("-")
    if int(c) > 2000:
        return True
    return False

# Generate all later blocks in the blockchain
def next_block(last_block, block):
    injection = False
    if injection and last_block.index == 3:
        this_index = 3
        this_timestamp = last_block.timestamp
        this_data = "Malicious" + str(this_index)
        this_hash = last_block.hash
    else:
        if smart_contract(block):
            this_index = last_block.index + 1
            this_timestamp = date.datetime.now()
            this_data = str(block[0] + block[1] + block[2] + block[3]) + str(this_index)
            this_hash = last_block.hash
        else:
            return -1

    new_block = Block(this_index, this_timestamp, this_data, this_hash)

    # Validate new block
    error_message = 'Invalid block!'
    if last_block.data == new_block.data:
        return error_message
    elif last_block.timestamp == this_timestamp:
        return error_message
    elif last_block.index == this_index:
        return error_message
    elif last_block.hash == new_block.hash:
        return error_message

    return new_block

def write_to_console(block, genesis):
    # Tell everyone about it!
    if genesis:
        print("Block #{} - GENESIS, has been added to the blockchain! ".format(block.index))
    else:
        print("Block #{}, has been added to the blockchain! ".format(block.index))

    print("Hash: {}".format(block.hash))
    print('DEBUG: [data: ' + str(block.data) + ', index: ' + str(block.index) + ', timestamp: ' + str(
        block.timestamp) + ', prev_hash: ' + str(block.previous_hash) + ']\n')

def readDocuments():
    docs = glob.glob("documents/*.txt")
    documents = []
    for file in docs:
        with open(file, "r") as ins:
            array = []
            for line in ins:
                array.append(line.rstrip("\n"))
            documents.append(array[:])
    return documents

def main():
    # Create the blockchain and add the genesis block
    blockchain = [create_genesis_block()]
    write_to_console(blockchain[0], True)

    previous_block = blockchain[0]

    blocks = readDocuments()

    # Add blocks to the chain
    for i in range(0, len(blocks)):

        block_to_add = next_block(previous_block, blocks[i])
        if block_to_add == -1:
            continue

        if 'Invalid block!' == block_to_add:
            print('Invalid block! ' + 'data: ' + str(blocks[i]) + 'index: ' + str(i))
            exit(1)

        blockchain.append(block_to_add)
        previous_block = block_to_add
        write_to_console(block_to_add, False)

if __name__ == "__main__":
    main()
