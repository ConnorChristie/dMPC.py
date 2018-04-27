const Main = artifacts.require("./MPC.sol");

module.exports = function(deployer) {
  deployer.deploy(Main);
};
