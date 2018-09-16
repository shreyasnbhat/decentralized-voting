var voting = artifacts.require("./VotingContract.sol");
var candidateNames = ["Shreyas","Sudeep","Aditya","Yash"];

module.exports = function(deployer) {
  deployer.deploy(voting,candidateNames,4, {from:web3.eth.accounts[0], value:web3.toWei(15,'ether')});
}
