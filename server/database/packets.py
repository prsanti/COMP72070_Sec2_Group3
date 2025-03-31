from ..connection.packet import Packet
import users
import sqlite3

def createPacketTable(cursor: sqlite3.Cursor):
    cursor.execute("""DROP TABLE IF EXISTS packets""")

    packetTable = """CREATE TABLE packets(
    packetID integer primary key,
    client varchar(255),
    type integer not null,
    category integer not null,
    command varchar )"""

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