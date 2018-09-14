pragma solidity ^0.4.22;

contract Counter {

  uint256 private count;

  constructor(uint256 _count) public{
    count = _count;
  }

  function increment() public {
    count += 1;
  }

  function getValue() public view returns(uint256) {
    return count;
  }

}
