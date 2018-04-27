const fs = require('fs');
const MPC = artifacts.require("./MPC.sol");

module.exports = (deployer, network) => {
  let exportedContracts = {}

  let contracts = [MPC]

  contracts.forEach((contract) => {

    exportedContracts[contract.contractName] = {
      abi: contract.abi,
      address: contract.address
    }
  })

  if (!fs.existsSync(__dirname + "/../export/")){
    fs.mkdirSync(__dirname + "/../export/")
  }

  let path = __dirname + "/../export/" + network+ ".json"

  fs.writeFile(path, JSON.stringify(exportedContracts), (e) => {if(e) console.error(e) })
}