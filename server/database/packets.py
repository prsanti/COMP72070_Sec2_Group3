from connection.packet import Packet
import sqlite3

def createPacketTable(cursor: sqlite3.Cursor):

    packetTable = """CREATE TABLE IF NOT EXISTS packets(
    packetID INTEGER PRIMARY KEY,
    client VARCHAR(255),
    type VARCHAR(10) NOT NULL,
    category VARCHAR(10) NOT NULL,
    command VARCHAR(255) )"""

    cursor.execute(packetTable)

def creatSentPacketTable(cursor: sqlite3.Cursor):

    packetTable = """CREATE TABLE IF NOT EXISTS SentPackets(
    packetID INTEGER PRIMARY KEY,
    client VARCHAR(255),
    type VARCHAR(10) NOT NULL,
    category VARCHAR(10) NOT NULL,
    command VARCHAR(255) )"""

    cursor.execute(packetTable)

def addPacketToTable(packet: Packet):
    from .database import connectAndCreateCursor

    connection, cursor = connectAndCreateCursor()

    # Serialize the command to a string safely (e.g., using JSON)
    import json
    command_value = json.dumps(packet.command) if isinstance(packet.command, list) else str(packet.command)

    sql = """INSERT INTO packets(packetID, client, type, category, command) 
             VALUES (NULL, ?, ?, ?, ?)"""

    values = (
        str(packet.client),
        packet.type.name,
        packet.category.name,
        command_value
    )

    cursor.execute(sql, values)
    connection.commit()
    connection.close()

    
def addSentPacketToTable(packet: Packet):
    from .database import connectAndCreateCursor
    
    client_value = str(packet.client)
    client_value = client_value.replace("'", "''")
    connection, cursor = connectAndCreateCursor()
    addPacket = f"""INSERT INTO SentPackets(packetID, client, type, category, command) 
    values(NULL, '{client_value}', '{packet.type.name}', '{packet.category.name}', '{packet.command}')"""

    cursor.execute(addPacket)
    connection.commit()
    connection.close

def getAllPackets(cursor: sqlite3.Cursor):
    
    getPackets = """SELECT * FROM packets"""
    cursor.execute(getPackets)
    packets = cursor.fetchall()

    return packets  

def getAllSentPackets(cursor: sqlite3.Cursor):
    getPackets = """SELECT * FROM SentPackets"""
    cursor.execute(getPackets)
    packets = cursor.fetchall()

    return packets