from eth_account import Account

def create_keystore(password: str):
    account = Account.create()
    print(account)
    keystore_json = Account.encrypt(account.key, password)
    return keystore_json

# Example usage
password = 'tJ1zu9Y4nCP'
keyfile = create_keystore(password)

# Print the generated keyfile
print(keyfile)