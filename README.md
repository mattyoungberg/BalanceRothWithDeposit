# Balance Roth with Deposit
#### A simple utility script to help me allocate funds correctly when I'm contributing to my Roth IRA.

----

I hold two positions in the FZROX and FXNAX mutual funds from Fidelity for one of my retirement accounts to which I contribute often. The script is configured to calculate numbers for those two funds based on the percentage I want to hold in FZROX (stock). That percentage, 95%, is a global variable at the top of the script.

This script is useful because as shares in the funds fluctuate in value, the 95%-5% balance disappears since FZROX's value is more volatile. Simply splitting my deposit in a 95-5% split won't help my positions re-converge, but with some math, the amounts I need to contribute to each to rebalance are simple enough to obtain. Doing these calculations by hand is possible, but can take 5-10 minutes to figure, and requires getting out pencil and paper. So, I spent an hour writing this utility script to simply do the calculations for me, since it will likely serve me for some years to come.

The script takes command line arguments and can be run like this from your command line or terminal:

```
C:\path\to\python.exe balance_roth_with_deposit.py 245.20 80.34 235.96 9.24
```

##### Positional Arguments:

- Total Balance of the account (245.20)
- Amount to deposit (80.34)
- Balance of position in FZROX (233.09)
- Balance of position in FXNAX (12.11)

It then performs a variety of calculations, and will spit out an output comparable to this:

```
-----
Deposit: $80.34
-----
Current Balance: $245.20
FZROX Balance: $235.96
FXNAX Balance: $9.24
-----
Target Percentages:
	FZROX: 95%
	FXNAX: 5%
-----
Deposit Amounts:
	$73.30 -> FZROX
	$7.04 -> FXNAX
```

This script also performs some validity checks in the background, and can handle the situation when the deposit isn't sufficient to bring the account to a perfect 95-5% balance by providing you target values for your account balance and position balances.

----
Directions on how to use the script can also be seen by using the `-h` command line argument.