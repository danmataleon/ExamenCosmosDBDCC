from azure.cosmos import CosmosClient

# Datos de conexión de Cosmos DB
COSMOS_DB_URL = "https://acdbdccdev.documents.azure.com:443/"
COSMOS_DB_KEY = "bb6SpeJq6un7wNZh2Yan88WrFtYWka4NU86U670ph3sMCjdy9SoYB0ozaXWmBgsZTubLp2MmWd9yACDb9m2xWA=="
DATABASE_NAME = "GestorProyectosDB"
USERS_CONTAINER = "Usuarios"
PROJECTS_CONTAINER = "Proyectos"

# Conexión a Cosmos DB
client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)

# base de datos
try:
    database = client.create_database_if_not_exists(DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

#contenedores
try:
    users_container = database.create_container_if_not_exists(
        id=USERS_CONTAINER, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    users_container = database.get_container_client(USERS_CONTAINER)

try:
    projects_container = database.create_container_if_not_exists(
        id=PROJECTS_CONTAINER, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400)
except exceptions.CosmosResourceExistsError:
    projects_container = database.get_container_client(PROJECTS_CONTAINER)