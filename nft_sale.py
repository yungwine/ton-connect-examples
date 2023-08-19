import time
from base64 import urlsafe_b64encode

from pytoniq_core.boc import Cell, begin_cell, Address
from pytoniq_core.tlb import StateInit


def get_sale_body(wallet_address: str, royalty_address: str, nft_address: str, price: int, amount: int):

    # contract code
    nft_sale_code_cell = Cell.one_from_boc('te6cckECCwEAArkAART/APSkE/S88sgLAQIBIAIDAgFIBAUAfvIw7UTQ0wDTH/pA+kD6QPoA1NMAMMABjh34AHAHyMsAFssfUATPFljPFgHPFgH6AszLAMntVOBfB4IA//7y8AICzQYHAFegOFnaiaGmAaY/9IH0gfSB9AGppgBgYaH0gfQB9IH0AGEEIIySsKAVgAKrAQH30A6GmBgLjYSS+CcH0gGHaiaGmAaY/9IH0gfSB9AGppgBgYOCmE44BgAEqYhOmPhW8Q4YBKGATpn8cIxbMbC3MbK2QV44LJOZlvKAVxFWAAyS+G8BJrpOEBFcCBFd0VYACRWdjYKdxjgthOjq+G6hhoaYPqGAD9gHAU4ADAgB92YIQO5rKAFJgoFIwvvLhwiTQ+kD6APpA+gAwU5KhIaFQh6EWoFKQcIAQyMsFUAPPFgH6AstqyXH7ACXCACXXScICsI4XUEVwgBDIywVQA88WAfoCy2rJcfsAECOSNDTiWnCAEMjLBVADzxYB+gLLaslx+wBwIIIQX8w9FIKAejy0ZSzjkIxMzk5U1LHBZJfCeBRUccF8uH0ghAFE42RFrry4fUD+kAwRlAQNFlwB8jLABbLH1AEzxZYzxYBzxYB+gLMywDJ7VTgMDcowAPjAijAAJw2NxA4R2UUQzBw8AXgCMACmFVEECQQI/AF4F8KhA/y8AkA1Dg5ghA7msoAGL7y4clTRscFUVLHBRWx8uHKcCCCEF/MPRQhgBDIywUozxYh+gLLassfFcs/J88WJ88WFMoAI/oCE8oAyYMG+wBxUGZFFQRwB8jLABbLH1AEzxZYzxYBzxYB+gLMywDJ7VQAlsjLHxPLPyPPFlADzxbKAIIJycOA+gLKAMlxgBjIywUmzxZw+gLLaszJgwb7AHFVUHAHyMsAFssfUATPFljPFgHPFgH6AszLAMntVNZeZYk=')

    # fees cell

    marketplace_address = Address('EQBYTuYbLf8INxFtD8tQeNk5ZLy-nAX9ahQbG_yl1qQ-GEMS')
    marketplace_fee_address = Address('EQCjk1hh952vWaE9bRguFkAhDAL5jj3xj9p0uPWrFBq_GEMS')
    destination_address = Address('EQAIFunALREOeQ99syMbO6sSzM_Fa1RsPD5TBoS0qVeKQ-AR')

    wallet_address = Address(wallet_address)
    royalty_address = Address(royalty_address)
    nft_address = Address(nft_address)

    marketplace_fee = int(price * 5 / 100)  # 5%
    royalty_fee = int(price * 5 / 100)  # 5%

    fees_data_cell = (begin_cell()
                      .store_address(marketplace_fee_address)
                      .store_coins(marketplace_fee)
                      .store_address(royalty_address)
                      .store_coins(royalty_fee)
                      .end_cell())


    sale_data_cell = (begin_cell()
                      .store_bit_int(0)
                      .store_uint(int(time.time()), 32)
                      .store_address(marketplace_address)
                      .store_address(nft_address)
                      .store_address(wallet_address)
                      .store_coins(price)
                      .store_ref(fees_data_cell)
                      .store_bit_int(0)
                      .end_cell())

    state_init_cell = StateInit(code=nft_sale_code_cell, data=sale_data_cell).serialize()

    sale_body = (begin_cell()
                 .store_uint(1, 32)
                 .store_uint(0, 64)
                 .end_cell())

    transfer_nft_body = (begin_cell()
                         .store_uint(0x5fcc3d14, 32)
                         .store_uint(0, 64)
                         .store_address(destination_address)
                         .store_address(wallet_address)
                         .store_bit_int(0)
                         .store_coins(int(1 * 10**9))
                         .store_bit_int(0)
                         .store_uint(0x0fe0ede, 31)
                         .store_ref(state_init_cell)
                         .store_ref(sale_body)
                         .end_cell())

    data = {
        'address': nft_address.to_str(),
        'amount': str(amount),
        'payload': urlsafe_b64encode(transfer_nft_body.to_boc()).decode()
    }

    return data
