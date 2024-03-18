import sqlite3
from bs4 import BeautifulSoup

# Connect to source and target databases
source_conn = sqlite3.connect('source_db.sqlite')
target_conn = sqlite3.connect('target_db.sqlite')

# Create a cursor for each database
source_cursor = source_conn.cursor()
target_cursor = target_conn.cursor()

# Create new_table in the target database if it doesn't exist
target_cursor.execute("""
CREATE TABLE IF NOT EXISTS new_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_block TEXT,
    next_page TEXT,
    text TEXT,
    code_tags TEXT
)
""")

# Query to fetch data from source database
source_cursor.execute("SELECT content FROM pages")

# Iterate over each row in the source database
for row in source_cursor:
    html = row[0]

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    li_tags = soup.find_all('li', {'class': 'listitem'})

    for li in li_tags:
        p_tags = li.find_all('p')
        text = ' '.join([p.text for p in p_tags])

        pre_tag = li.find('pre', {'class': 'programlisting prettyprint lang-sh'})
        print(pre_tag)
        code_block = pre_tag.text if pre_tag else None

        data = {
            'code_block': code_block,
            'text': text,
        }

        # Insert the parsed data into the target database
        target_cursor.execute("INSERT INTO new_table (code_block, text) VALUES (?, ?)", 
                              (data['code_block'], data['text']))

# Commit the changes and close the connections
target_conn.commit()
source_conn.close()
target_conn.close()