import asyncio
import time

from pytoniq_core import Address

from pytonconnect import TonConnect
from pytonconnect.exceptions import UserRejectsError

from comments import get_comment_message
from nfts import get_nft_transfer_message
from jettons import get_jetton_transfer_message, get_jetton_burn_message
from nft_sale import get_sale_body


async def main():
    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json')
    is_connected = await connector.restore_connection()
    print('is_connected:', is_connected)

    def status_changed(wallet_info):
        print('wallet_info:', wallet_info)
        unsubscribe()

    def status_error(e):
        print('connect_error:', e)

    unsubscribe = connector.on_status_change(status_changed, status_error)

    wallets_list = connector.get_wallets()
    print('wallets_list:', wallets_list)

    generated_url = await connector.connect(wallets_list[0])
    print('generated_url:', generated_url)

    print('Waiting 2 minutes to connect...')
    for i in range(120):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                print('Connected with address:', Address(wallet_address))
            break

    if connector.connected:
        print('Sending transaction...')

        transaction = {
            'valid_until': int(time.time() + 3600),
            'messages': [
                get_sale_body(
                    wallet_address=wallet_address,
                    royalty_address=wallet_address,
                    nft_address='EQDxP7tp6xc27-zj32Js6OYOKbYuMCjqEuaPusqa8owpFxR8',
                    price=int(10.5 * 10**9),
                    amount=int(1.08 * 10**9)
                ),
                # get_comment_message(
                #     destination_address='0:0000000000000000000000000000000000000000000000000000000000000000',
                #     amount=int(0.01 * 10**9),  # amount should be specified in nanocoins
                #     comment='hello world!'
                # ),
                # get_nft_transfer_message(
                #     nft_address='EQDrA-3zsJXTfGo_Vdzg8d07Da4vSdHZllc6W9qvoNoMstF-',
                #     recipient_address='0:0000000000000000000000000000000000000000000000000000000000000000',
                #     transfer_fee=int(0.07 * 10**9),
                #     response_address=wallet_address
                # ),
                # get_jetton_transfer_message(
                #     jetton_wallet_address='EQCXsVvdxTVmSIvYv4tTQoQ-0Yq9mERGTKfbsIhedbN5vTVV',
                #     recipient_address='0:0000000000000000000000000000000000000000000000000000000000000000',
                #     transfer_fee=int(0.07 * 10**9),
                #     jettons_amount=int(0.01 * 10**9),  # replace 9 for jetton decimal. For example for jUSDT it should be (amount * 10**6)
                #     response_address=wallet_address
                # ),
                # get_jetton_burn_message(
                #     jetton_wallet_address='EQCXsVvdxTVmSIvYv4tTQoQ-0Yq9mERGTKfbsIhedbN5vTVV',
                #     transfer_fee=int(0.07 * 10 ** 9),
                #     jettons_amount=int(0.01 * 10 ** 9),  # replace 9 for jetton decimal. For example for jUSDT it should be (amount * 10**6)
                #     response_address=wallet_address
                # )
            ]
        }

        try:
            result = await connector.send_transaction(transaction)
            print('Transaction was sent successfully')
            print(result)

        except Exception as e:
            if isinstance(e, UserRejectsError):
                print('You rejected the transaction')
            else:
                print('Unknown error:', e)

        print('Waiting 2 minutes to disconnect...')
        asyncio.create_task(connector.disconnect())
        for i in range(120):
            await asyncio.sleep(1)
            if not connector.connected:
                print('Disconnected')
                break

    print('App is closed')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
