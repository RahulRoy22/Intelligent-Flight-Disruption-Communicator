import chromadb

# Initialize a local Chroma client. This will create a 'chroma_data' folder in your project root.
client = chromadb.PersistentClient(path="./chroma_data")

# Create a collection (think of this like a table in a standard SQL database)
# We use cosine similarity to find the most relevant rules.
collection = client.get_or_create_collection(name="airport_rules")

def seed_database():
    """
    Populates the vector database with specific airport operational rules.
    In a full production app, an Airflow pipeline would pull these from the FAA NOTAM API.
    """
    # Check if we already have data to avoid duplicate entries
    if collection.count() == 0:
        documents = [
            "KJFK RULE: If wind gusts exceed 25 knots, Runway 13L/31R must be closed due to crosswind limits, causing minor arrival delays.",
            "KJFK RULE: Visibility below 1/2 statute mile (SM) triggers Low Visibility Operations (LVP), increasing spacing between landing aircraft and causing 30-45 minute holding patterns.",
            "KJFK RULE: Heavy snow (-SN or +SN) requires snowplow operations, shutting down active runways for 20-minute intervals.",
            "KORD RULE: Freezing rain (-FZRA) at Chicago O'Hare requires mandatory de-icing at the gate, delaying departures by roughly 35 minutes."
        ]
        
        # We assign an ID to each document
        ids = ["rule_jfk_wind", "rule_jfk_vis", "rule_jfk_snow", "rule_ord_ice"]
        
        # Metadata helps us filter searches later if needed
        metadatas = [{"airport": "KJFK"}, {"airport": "KJFK"}, {"airport": "KJFK"}, {"airport": "KORD"}]
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Vector database seeded with airport rules.")

def retrieve_airport_rules(query_text: str, n_results: int = 1) -> str:
    """
    Searches the database for rules matching the current weather or disruption.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Extract the retrieved text document
    if results['documents'] and len(results['documents'][0]) > 0:
        return results['documents'][0][0]
    return "No specific operational rules found for this condition."

# Ensure the database is seeded when this module is imported
seed_database()