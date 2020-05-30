********************Vault Setup**********************
Only if EC2 instance public IP changes.

Check the status of consul
-----------
sudo systemctl status consul

If not started start it
------------
sudo systemctl start consul

Since when we restart the  public ip’s get changed so wee have to change ip’s in thee vault config flies as well
Now, open config.hcl file in /etc/vault/ 
------------
sudo vi /etc/vault/config.hcl

-----
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
}

listener "tcp" {
 address     = "0.0.0.0:8200"
 tls_disable = 1
}                                 (replace the new ip with the old ones)
api_addr = "https://10.206.1.198:8200"
ui = true

-----

Save and exit

Now,
sudo systemctl daemon-reload
sudo systemctl restart vault
sudo systemctl status vault

Make sure the vault is running  and now the vault will be in sealed state so unseal it

And access using new ip:8200

*******************UnSeal Vault with below commands*************

vault operator unseal 0ECTrSYfTgQBfRAsyR77d1ctJskyyFjJDeWu+yvc+clD
vault operator unseal 0ECTrSYfTgQBfRAsyR77d1ctJskyyFjJDeWu+yvc+clD
vault operator unseal S4aI0jwrsShUZR4TSDdRQ1sFRObw8rWCu8zUBskgtf9W

*******************Create Cassandra secrets for connection*****************************
vault secrets enable database

vault write database/config/my-cassandra-database \
    plugin_name="cassandra-database-plugin" \
    hosts=100.25.10.11\
    protocol_version=4 \
    username=cassandra \
    password=cassandra \
    allowed_roles=my-role
    
vault write database/roles/my-role \
    db_name=my-cassandra-database \
    creation_statements="CREATE USER '{{username}}' WITH PASSWORD '{{password}}' NOSUPERUSER; \
          GRANT SELECT ON ALL KEYSPACES TO {{username}};" \
    default_ttl="1h" \
    max_ttl="24h"
