from flask import Flask , redirect , url_for
from flask.helpers import flash
from flask.templating import render_template
from utils.game import Game

app = Flask(__name__)
game = Game()

app.config['SECRET_KEY'] = 'dattebayo!'

@app.route('/')
def home_page():
    return render_template('__home_page.html')

@app.route('/game')
def rps_game():
    if(game.is_in_progress):
        if(game.winner == 'Bot'):
            flash('Opps! The Bot Got The Point' , category='fail')
        elif(game.winner == 'Draw'):
            flash('Both Are Same! ' , category='yellow')
        else:
            flash('Good! You Got The Point' , category='success')
        
        game.winner = None
        game.is_in_progress = False
    
    return render_template('__game.html' , choosed = game.started , value = game.user , value_bot = game.bot , player_point = game.player_score , bot_point = game.bot_score , games = game.games)    
    
@app.route('/select/<option>')
def select(option):
    game.set_winner(option)
    
    game.is_in_progress = True
    
    game.started = True
    
    return redirect(url_for('rps_game'))

@app.route('/rematch')
def rematch():
    game.refresh_content()
    
    return redirect(url_for('rps_game'))