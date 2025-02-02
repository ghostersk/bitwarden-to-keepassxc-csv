# bitwarden-to-keepassxc-csv
Export Vaultwarden vault as CSV to Keepassxc application
This is cimple python script, what will take unecrypted VaultWarden vault in CSV format and converts it to format what KeepassXC understands.
- This was<b> not tested on Bitwarden - only VaultWarden, I am not sure if there is different layout</b>
- If Vaultwarden record has multiple URL's it will create the record for each URL (as currently I do not see any way to add multiple URL using Import to KeepassXC) this is possible manually from the app.
- if you mark the file executable, you can run it .\convertor.py
- otherwise you need to run it as python <b>convertor.py <exported vaultwarden vault.csv> <keepasxc import.csv></b>
- if second argument not provided, it will create file in current directory: "keepassxc-import.csv"
- <b>This code also imports TOTP, by extracting the secret value.</b>
