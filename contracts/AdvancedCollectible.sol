pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {

    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;

    enum Bclass{DANCER, GUNBREAKER, ASTROLOGIAN}

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Bclass) public tokenIdToBclass;
    mapping(bytes32 => uint256) public requestIdToTokenId;

    event requestedCollectible(bytes32 indexed requestId);

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("wols", "FFXIVWOL") {
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18; // 0.1 LINK 1000000000000000000
        tokenCounter = 0;
    }

    function createCollectible(uint256 userProvidedSeed, string memory tokenURI) 
        public returns (bytes32) {
            bytes32 requestId = requestRandomness(keyHash, fee, userProvidedSeed);
            requestIdToSender[requestId] = msg.sender;
            requestIdToTokenURI[requestId] = tokenURI;
            emit requestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address wolOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(wolOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);
        Bclass wolClass = Bclass(randomNumber % 3);
        tokenIdToBclass[newItemId] = wolClass;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved user"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}