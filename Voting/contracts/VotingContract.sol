pragma solidity ^0.4.22;

contract VotingContract {

  mapping (bytes32 => uint8) public votesReceived;

  bytes32[] public candidateList;
  uint public candidateCount;

  constructor (bytes32[] candidateNames, uint count) public {
    candidateList = candidateNames;
    candidateCount = count;
  }

  function getCandidate(uint index) view public returns (bytes32) {
    return candidateList[index];
  }

  function getCandidates() view public returns(bytes32[]) {
    return candidateList;
  }

  function totalVotesFor(bytes32 candidate) view public returns (uint8) {
    require(validCandidate(candidate));
    return votesReceived[candidate];
  }


  function voteForCandidate(bytes32 candidate) public {
    require(validCandidate(candidate));
    votesReceived[candidate] += 1;
  }

  function validCandidate(bytes32 candidate) view public returns (bool) {
    for(uint i = 0; i < candidateList.length; i++) {
      if (candidateList[i] == candidate) {
        return true;
      }
    }
    return false;
  }
}
