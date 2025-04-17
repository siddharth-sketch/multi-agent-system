import sqlite3

def create_token_tracking_table():
    """
    Creates a table to track LLM token usage across different agents and nodes
    """
    conn = sqlite3.connect('token_tracking.db')
    cursor = conn.cursor()
    
    # Create table for token tracking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS token_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_query TEXT NOT NULL,
        agent_name TEXT NOT NULL,
        node_name TEXT NOT NULL, 
        input_token INTEGER NOT NULL,
        output_token INTEGER NOT NULL,
        total_token INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def insert_token_tracking(user_query: str, agent_name: str, node_name: str, 
                         input_token: int, output_token: int, total_token: int):
    """
    Inserts token tracking data into the token_tracking table
    
    Args:
        user_query (str): The user's input query
        agent_name (str): Name of the agent processing the query
        node_name (str): Name of the specific node within the agent
        input_token (int): Number of input tokens used
        output_token (int): Number of output tokens used 
        total_token (int): Total tokens used (input + output)
    """
    try:
        conn = sqlite3.connect('token_tracking.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO token_tracking 
        (user_query, agent_name, node_name, input_token, output_token, total_token)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_query, agent_name, node_name, input_token, output_token, total_token))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        if conn:
            conn.close()
        raise e

def show_token_tracking():
    """
    Displays all records from the token_tracking table
    
    Returns:
        list: List of tuples containing all records from token_tracking table
    """
    try:
        conn = sqlite3.connect('token_tracking.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM token_tracking')
        records = cursor.fetchall()
        
        conn.close()
        return records
        
    except Exception as e:
        if conn:
            conn.close()
        raise e

def check_and_create_db():
    """
    Checks if the token_tracking table exists in the database, creates it if not
    """
    try:
        conn = sqlite3.connect('token_tracking.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute('''
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='token_tracking'
        ''')
        
        table_exists = cursor.fetchone()
        conn.close()
        
        if not table_exists:
            print("Token tracking table does not exist. Creating table...")
            create_token_tracking_table()
            print("Token tracking table created successfully")
        else:
            print("Token tracking table already exists")
            
    except Exception as e:
        if conn:
            conn.close()
        raise e

if __name__ == "__main__":
    check_and_create_db()
