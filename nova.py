# import speech_recognition as sr
# import os
# import subprocess
# from datetime import datetime
# from common import common_list
#
#
# directory = "/Applications"
# files = os.listdir(directory)
# app_files = [file for file in files if file.endswith('.app')]
# print(app_files)
#
#
# def say(text):
#     os.system(f'say "{text}"')
# def gratting():
#     hour = int(datetime.now().hour)
#     if hour >= 9 and hour < 3:
#         say("Good Night")
#     elif hour >= 4 and hour < 12 :
#         say("Good Morning")
#     elif hour >= 12 and hour < 18 :
#         say("Good Afternoon")
#     else :
#         say("Good Evening")
# def takeCommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.pause_threshold = 0.5
#         audio = r.listen(source)
#         try:
#             print("Recognizing...")
#             query = r.recognize_google(audio, language="en-in")
#
#             print(f"User said: {query}")
#             return query
#         except Exception as e:
#             return "joor thi bol topaa"
#
# if __name__ == "__main__":
#     print("hii dhruvil")
#     gratting()
#     say("hii am nova a.i")
#
#     while True :
#         print("listting")
#         get_speech = takeCommand()
#         say(get_speech)
#
#
#         for directory in app_files:
#             directory = directory
#             if directory.strip().lower() in get_speech.lower():
#                 # print(os)
#                 # os.system(f"open ~/System/Applications/{directory}.app")
#                 subprocess.run(["open" ,f"/System/Applications/WhatsApp.app"])
#                 print(f"open /System/Applications/{directory}.app")
#
# subprocess.run(["open","Applications/Keynote.app"])






# import asyncio
# import json
# from websockets import connect
# import websockets
# # Replace with your desired subscription type (e.g., "unconfirmed_sub", "blocks_sub")
# subscription_type = "unconfirmed_sub"  # Subscribe to unconfirmed transactions
#
# async def connect_and_subscribe(url, message):
#     async with websockets.connect(url) as websocket:
#         await websocket.send(message)  # Send subscription message
#         print(f"Subscribed to {subscription_type}")
#
#         async for message in websocket:
#             data = json.loads(message)
#             # Handle incoming messages based on their "op" field
#             if data["op"] == "utx":  # Unconfirmed transaction
#                 print("New Unconfirmed Transaction:")
#                 print(json.dumps(data["x"], indent=4))
#             elif data["op"] == "block":  # New block
#                 print("New Block:")
#                 print(json.dumps(data["x"], indent=4))
#             else:
#                 print(f"Received unknown message: {message}")
#
# if __name__ == "__main__":
#     url = "wss://ws.blockchain.info/inv"
#     subscription_message = json.dumps({"op": subscription_type})
#     asyncio.run(connect_and_subscribe(url, subscription_message))


import asyncio
import pandas as pd
import streamlit as st
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport



async def run_subscription():
    # Setup WebSocket connection
    transport = WebsocketsTransport(
        url="wss://streaming.bitquery.io/eap?token=<YOUR TOKEN HERE>",
        headers={"Sec-WebSocket-Protocol": "graphql-ws"}
    )

    # Establish the connection
    await transport.connect()
    print("Connected to WebSocket")

    page = st.sidebar.radio("Select Page", ["General", "Raydium"])
    general_df = pd.DataFrame()
    raydium_df = pd.DataFrame()

    if page == "General":
        st.subheader("General Table")
        table = st.table(general_df)
        while True:
            async for result in transport.subscribe(
                gql("""
                subscription {
                    Solana {
                        General: DEXTradeByTokens {
                            Block { Time }
                            Trade {
                                Amount
                                Price
                                Currency { Symbol Name }
                                Side { Amount Currency { Symbol Name MetadataAddress }}
                                Dex { ProgramAddress ProtocolFamily ProtocolName }
                                Market { MarketAddress }
                                Order { LimitAmount LimitPrice OrderId }
                                PriceInUSD
                            }
                        }
                    }
                }
                """)
            ):
                if result.data:
                    new_data = pd.json_normalize(result.data['Solana']['General'])
                    general_df = pd.concat([general_df, new_data], ignore_index=True)
                    with st.spinner('Updating data...'):
                        table.table(general_df)
    elif page == "Raydium":
        st.subheader("Raydium Table")
        table = st.table(raydium_df)
        while True:
            async for result in transport.subscribe(
                    gql("""
                    subscription {
                        Solana {
                            Raydium: DEXTrades(
                                where: {Trade: {Dex: {ProgramAddress: {is: "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"}}}}
                            ) {
                                Trade {
                                    Dex { ProgramAddress ProtocolName }
                                    Buy {
                                        Account { Address }
                                        Amount
                                        Currency { Symbol Name }
                                        PriceInUSD
                                    }
                                    Sell {
                                        Account { Address }
                                        Amount
                                        Currency { Symbol Name }
                                        PriceInUSD
                                    }
                                }
                                Block { Time Height }
                                Transaction { Signature }
                            }
                        }
                    }
                    """)
            ):
                if result.data:
                    new_data = pd.json_normalize(result.data['Solana']['Raydium'])
                    raydium_df = pd.concat([raydium_df, new_data], ignore_index=True)
                    with st.spinner('Updating data...'):
                        table.table(raydium_df)


def main():
    st.title("Solana DEX General & Raydium Data Dashboard")
    asyncio.run(run_subscription())

if __name__ == "__main__":
    main()