from models import Users, Cart, Parts
from extensions import db as db_flask
from sqlalchemy import text, sql, select, exists


def check_if_part_exists(part_id):
    # Create a select statement using exists() and where() to check if the part_id exists

    exists_query = db_flask.session.query(db_flask.exists().where(Cart.part_id == part_id))
    element_exists = exists_query.scalar()


    return element_exists

if __name__ == '__main__':
    # Test the function
    part_id_to_check = 2
    exists_result = check_if_part_exists(part_id_to_check)
    print(f"Element with part_id {part_id_to_check} exists: {exists_result}")