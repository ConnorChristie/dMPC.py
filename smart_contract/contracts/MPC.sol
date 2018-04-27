pragma solidity ^0.4.18;

import "./DepositManager.sol";
import "./QuorumManager.sol";

contract MPC is DepositManager, QuorumManager {

    uint8 constant EXTERNAL_QUORUM_SIZE = 5;
    uint8 constant INTERNAL_QUORUM_SIZE = 3;
    uint8 constant QUORUM_SIZE = 3;//EXTERNAL_QUORUM_SIZE * INTERNAL_QUORUM_SIZE;

    event StoreData(address indexed owner, bytes32 indexed dataHash, address[] shareholders);

    function storeData(bytes32 dataHash) public {
        require(dataHash != 0x0, "Name must unique");

        bytes32 refId = keccak256(msg.sender, dataHash);

        address[] memory stakeholders = this.getActiveStakeholders();
        address[] memory quorum = this.generateQuorum(QUORUM_SIZE, stakeholders, msg.sender, refId);

        emit StoreData(msg.sender, dataHash, quorum);
    }


    // Tasks
    // Solutions
    // Verifications

    // enum State {
    //     Initialized,
    //     SolverRegistered,
    //     SolutionSubmitted
    // }

    // struct Task {
    //     address owner;
    //     uint256 difficulty;
    //     uint256 reward;
    //     bytes32 taskData;

    //     State state;
    // }

    // struct Solver {
    //     address solver;
    //     bytes32 randomHash;
    //     uint256 startBlock;

    //     bytes32[2] solutionHashes;
    // }

    // Task[] public tasks;

    // mapping (uint256 => Solver) private taskIdToSolver;

    // event TaskCreated(uint256 indexed taskId, uint256 indexed difficulty, uint256 indexed reward);
    // event SolverRegistered(uint256 taskId, address solver);
    // event SolutionSubmitted(uint256 taskId, uint256 minDeposit, bytes32 taskData, bytes32[2] solutionHashes);

    // function _owns(uint256 _taskId, address _claimant) internal view returns (bool) {
    //     return tasks[_taskId].owner == _claimant;
    // }

    // function _isState(uint256 _taskId, State _state) internal view returns (bool) {
    //     return tasks[_taskId].state == _state;
    // }

    // function _isSolver(uint256 _taskId, address _solver) internal view returns (bool) {
    //     return taskIdToSolver[_taskId].solver == _solver;
    // }

    // function _updateState(uint256 _taskId, State _state) internal returns (bool) {
    //     Task storage task = tasks[_taskId];

    //     task.state = _state;

    //     return true;
    // }

    // // Creates a new task using the supplied value as the reward
    // // @param difficulty The minimum number of blocks required to pass before solver can submit a solution
    // // @param taskData The arbitrary task data
    // function createTask(uint256 difficulty, bytes32 taskData) external payable returns (uint256) {
    //     require(difficulty > 0);
    //     require(taskData != 0x0);
    //     require(msg.value > 0);

    //     uint256 _reward = msg.value;

    //     Task memory _task = Task({
    //         owner: msg.sender,
    //         difficulty: difficulty,
    //         reward: _reward,
    //         taskData: taskData,
    //         state: State.Initialized
    //     });

    //     uint256 taskId = tasks.push(_task) - 1;

    //     emit TaskCreated(taskId, difficulty, _reward);

    //     return taskId;
    // }

    // function registerToSolve(uint256 taskId, bytes32 randomHash) external returns (bool) {
    //     require(randomHash != 0x0);
    //     require(!_owns(taskId, msg.sender));
    //     require(_isState(taskId, State.Initialized));

    //     taskIdToSolver[taskId] = Solver({
    //         solver: msg.sender,
    //         randomHash: randomHash,
    //         startBlock: block.number,
    //         solutionHashes: new bytes32[](0)
    //     });

    //     _updateState(taskId, State.SolverRegistered);

    //     emit SolverRegistered(taskId, msg.sender);

    //     return true;
    // }

    // function submitSolution(uint256 taskId, bytes32[2] solutionHashes) external returns (bool) {
    //     require(solutionHashes.length == 2);
    //     require(_isState(taskId, State.SolverRegistered));
    //     require(_isSolver(taskId, msg.sender));

    //     Task storage task = tasks[taskId];
    //     Solver storage solver = taskIdToSolver[taskId];

    //     require(block.number >= solver.startBlock + task.difficulty);

    //     solver.solutionHashes = solutionHashes;

    //     _updateState(taskId, State.SolutionSubmitted);

    //     return true;
    // }

}
