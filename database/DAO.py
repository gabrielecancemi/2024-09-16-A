from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_min_max():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select min(s.Lat) as minLat, max(s.Lat) as maxLat, min(s.Lng) as minLon, max(s.Lng) as maxLon  from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append((row["minLat"], row["maxLat"]))
                result.append((row["minLon"], row["maxLon"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_shapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.shape) from sighting s where s.shape != "" order by s.shape desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodi(lat, lon, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.* from state s, sighting s2  where s.Lat > %s and s.Lng > %s and s.id = s2.state 
                        and s2.shape = %s group by s.id"""
            cursor.execute(query, (lat, lon, shape))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_durate(shape):
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.state as st, sum(s.duration) as tot from sighting s where s.shape = %s group by s.state """
            cursor.execute(query, (shape,))

            for row in cursor:
                result[row["st"].upper()] = row["tot"]
            cursor.close()
            cnx.close()
        return result




