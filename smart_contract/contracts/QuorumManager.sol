pragma solidity ^0.4.18;

import "./DepositManager.sol";
import "./Random.sol";

contract QuorumManager {

    Random private random;

    struct Quorum {
        address[] shareholders;
    }

    struct DataRef {
        address owner;
        bytes32 refId;
        uint256 createdBlock;
        uint256 lastUpdatedBlock;

        Quorum quorum;
    }

    mapping (bytes32 => DataRef) public dataRefs;

    constructor() public {
        random = new Random(uint256(blockhash(block.number - 1)));
    }

    function generateQuorum(uint8 size, address[] population, address owner, bytes32 refId) public returns (address[]) {
        require(size > 0, "Size should be positive");
        require(population.length >= size, "Population should be larger than quorum size");

        Quorum memory _quorum = Quorum({
            shareholders: new address[](size)
        });

        uint8 index = 0;

        while (index < size) {
            address member = population[random.nextInt(population.length)];

            if (!_inQuorum(member, _quorum)) {
                _quorum.shareholders[index++] = member;
            }
        }

        DataRef memory _ref = DataRef({
            owner: owner,
            refId: refId,
            createdBlock: block.number,
            lastUpdatedBlock: block.number,
            quorum: _quorum
        });

        dataRefs[refId] = _ref;

        return _quorum.shareholders;
    }

    function _inQuorum(address who, Quorum quorum) private pure returns (bool) {
        for (uint8 i = 0; i < quorum.shareholders.length; i++) {
            if (quorum.shareholders[i] == who) {
                return true;
            }
        }

        return false;
    }

    // function generateQuorum(uint8 size, address[] population) public returns (address[]) {
    //     require(size > 0, "Size should be positive");
    //     require(population.length >= size, "Population should be larger than quorum size");

    //     bool[] memory included = new bool[](size);
    //     address[] memory quorum = new address[](size);

    //     uint8 index = 0;

    //     while (quorum.length < size) {
    //         address member = population[random.nextInt(population.length)];
    //         uint160 addressInt = uint160(member);

    //         if (!included[addressInt]) {
    //             included[addressInt] = true;
    //             quorum[index++] = member;
    //         }
    //     }

    //     return quorum;
    // }

}