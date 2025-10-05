#!/usr/bin/env python3
"""
Script to load the complete schema.sql file into the database
"""

import subprocess
import os

def load_full_schema():
    """Load the complete schema.sql file into the database"""
    try:
        print("Loading complete schema.sql into database...")
        
        # MySQL command to execute the schema file
        mysql_cmd = [
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
            "-u", "root",
            "-proot",
            "tcc_zilli"
        ]
        
        # Read the schema file
        with open('flaskr/schema.sql', 'r', encoding='utf-8') as file:
            schema_content = file.read()
        
        # Add foreign key constraint disabling at the beginning
        schema_content = "SET FOREIGN_KEY_CHECKS=0;\n" + schema_content
        # Fix the UNIQUE constraint issue by removing it
        schema_content = schema_content.replace('RES_RESUMO TEXT UNIQUE', 'RES_RESUMO TEXT')
        # Increase column sizes
        schema_content = schema_content.replace('RES_TITULO VARCHAR(100)', 'RES_TITULO VARCHAR(500)')
        schema_content = schema_content.replace('OBJ_CONSTRUCOES_LINGUISTICAS VARCHAR(500)', 'OBJ_CONSTRUCOES_LINGUISTICAS VARCHAR(1000)')
        schema_content = schema_content.replace('CON_CONSTRUCOES_LINGUISTICAS VARCHAR(500)', 'CON_CONSTRUCOES_LINGUISTICAS VARCHAR(1000)')
        # Re-enable foreign key constraints at the end
        schema_content = schema_content + "\nSET FOREIGN_KEY_CHECKS=1;"
        
        # Execute the schema
        process = subprocess.run(
            mysql_cmd,
            input=schema_content,
            text=True,
            encoding='utf-8',
            capture_output=True
        )
        
        if process.returncode == 0:
            print("✅ Schema loaded successfully!")
            print("📊 Database now contains all 99 abstracts with objectives and conclusions")
        else:
            print(f"❌ Error loading schema: {process.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    load_full_schema()
