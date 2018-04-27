pragma solidity ^0.4.18;

contract DepositManager {

    uint256 constant MIN_DEPOSIT = 1 ether;

    struct Stakeholder {
        uint256 balance;
        bool active;
        bool exists;
    }

    mapping (address => Stakeholder) public stakeholders;

    address[] private indexToStakeholder;
    uint256 private activeStakeholders;

    event Deposit(address stakeholder, uint256 amount, bool active);
    event Withdraw(address stakeholder, uint256 amount, bool active);

    function deposit() external payable returns (uint256) {
        Stakeholder storage stakeholder = stakeholders[msg.sender];
        stakeholder.balance += msg.value;

        if (!stakeholder.exists) {
            indexToStakeholder.push(msg.sender);
            stakeholder.exists = true;
        }

        if (!stakeholder.active && stakeholder.balance >= MIN_DEPOSIT) {
            stakeholder.active = true;
            activeStakeholders++;
        }

        emit Deposit(msg.sender, msg.value, stakeholder.active);

        return stakeholder.balance;
    }

    function withdraw(uint256 amount) external returns (uint256) {
        Stakeholder storage stakeholder = stakeholders[msg.sender];
        require(stakeholder.balance >= amount);

        stakeholder.balance -= amount;

        if (stakeholder.active && stakeholder.balance < MIN_DEPOSIT) {
            stakeholder.active = false;
            activeStakeholders--;
        }

        msg.sender.transfer(amount);

        emit Withdraw(msg.sender, amount, stakeholder.active);

        return stakeholder.balance;
    }

    function getActiveStakeholders() public view returns (address[]) {
        require(activeStakeholders > 0);

        address[] memory active = new address[](activeStakeholders);
        uint256 index = 0;

        for (uint256 i = 0; i < indexToStakeholder.length; i++) {
            address stakeholderAddress = indexToStakeholder[i];
            Stakeholder storage stakeholder = stakeholders[stakeholderAddress];

            if (stakeholder.active && stakeholder.exists) {
                active[index++] = stakeholderAddress;
            }
        }

        return active;
    }

    function() public payable { }

}
