var voting = artifacts.require("./VotingContract.sol");
var candidateNames = ["Shreyas","Sudeep","Aditya","Yash"];

module.exports = function(deployer) {
  deployer.deploy(voting,candidateNames,4);
}
