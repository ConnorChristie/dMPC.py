const MPC = artifacts.require('./MPC.sol');
const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

contract('MPC', function (accounts) {
    let main;

    const owner = accounts[1];
    const solver = accounts[2];
    const verifier = accounts[3];

    context('deposit layer', () => {

        before(async () => {
            main = await MPC.deployed();
        });

        // it('should deposit', async () => {
        //     let deposit = web3.utils.toWei('1', 'ether');

        //     let tx = await main.deposit(
        //         { from: owner, value: deposit }
        //     );

        //     log = tx.logs.find(log => log.event === 'Deposit');

        //     assert.equal(log.args.stakeholder, owner);
        //     assert(log.args.amount.eq(deposit));
        // });

        // it('should get active stakeholders', async () => {
        //     let deposit = web3.utils.toWei('2', 'ether');
        //     let index = 0;

        //     for (let address of accounts) {
        //         await main.deposit(
        //             { from: address, value: deposit }
        //         );

        //         if (index > accounts.length / 2) {
        //             deposit = web3.utils.toWei('0.5', 'ether');
        //         }

        //         index++;
        //     }

        //     let activeNodes = await main.getActiveStakeholders();

        //     assert.equal(activeNodes.length, 7);
        // });

        it('should get active stakeholders', async () => {
            let deposit = web3.utils.toWei('2', 'ether');
            let index = 0;

            for (let address of accounts) {
                await main.deposit(
                    { from: address, value: deposit }
                );

                if (index > accounts.length / 2) {
                    deposit = web3.utils.toWei('0.5', 'ether');
                }

                index++;
            }

            let tx = await main.storeData(12345);
            let logs = tx.logs.find(log => log.event === 'StoreData');

            console.log(logs);
        });
    });
});
