from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_bclass, fund_advanced_collectible
import time

STATIC_SEED = 123

def main():
    dev = accounts.add(config['wallets']['from_key'])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible)-1]
    transaction = advanced_collectible.createCollectible(STATIC_SEED,"None", {"from": dev})
    transaction.wait(1)
    requestId = transaction.events['requestedCollectible']['requestId']
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    time.sleep(35)
    bclass = get_bclass(advanced_collectible.tokenIdToBclass(token_id))
    print('WoL class of tokenId {} is {}'.format(token_id, bclass))