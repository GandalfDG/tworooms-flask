
def init_db_indices(db):
    db.games.create_index("access_code")