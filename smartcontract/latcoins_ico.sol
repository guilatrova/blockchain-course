pragma solidity ^0.4.11;

contract latcoin_ico {

    uint public max_latcoins = 1000000;
    uint public usd_to_latcoins = 1000;
    uint public total_latcoins_bought = 0;

    mapping(address => uint) equity_latcoins;
    mapping(address => uint) equity_usd;

    modifier can_buy_latcoins(uint usd_invested) {
        require (usd_invested * usd_to_latcoins + total_latcoins_bought <= max_latcoins);
        _;
    }
}
