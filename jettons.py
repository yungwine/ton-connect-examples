from pytoniq_core import begin_cell
from base64 import urlsafe_b64encode


def get_jetton_transfer_message(jetton_wallet_address: str, recipient_address: str, transfer_fee: int, jettons_amount: int) -> dict:
    data = {
        'address': jetton_wallet_address,
        'amount': str(transfer_fee),
        'payload': urlsafe_b64encode(
            begin_cell()
            .store_uint(0xf8a7ea5, 32)  # op code for jetton transfer message
            .store_uint(0, 64)  # query_id
            .store_coins(jettons_amount)
            .store_address(recipient_address)  # destination address
            .store_address(recipient_address)  # address send notification to
            .store_uint(0, 1)  # custom payload
            .store_coins(1)  # forward amount
            .store_uint(0, 1)  # forward payload
            .end_cell()  # end cell
            .to_boc()  # convert it to boc
        )
        .decode()  # encode it to urlsafe base64
    }

    return data


def get_jetton_burn_message(jetton_wallet_address: str, transfer_fee: int, jettons_amount: int, response_address=None) -> dict:
    data = {
        'address': jetton_wallet_address,
        'amount': str(transfer_fee),
        'payload': urlsafe_b64encode(
            begin_cell()
            .store_uint(0x595f07bc, 32)  # op code for jetton transfer message
            .store_uint(0, 64)  # query_id
            .store_coins(jettons_amount)
            .store_address(response_address)  # address send notification to
            .end_cell()  # end cell
            .to_boc()  # convert it to boc
        )
        .decode()  # encode it to urlsafe base64
    }

    return data

