from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair
from solathon.utils import clean_response, lamport_to_sol, sol_to_lamport
from datetime import datetime, timedelta
import time
import secrets
import random

# Correct RPC endpoint for devnet
client = Client("https://api.devnet.solana.com")

def getbal(sender):
    balance = client.get_balance(sender)
    tosol = lamport_to_sol(balance)
    print("Your Balance : ", tosol, "SOL")
    print("")

def tx_sol(sender, keysender, receiver, value):
    instruction = transfer(
        from_public_key=sender,
        to_public_key=receiver,
        lamports=int(value)
    )

    transaction = Transaction(instructions=[instruction], signers=[keysender])

    result = client.send_transaction(transaction)
    print(sender, " Send ", lamport_to_sol(value), " SOL To ", receiver)
    print("Transaction ID : ", result)
    getbal(sender)
    print("Transaction Will Continue For 3 Second...")
    time.sleep(3)

def wait_until_time(hour, minute):
    now = datetime.utcnow()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if now > target:
        target += timedelta(days=1)

    while True:
        now = datetime.utcnow()
        time_to_wait = (target - now).total_seconds()

        if time_to_wait <= 0:
            break

        hours, remainder = divmod(time_to_wait, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Time until {target.strftime('%H:%M:%S')} UTC: {int(hours):02}:{int(minutes):02}:{int(seconds):02}", end='\r')
        time.sleep(1)
    
    print(f"\nReached {target.strftime('%H:%M:%S')} UTC. Starting transactions...")

print("Auto Send Random Solana To Random Address")
loop = input("How Many You Want To Transaction? : ")

wait_until_time(0, 5)

for i in range(0, int(loop)):
    with open('keylist.txt', 'r') as file:
        local_data = file.read().splitlines()
        for pvkeylist in local_data:
            keysender = Keypair().from_private_key(pvkeylist)
            sender = keysender.public_key
            keyreceiver = Keypair()  # generate random pvkey
            receiver = keyreceiver.public_key
            inputval = random.uniform(0.001, 0.0011)
            value = sol_to_lamport(inputval)
            tx_sol(sender, keysender, receiver, value)
