from __future__ import annotations
from argparse import ArgumentParser
from decimal import Decimal
from typing import Optional

STOCK_PERCENTAGE = 95


class Args:

    def __init__(self):
        self.parser = self.create_arg_parser()
        self.account_balance: Optional[float] = None
        self.deposit_amount: Optional[float] = None
        self.fzrox_amount: Optional[float] = None
        self.fxnax_amount: Optional[float] = None

        self.add_args_to_parser()

    @staticmethod
    def create_arg_parser() -> ArgumentParser:
        return ArgumentParser(
            description=(f'Calculates deposit amounts for my FZROX and FXNAX '
                         f'positions to keep the account balanced '
                         f'at {STOCK_PERCENTAGE}% and {100 - STOCK_PERCENTAGE}'
                         f'respectively.'),
            add_help=True
        )

    def add_args_to_parser(self) -> None:
        self.parser.add_argument('account_balance', type=float,
                                 help='The total balance of the roth account')
        self.parser.add_argument('deposit_amount', type=float,
                                 help='The amount that has recently been ' +
                                      'deposited')
        self.parser.add_argument('fzrox_amount', type=float,
                                 help='The amount in the FZROX position')
        self.parser.add_argument('fxnax_amount', type=float,
                                 help='The amount in the FXNAX position')

    def parse(self) -> Args:
        self.parser.parse_args(namespace=self)
        return self


class BalancesCalculator:

    def __init__(self, args: Args):
        self._account_balance: float = args.account_balance
        self._fzrox_balance: float = args.fzrox_amount
        self._fxnax_balance: float = args.fxnax_amount
        self.check_sum_of_balances()
        self._deposit_amount: float = args.deposit_amount
        self._balance_after_deposit = self._account_balance + \
                                      self._deposit_amount
        self.deposit_insufficient_to_balance = False
        self._fzrox_percentage: float = STOCK_PERCENTAGE / 100
        self._fxnax_percentage: float = 1 - self._fzrox_percentage
        self._target_fzrox_amount = self._balance_after_deposit * \
                                    self._fzrox_percentage
        self._target_fxnax_amount = self._balance_after_deposit * \
                                    self._fxnax_percentage
        self._to_fzrox: float = self.get_fzrox_amount()
        self._to_fxnax: float = self.get_fxnax_amount()

    def check_sum_of_balances(self):
        if Decimal(str(self._fzrox_balance)) + Decimal(
                str(self._fxnax_balance)) != Decimal(
                str(self._account_balance)):
            raise ValueError(
                'The FZROX and FXNAX balances must sum to the account balance:'
                f' {self.get_fzrox_balance_string()} + '
                f'{self.get_fxnax_balance_string()} != '
                f'{self.get_account_balance_string()}')

    def get_fzrox_amount(self) -> float:
        target: float = (self._account_balance + self._deposit_amount) * \
                        self._fzrox_percentage
        diff: float = target - self._fzrox_balance
        if self._deposit_amount < diff:
            self.deposit_insufficient_to_balance = True
        return diff

    def get_fxnax_amount(self) -> float:
        target: float = (self._account_balance + self._deposit_amount) * \
                        self._fxnax_percentage
        diff: float = target - self._fxnax_balance
        if self._deposit_amount < diff:
            self.deposit_insufficient_to_balance = True
        return diff

    def get_account_balance_string(self) -> str:
        return '${:.2f}'.format(self._account_balance)

    def get_fzrox_balance_string(self) -> str:
        return '${:.2f}'.format(self._fzrox_balance)

    def get_fxnax_balance_string(self) -> str:
        return '${:.2f}'.format(self._fxnax_balance)

    def get_deposit_amount_string(self) -> str:
        return '${:.2f}'.format(self._deposit_amount)

    def get_balance_after_deposit_string(self) -> str:
        return '${:.2f}'.format(self._balance_after_deposit)

    def get_target_fzrox_amount_string(self) -> str:
        return '${:.2f}'.format(self._target_fzrox_amount)

    def get_target_fxnax_amount_string(self) -> str:
        return '${:.2f}'.format(self._target_fxnax_amount)

    def get_amount_to_fzrox_string(self) -> str:
        return '${:.2f}'.format(self._to_fzrox)

    def get_amount_to_fxnax_string(self) -> str:
        return '${:.2f}'.format(self._to_fxnax)

    def get_fzrox_percentage_string(self) -> str:
        return '{:.0f}%'.format(self._fzrox_percentage * 100)

    def get_fxnax_percentage_string(self) -> str:
        return '{:.0f}%'.format(self._fxnax_percentage * 100)


class Output:

    def __init__(self, balances: BalancesCalculator):
        self.balances = balances

    def get(self) -> str:
        if self.balances.deposit_insufficient_to_balance:
            return self._create_summary() + \
                   self._get_insufficient_deposit_amounts()
        else:
            return self._create_summary() + \
                   self._get_sufficient_deposit_amounts()

    def _create_summary(self) -> str:
        return ('\n-----'
                f'\nDeposit: {self.balances.get_deposit_amount_string()}'
                '\n-----'
                '\nCurrent Balance: '
                f'{self.balances.get_account_balance_string()}'
                f'\nFZROX Balance: {self.balances.get_fzrox_balance_string()}'
                f'\nFXNAX Balance: {self.balances.get_fxnax_balance_string()}'
                '\n-----'
                '\nTarget Percentages:'
                f'\n\tFZROX: {self.balances.get_fzrox_percentage_string()}'
                f'\n\tFXNAX: {self.balances.get_fxnax_percentage_string()}'
                '\n-----')

    def _get_sufficient_deposit_amounts(self) -> str:
        return ('\nDeposit Amounts:'
                f'\n\t{self.balances.get_amount_to_fzrox_string()} -> FZROX'
                f'\n\t{self.balances.get_amount_to_fxnax_string()} -> FXNAX')

    def _get_insufficient_deposit_amounts(self) -> str:
        return (
            '\nDEPOSIT INSUFFICIENT TO REBALANCE ACCOUNT. REBALANCE MANUALLY.'
            '\nTargets:'
            '\nAccount Balance after Deposit: '
            f'{self.balances.get_balance_after_deposit_string()}'
            '\nFZROX Balance after Deposit: '
            f'{self.balances.get_target_fzrox_amount_string()}'
            '\nFXNAX Balance after Deposit: '
            f'{self.balances.get_target_fxnax_amount_string()}')


def main():
    args = Args().parse()
    balances = BalancesCalculator(args)
    print(Output(balances).get())
    return


if __name__ == '__main__':
    main()
