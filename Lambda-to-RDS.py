import pymysql
import os

# Set these in Lambda Environment Variables
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']

def lambda_handler(event, context):
    conn = None
    try:
        # 1. Connect to the RDS Instance (not a specific DB)
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            connect_timeout=5
        )
        
        with conn.cursor() as cur:
            # 2. Create the database schema if it doesn't exist
            cur.execute("CREATE DATABASE IF NOT EXISTS naresh_database")
            
            # 3. Switch to that database
            cur.execute("USE naresh_database")
            
            # 4. Define the correct Table structure
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Users (
                UserID INT AUTO_INCREMENT PRIMARY KEY,
                Username VARCHAR(255) NOT NULL,
                Email VARCHAR(255),
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # 5. Execute and Commit
            cur.execute(create_table_query)
            conn.commit()
            
        return {
            "statusCode": 200, 
            "body": "Database 'naresh_database' and table 'Users' are ready!"
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
        
    finally:
        if conn:
            conn.close()
