# pylint: disable=line-too-long

"""Data Access for Guests"""

from sqlite3 import Connection

from app.domain.Guests import Guest, GuestDTO


class GuestDAO:
    """Guest DAO is a abstraction for database operations"""

    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        """counts all records"""
        cursor = self.db.cursor()
        count = cursor.execute('SELECT COUNT(*) FROM guest').fetchone().get('COUNT(*)')
        return count

    def insert(self, guest: Guest) -> None:
        """creates a new register"""
        guest_dto = guest.to_dict()
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT INTO guest (document, created_at, name, surname, country, phone) VALUES (?, ?, ?, ?, ?, ?);'
            , (guest_dto['document'], guest_dto['created_at'], guest_dto['name'], guest_dto['surname'], guest_dto['country'], guest_dto['phone'],))
        self.db.commit()

    def find(self, document) -> Guest | None:
        cursor = self.db.cursor()
        cursor.execute('SELECT document, created_at, name, surname, country, phone FROM guest WHERE guest.document = ?;',  (document,))
        result = cursor.fetchone()

        if result is None:
            return

        guest_dto: GuestDTO = {
            'document': result['document'],
            'name': result['name'],
            'surname': result['surname'],
            'phone': result['phone'],
            'country': result['country'],
            'created_at':result['created_at']}

        guest = Guest(guest_dto)
        return guest

    def find_many(self) -> list[Guest]:
        """searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT document, created_at, name, surname, country, phone FROM guest;')
        result = cursor.fetchall()

        if len(result) < 1:
            return result

        guests = [ Guest({
                'document': guest['document'],
                'name': guest['name'],
                'surname': guest['surname'],
                'country': guest['country'] ,
                'phone': guest['phone'],
                'created_at': guest['created_at']
            }) for guest in result ]

        return guests


    def update(self, guest: Guest) -> None:
        """updates a record in the table as a whole. params must have the document of the data to be updated as well as all the entity values in the table"""
        guest_dto = guest.to_dict()
        cursor = self.db.cursor()
        cursor.execute('UPDATE guest SET name = :name, surname = :surname, country = :country, phone = :phone WHERE document = :document;', guest_dto)

    def delete(self, document):
        """delete a record based on its document, params -> { document: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM guest WHERE document = ?', (document,))
