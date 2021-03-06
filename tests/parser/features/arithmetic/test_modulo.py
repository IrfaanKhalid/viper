import pytest
from viper.exceptions import TypeMismatchException
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_modulo():
    code = """
@public
def num_modulo_num() -> num:
    return 1 % 2

@public
def decimal_modulo_decimal() -> decimal:
    return 1.5 % .33

@public
def decimal_modulo_num() -> decimal:
    return .5 % 1


@public
def num_modulo_decimal() -> decimal:
    return 1.5 % 1
"""
    c = get_contract_with_gas_estimation(code)
    assert c.num_modulo_num() == 1
    assert c.decimal_modulo_decimal() == .18
    assert c.decimal_modulo_num() == .5
    assert c.num_modulo_decimal() == .5


def test_modulo_with_different_units(assert_compile_failed):
    code = """
@public
def foo(a: currency_value, b: num):
    x = a % b
"""
    assert_compile_failed(lambda: get_contract_with_gas_estimation(code), TypeMismatchException)


def test_modulo_with_positional_input(assert_compile_failed):
    code = """
@public
def foo(a: num(sec, positional), b: num):
    x = a % b
"""
    assert_compile_failed(lambda: get_contract_with_gas_estimation(code), TypeMismatchException)


def test_modulo_with_input_of_zero(assert_tx_failed):
    code = """
@public
def foo(a: num, b: decimal) -> decimal:
    return a % b
"""
    c = get_contract_with_gas_estimation(code)
    assert_tx_failed(lambda: c.foo(1, 0))
