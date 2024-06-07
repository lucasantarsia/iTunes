from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbums(d):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.* , sum(t.Milliseconds) as totD
                from album a , track t 
                where a.AlbumId = t.AlbumId 
                group by a.AlbumId 
                having totD > %s"""

        cursor.execute(query, (d,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow t.AlbumId as a1 , t2.AlbumId as a2
                from playlisttrack p , track t , playlisttrack p2 , track t2 
                where p2.PlaylistId = p.PlaylistId
                and t2.TrackId = p.TrackId
                and p.TrackId = t.TrackId
                and t.AlbumId < t2.AlbumId"""

        cursor.execute(query)

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:  # append lo faccio solo se i due nodi sono nel grafo
                result.append((idMap[row["a1"]], idMap[row["a2"]]))

        cursor.close()
        conn.close()
        return result
