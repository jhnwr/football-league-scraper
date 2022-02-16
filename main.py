from sqlmodel.sql.expression import Select, SelectOfScalar

from db.database import create_db_and_tables
from services.league_service import get_league_data, add_to_database, update_teams

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True


def main():
    create_db_and_tables()
    leagues = ['championship-table', 'premier-league-table', 'league-1-table', 'league-2-table']
    for league in leagues:
        data = get_league_data(league)
        add_to_database(data)
        update_teams(data)


if __name__ == "__main__":
    main()
