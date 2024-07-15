import sqlite3

def get_the_concept_ids():
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Definitioner")
    rows = cursor.fetchall()
    conn.close()
    return [a for a, in rows]

def get_concept(id_):
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM Definitioner WHERE id = ?",(id_,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_concepts():
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Definitioner")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_edges_db2():
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, gen, spec FROM Contexts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_column(table_choice, column_name, data_type, database = None):
    if database != None:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
    else:
        conn = sqlite3.connect('lin_fk.db')
        cursor = conn.cursor()
    cursor.execute("ALTER TABLE {} ADD COLUMN {} {}".format(table_choice, column_name, data_type))
    conn.commit()
    conn.close()

def create_table(table_name):
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            gen INTEGER NOT NULL,
            spec INTEGER NOT NULL
            );
        """)
    conn.commit()
    conn.close()

def insert_into_table(q, s, table_name):
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(id) FROM {table_name}")
    max_id = cursor.fetchone()[0]
    next_id = 1 if max_id is None else max_id + 1
    print(q[1])
    query = f"INSERT INTO {table_name} (id, {q[0]}, {s[0]}) VALUES (?, ?, ?)"
    cursor.execute(query, (next_id, q[1], s[1]))
    conn.commit()
    conn.close()

def delete_rows(id_):
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Contexts WHERE id = ?",(id_,))
    conn.commit()
    conn.close()

def update_column_for_row_at_id(table_name, id_, new_column):
    """
    Updates a specific column for a specific row in a given SQLite database table based on the row's ID.

    Args:
        table_name (str): The name of the table to update.
        id (int): The ID of the row to update.
        new_column (tuple): A tuple containing the column name and the new value to set.

    Example:
        update_column_for_row_at_id('users', 123, ('email', 'new.email@example.com'))
        This will update the 'email' column for the row with ID 123 in the 'users' table to 'new.email@example.com'.
    """
    conn = sqlite3.connect('grupper_ringar.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET {new_column[0]} = ? WHERE id = ?", (new_column[1], id_))
    conn.commit()
    conn.close()
#

update_column_for_row_at_id('Inheritances',115, ('validation',0))
print('done')
#for i in range(0,2795):
    #delete_rows(i)
#create_table('Contexts')
#create_table('Implied_Contexts')
#add_column('Contexts','validation_reasoning','TEXT','grupper_ringar.db')
#add_column('Implied_Contexts','validation_reasoning','TEXT','grupper_ringar.db')
#add_column('Contexts','validation','INTEGER','grupper_ringar.db')
#add_column('Implied_Contexts','validation','INTEGER','grupper_ringar.db')