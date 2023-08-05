from pytoniq_core import begin_cell
from base64 import urlsafe_b64encode


def get_nft_transfer_message(nft_address: str, recipient_address: str, transfer_fee: int, response_address: str = None) -> dict:
    data = {
        'address': nft_address,
        'amount': str(transfer_fee),
        'payload': urlsafe_b64encode(
            begin_cell()
            .store_uint(0x5fcc3d14, 32)  # op code for nft transfer message
            .store_uint(0, 64)  # query_id
            .store_address(recipient_address)  # new owner
            .store_address(response_address or response_address)  # address send excess to
            .store_uint(0, 1)  # custom payload
            .store_coins(1)  # forward amount
            .store_uint(0, 1)  # forward payload
            .end_cell()  # end cell
            .to_boc()  # convert it to boc
        )
        .decode()  # encode it to urlsafe base64
    }


    return data
