vault secrets enable database

vault write database/config/my-cassandra-database \
    plugin_name="cassandra-database-plugin" \
    hosts=100.25.10.11\
    protocol_version=4 \
    username=cassandra \
    password=cassandra \
    allowed_roles=my-role
