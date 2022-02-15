from requests_html import HTMLSession
from sqlmodel import Session, select

from db.database import engine
from db.models import Team


def is_negative(value):
    # how to change all numbers inc negative to an int from a str
    if value[0] == '-':
        return value[1:].isdigit()
    else:
        return value.isdigit()


def get_league_data(league_name):
    s = HTMLSession()
    url = f'https://www.skysports.com/{league_name}'
    r = s.get(url)
    table = r.html.find('table')[0]
    tabledata = [[int(c.text.replace('*', '').strip()) if is_negative(c.text) else c.text.replace('*', '').strip() for c in row.find('td')[:-1]]
                 for row in table.find('tr')][1:]
    for row in tabledata:
        row.append(league_name)
    return tabledata


def add_to_database(tabledata):
    with Session(engine) as session:
        for row in tabledata:
            loading = Team(
                league_name=row[10],
                position=row[0],
                team_name=row[1],
                played=row[2],
                won=row[3],
                drawn=row[4],
                lost=row[5],
                goals_for=row[6],
                goals_against=row[7],
                goal_difference=row[8],
                points=row[9],
            )

            statement = select(Team).where(Team.team_name == row[1])
            res = session.exec(statement)
            if not res.first():
                session.add(loading)
                session.commit()
                session.refresh(loading)
                print(f'added team {row[1]}')


def update_teams(tabledata):
    with Session(engine) as session:
        for row in tabledata:
            statement = select(Team).where(Team.team_name == row[1])
            res = session.exec(statement)
            team = res.one()

            team.league_name = row[10].replace('-table', '')
            team.position = row[0]
            team.team_name = row[1]
            team.played = row[2]
            team.won = row[3]
            team.drawn = row[4]
            team.lost = row[5]
            team.goals_for = row[6]
            team.goals_against = row[7]
            team.goal_difference = row[8]
            team.points = row[9]

            session.add(team)
            session.commit()
            session.refresh(team)
            #print('Updated:', team)


if __name__ == '__main__':
    data = get_league_data('championship-table')
