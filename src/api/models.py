from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, UUID, Numeric

metadata = MetaData()

menu = Table(
    'menu',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
)

submenu = Table(
    'submenu',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    Column('menu_id', Integer, ForeignKey('menu.id', ondelete='CASCADE'))
)

dish = Table(
    'dish',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    # Column('price', Numeric, nullable=False),
    Column('price', String, nullable=False),
    Column('submenu_id', Integer, ForeignKey('submenu.id', ondelete='CASCADE'))
)