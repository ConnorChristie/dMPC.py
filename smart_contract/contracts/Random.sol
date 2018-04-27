pragma solidity ^0.4.18;

contract Random {
    uint256 private seed;

    constructor(uint256 _seed) public {
        seed = _seed;
    }

    function nextInt(uint256 upper) public returns (uint256 randomNumber) {
        seed = uint256(keccak256(
            seed,
            blockhash(block.number - 1),
            block.coinbase,
            block.difficulty
        ));

        return seed % upper;
    }
}