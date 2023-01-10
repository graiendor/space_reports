from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, MetaData


class Recorder():
    def __init__(self):
        self.engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
        self.meta = MetaData()
        self.spaceship_table = Table(
            'spaceships', self.meta,
            Column('id', Integer, primary_key=True),
            Column('alignment', String),
            Column('name', String),
            Column('length', String),
            Column('vessel_class', String),
            Column('size', String),
            Column('armed', String),
        )
        self.officers_table = Table(
            'officers', self.meta,
            Column('id', Integer, primary_key=True),
            Column('first_name', String),
            Column('last_name', String),
            Column('rank', String),
            Column('spaceship_id', Integer, ForeignKey('spaceships.id'))
        )
        self.traitor_table = Table(
            'traitors', self.meta,
            Column('id', Integer, primary_key=True),
            Column('first_name', String),
            Column('last_name', String),
            Column('rank', String)
        )
        self.meta.create_all(self.engine)
        self.create_tables()

    def create_tables(self):
        self.meta.create_all(self.engine)

    def insert_spaceship(self, spaceship):
        if not self.spaceship_exists(spaceship):
            spaceship_insert = self.spaceship_table.insert().values(
                alignment=spaceship.alignment, name=spaceship.name, length=spaceship.length,
                vessel_class=spaceship.vessel_class, size=spaceship.size, armed=spaceship.armed).returning(
                self.spaceship_table.c.id)
            spaceship_id = self.engine.execute(spaceship_insert).fetchone()[0]
            self.insert_officers(spaceship.officers, spaceship_id)
        else:
            update_query = self.spaceship_table.update().where(
                self.spaceship_table.c.name == spaceship.name).values(alignment=spaceship.alignment,
                                                                      name=spaceship.name,
                                                                      length=spaceship.length,
                                                                      vessel_class=spaceship.vessel_class,
                                                                      size=spaceship.size, armed=spaceship.armed)
            self.engine.execute(update_query)

    def insert_officers(self, officers, spaceship_id: int):
        for officer in officers:
            officer_insert = self.officers_table.insert().values(
                first_name=officer['first_name'], last_name=officer['last_name'], rank=officer['rank'],
                spaceship_id=spaceship_id)
            self.engine.execute(officer_insert)

    def spaceship_exists(self, spaceship_to_check):
        spaceship_query = self.spaceship_table.select().where(
            self.spaceship_table.c.name == spaceship_to_check.name)
        spaceship = self.engine.execute(spaceship_query).fetchone()
        officer_identical = False
        if spaceship:
            officer_query = self.officers_table.select().where(
                self.officers_table.c.spaceship_id == spaceship.id)
            officers = self.engine.execute(officer_query).fetchall()
            for officer in officers:
                if officer['first_name'] in [officer['first_name'] for officer in spaceship_to_check.officers] and \
                        officer['last_name'] in [officer['last_name'] for officer in spaceship_to_check.officers]:
                    officer_identical = True
        return spaceship is not None and not officer_identical

    def insert_traitor(self, traitor):
        if not self.traitor_exists(traitor):
            traitor_insert = self.traitor_table.insert().values(
                first_name=traitor['firstName'], last_name=traitor['lastName'], rank=traitor['rank'])
            self.engine.execute(traitor_insert)

    def traitor_exists(self, traitor):
        traitor_query = self.traitor_table.select().where(
            self.traitor_table.c.first_name == traitor['firstName'] and self.traitor_table.c.last_name == traitor[
                'lastName'])
        traitor = self.engine.execute(traitor_query).fetchone()
        return traitor is not None

    def get_traitors(self):
        traitors = []
        traitor_query = self.traitor_table.select()
        traitors = self.engine.execute(traitor_query).fetchall()
        return traitors
