from brownie import AdvancedCollectible, network, accounts, config
from scripts.helpful_scripts import get_bclass

bclass_metadata_dic = {
    "DANCER": "https://ipfs.io/ipfs/QmdYHQeJgs8e9pPGRPYoqYsMSpgZRAgAppQjr4JDuno2QD?filename=0-DANCER.json",
    "GUNBREAKER": "https://ipfs.io/ipfs/QmdsMjCUV2GULGS51zB9fy94cZJTUAodF63YDzU3K2cSiq?filename=1-GUNBREAKER.json",
    "ASTROLOGIAN": "https://ipfs.io/ipfs/QmerBwTL34yf9yP8NZDFvjRoejX7kYndmu7QXzf7HuXqNo?filename=2-ASTROLOGIAN.json"
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is: " + str(number_of_advanced_collectibles))
    for token_id in range(number_of_advanced_collectibles):
        bclass = get_bclass(advanced_collectible.tokenIdToBclass(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible, bclass_metadata_dic[bclass])
        else:
            print("Skipping {}, we've already set that tokenURI!").format(token_id)

def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config['wallets']['from_key'])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can now view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print("Please allow around 20 minutes and click the 'refresh metadata button' to view data.")