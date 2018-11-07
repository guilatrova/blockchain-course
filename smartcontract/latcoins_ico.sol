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

    function equity_in_latcoins(address investor) external constant returns (uint) {
        return equity_latcoins[investor];
    }

    function equity_in_usd(address investor) external constant returns (uint) {
        return equity_usd[investor];
    }

    function buy_latcoins(address investor, uint usd_invested) external
    can_buy_latcoins(usd_invested) {
        uint latcoins_bought = usd_invested * usd_to_latcoins;

        equity_latcoins[investor] += latcoins_bought;
        equity_usd[investor] = equity_latcoins[investor] / usd_to_latcoins;
        total_latcoins_bought += latcoins_bought;
    }

    function sell_latcoins(address investor, uint latcoins_sold) external {
        equity_latcoins[investor] -= latcoins_sold;
        equity_usd[investor] = equity_latcoins[investor] / usd_to_latcoins;
        total_latcoins_bought -= latcoins_sold;
    }
}
