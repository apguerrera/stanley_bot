pragma solidity ^0.4.11;

contract myToken is MintableToken {
    mapping(address => uint256) balances;
    uint256 public totalSupply;
    string public constant name = "Adriano";
    uint8 public decimals = 18;
    string public constant symbol = 'ADR';
    bool public transferAllowed;

    function MyToken() {
        balances[msg.sender] = 10;
        totalSupply = 10;
        // mint(msg.sender,10);
    }


    function balanceOf(address a) constant returns (uint256) {
        return balances[a];
    }

    function mint(address a, uint256 amount) {
        balances[a] += amount;
        totalSupply += amount;
    }

    function transfer(address to, uint256 amount) returns(bool) {
        if(balances[msg.sender] >= amount && amount > 0 && balances[to] + amount > balances[to]) {
            balances[msg.sender] -= amount;
            balances[to] += amount;
            return true;
        }
        return false;
    }



    function newTokens () payable {
        uint256 tokens = msg.value * 10;
        mint(msg.sender, tokens);
    }
}
