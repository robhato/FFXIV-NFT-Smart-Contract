from brownie import AdvancedCollectible, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_bclass
from pathlib import Path
import os
import requests
import json

def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        bclass = get_bclass(nft_contract.tokenIdToBclass(token_id))
        # Create metadata file with path to metadata folder e.g. ./metadata/rinkeby/0-DANCER.json
        metadata_filename = (
            "./metadata/{}/".format(network.show_active()) + str(token_id)
            + "-" + bclass + ".json"
        )
        if Path(metadata_filename).exists():
            print("{} already found!".format(metadata_filename))
        else:
            print("Creating Metadata File {}".format(metadata_filename))
            collectible_metadata["name"] = get_bclass(nft_contract.tokenIdToBclass(token_id))
            collectible_metadata["description"] = "The {} class in hit MMORPG Final Fantasy XIV!".format(collectible_metadata["name"].lower())
            if (collectible_metadata["name"] == 'DANCER'):
                collectible_metadata["attributes"][0]["value"] = "DPS"
            elif (collectible_metadata["name"] == 'GUNBREAKER'):
                collectible_metadata["attributes"][0]["value"] = "TANK"
            else:
                collectible_metadata["attributes"][0]["value"] = "HEALER"
            # print(collectible_metadata)
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "True":
                image_path = "./img/{}.png".format(bclass.lower())
                image_to_upload = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_to_upload
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "True":
                upload_to_ipfs(metadata_filename)

# 0x20B8283C9C7AC2FbFFcBEBB77dFA44930D562D36
# http://127.0.0.1:5001/webui

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(uri)
        return uri
    return None
