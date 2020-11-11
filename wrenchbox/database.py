import argparse
import logging
from datetime import datetime

from munch import Munch
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from .logging import setup_log


class Database:
    def __init__(self, url: str, schema: str = None, allow_empty: bool = False):
        logging.info('Connecting: %s', url)
        self.url = url
        self.schema = schema
        self.engine = create_engine(self.url, connect_args={'options': '-csearch_path={}'.format(self.schema)} if self.schema is not None else dict())
        self.session = Session(self.engine)
        try:
            self.base = automap_base()
            self.base.prepare(self.engine, reflect=True)
        except Exception as exp:
            if allow_empty:
                logging.warning('Cannot map tables, an empty base will be created: %s', self.url)
                self.base = None
            else:
                raise exp
        logging.info('Connection is established: %s', self.url)


class Table:
    def __init__(self, pool: Munch, database: str, table: str, alt_table=None):
        self.session = getattr(pool, database).session
        if alt_table is not None:
            logging.info('Alternative table is provided: %s.%s', database, table)
            self.model = alt_table
        elif getattr(pool, database).base is not None:
            try:
                self.model = getattr(getattr(pool, database).base.classes, table)
            except AttributeError as exp:
                if table in getattr(pool, database).base.metadata.tables.keys():
                    logging.critical('Cannot find table (mainly caused by missing primary key): %s.%s', database, table)
                raise exp
        else:
            logging.critical('No database is provided for table: %s.%s', database, table)


class DatabaseHandler:
    def __init__(self, databases: dict, tables: list, alt_tables: dict = None):
        """
        Init a database handler
        :param databases: a dict of databases such like {'db':'url',...}
        :param tables: a list of tuples such like [('db','table'),...]
        """
        logging.info('Init database handler...')
        self.config = Munch(
            databases=databases,
            tables=tables,
            alt_tables=alt_tables
        )
        self.o = Munch()
        self.db = Munch()
        if len(self.config.databases) and len(self.config.tables):
            self.connect(True)
        else:
            logging.warning('No database or table info are provided, an empty database handler will be created.')
        logging.info('Initialization of database handler is completed.')

    def connect(self, reconnect: bool = False):
        if reconnect:
            self.o = Munch()
            self.db = Munch()
        for table in self.config.tables:
            if self.config.alt_tables is not None and table[1] in self.config.alt_tables:
                alt_table = self.config.alt_tables[table[1]]
            else:
                alt_table = None
            if getattr(self.db, table[0], None) is None:
                logging.info('Creating database connection: %s', table[0])
                setattr(self.db, table[0], Database(
                    self.config.databases[table[0]],
                    schema='public' if self.config.databases[table[0]].startswith('postgresql') else None,
                    allow_empty=alt_table is not None
                ))
                logging.info('Database connection is established: %s', table[0])
            setattr(self.o, table[1], Table(self.db, table[0], table[1], alt_table=alt_table))
            logging.info('Table is synced: %s.%s', table[0], table[1])

    @staticmethod
    def commit(session, item):
        logging.debug(item.__dict__)
        session.add(item)
        try:
            session.commit()
        except Exception as exp:
            session.rollback()
            raise exp

    def handle(self, table: str, filters: dict, fields: dict, inserts: dict = None, replace: bool = True):
        """
        Perform insert or update query
        :param table: target table name
        :param filters: filters for identifying the unique record
        :param fields: fields for the insert or update
        :param inserts: fields for insert only despite of "fields"
        :param replace: no change will be applied to existing records if set to False
        :return:
        """
        c = getattr(self.o, table)
        s = c.session.query(c.model).filter_by(**filters)
        k = None
        if s.count() > 0:
            if s.count() == 1:
                k = s.first()
                if replace:
                    logging.debug('Targeting record of "%s" exists, will be replaced: %s', table, filters)
                    for key, value in fields.items():
                        setattr(k, key, value)
                    self.commit(c.session, k)
                else:
                    logging.debug('Targeting record of "%s" exists, will be kept: %s', table, filters)
            else:
                logging.error('Identifier of "%s" is not unique: %s', table, filters)
        else:
            k = c.model(**fields)
            if inserts:
                for key, value in inserts.items():
                    setattr(k, key, value)
            self.commit(c.session, k)
        return k


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='show debug information')
    parser.add_argument('--replace', action='store_true', default=False, help='replace existing records')
    parser.add_argument('--id', type=int, default=1, help='test id, default: 1')
    parser.add_argument('db', type=str, help='database url')
    parser.add_argument('table', type=str, help='table name, must have columns of "id" and "name"')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    DatabaseHandler({
        'test': args.db
    }, [
        ('test', 'test')
    ]).handle(
        'test', {
            'id': args.id
        }, {
            'id': args.id,
            'name': str(datetime.now())
        }, replace=args.replace
    )
