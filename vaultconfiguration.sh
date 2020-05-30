********************Unseal Vault**********************

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
