from connection.packet import Packet
import sqlite3

def createPacketTable(cursor: sqlite3.Cursor):
    cursor.execute("""DROP TABLE IF EXISTS packets""")

    packetTable = """CREATE TABLE packets(
    packetID INTEGER PRIMARY KEY,
    client VARCHAR(255),
    type INTEGER NOT NULL,
    category INTEGER NOT NULL,
    command VARCHAR(255) )"""

    cursor.execute(packetTable)

def addPacketToTable(cursor: sqlite3.Cursor, packet: Packet):
    addPacket = f"""INSERT INTO PACKETS(packetID, client, type, category, command) 
    values(NULL, '{packet.client}', {packet.type}, {packet.category}, '{packet.command}')"""

    cursor.execute(addPacket)
    cursor.connection.commit()

def getAllPackets(cursor: sqlite3.Cursor):
    
    getPackets = """SELECT * FROM packets"""
    cursor.execute(getPackets)
    packets = cursor.fetchall()

    return packets