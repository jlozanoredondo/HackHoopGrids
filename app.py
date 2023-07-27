from flask import Flask, render_template, request
import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "ddbb/nba.db")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, nombre, abbr FROM equipos')
    teams = c.fetchall()
    players = []
    team_1 = {}
    team_2 = {}

    if request.method == 'POST':
        team_1_id = request.form.get('team1')
        team_2_id = request.form.get('team2')

        c.execute('SELECT id, nombre, abbr FROM equipos WHERE id=?', (team_1_id,))
        team_1_id, team_1_name, team_1_abbr = c.fetchone()
        team_1 = {'id': team_1_id, 'name': team_1_name, 'abbr': team_1_abbr}

        c.execute('SELECT id, nombre, abbr FROM equipos WHERE id=?', (team_2_id,))
        team_2_id, team_2_name, team_2_abbr = c.fetchone()
        team_2 = {'id': team_2_id, 'name': team_2_name, 'abbr': team_2_abbr}
        
        query = '''
            SELECT 
                J.id,
                J.nombre,
                J.active,
                SUM(CASE WHEN JE1.id_equipo = ? THEN JE1.num_partidos ELSE 0 END) as games_played_team1,
                SUM(CASE WHEN JE2.id_equipo = ? THEN JE2.num_partidos ELSE 0 END) as games_played_team2
            FROM 
                jugador_equipo JE1 
                JOIN jugador_equipo JE2 ON JE1.id_jugador = JE2.id_jugador 
                JOIN jugadores J ON JE1.id_jugador = J.id
            WHERE 
                JE1.id_equipo = ? AND 
                JE2.id_equipo = ? AND
                JE1.id_jugador = JE2.id_jugador
            GROUP BY
                J.id
            ORDER BY 
                (games_played_team1 + games_played_team2)
        '''
        c.execute(query, (team_1_id, team_2_id, team_1_id, team_2_id))
        players = [{
            'id': row[0],
            'name': row[1],
            'active': row[2],
            'games_played_team1': row[3],
            'games_played_team2': row[4]
        } for row in c.fetchall()]

    conn.close()
    return render_template('index.html', teams=teams, players=players, team_1=team_1, team_2=team_2)


if __name__ == '__main__':
    app.run(debug=True)
