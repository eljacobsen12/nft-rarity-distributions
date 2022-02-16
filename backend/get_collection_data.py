import requests
import json
import pandas as pd
#from web3 import Web3


def get_collection_opensea(slug):
    url = "https://api.opensea.io/api/v1/collection/" + str(slug)
    opensea = requests.get(url)
    collection = json.loads(opensea.content)
    #print('NAME: ' + '\t\t' + str(collection['collection']['name']))
    #print('ADDRESS: ' + '\t' + str(collection['collection']['primary_asset_contracts'][0]['address']))
    #print('OWNER: ' + '\t\t' + str(collection['collection']['primary_asset_contracts'][0]['payout_address']))
    #print('SLUG: ' + '\t\t' + str(collection['collection']['slug']))
    #print('LINK: ' + '\t\t' + str(collection['collection']['primary_asset_contracts'][0]['external_link']))
    #print('IMAGE: ' + '\t\t' + str(collection['collection']['image_url']))
    #print('SCHEMA: ' + '\t' + str(collection['collection']['primary_asset_contracts'][0]['schema_name']))
    #print('TWITTER: ' + '\t' + str(collection['collection']['twitter_username']))
    #print('DISCORD: ' + '\t' + str(collection['collection']['discord_url']))
    #print('MEDIUM: ' + '\t' + str(collection['collection']['medium_username']))
    #print('INSTAGRAM: ' + '\t' + str(collection['collection']['instagram_username']))
    #print('TELEGRAM: ' + '\t' + str(collection['collection']['telegram_url']))
    #print('WIKI: ' + '\t\t' + str(collection['collection']['wiki_url']))
    return collection

def get_contract_etherscan(address):
    key = 'H6DPR46U1EKHIXEXZH7BN64KBCCZ7YN23W'
    url = ('https://api.etherscan.io/api?module=contract&action=getabi&address=' +  str(address) + '&apikey=' +  str(key))
    etherscan = requests.get(url)
    return json.loads(etherscan.content)


# Get collection data on batch.
def get_collections_csv(path):
    csv = pd.read_csv(path)

    for index, row in csv.iterrows():
        if row.slug != 'NULL':
            collection = get_collection_opensea(row.slug)
            print('SLUG:' + '\t\t' + str(collection['collection']['slug']))
            print('ADDRESS:' + '\t' + str(collection['collection']['primary_asset_contracts'][0]['address']))
            print('OWNER:' + '\t\t' + str(collection['collection']['payout_address']))
            print('SCHEMA: ' + '\t' + str(collection['collection']['primary_asset_contracts'][0]['schema_name']))
        else:
            print('SLUG:' + '\t\t' + 'NULL')
        print('\n')


slug = 'bored-ape-kennel-club'

collection = get_collection_opensea(slug)
print(collection)
#contract = get_contract_etherscan(address)