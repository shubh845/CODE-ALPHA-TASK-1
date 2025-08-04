from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

WORDS = ['python', 'developer', 'flask', 'hangman', 'function', 'variable']
MAX_TRIES = 6

def pick_word():
    return random.choice(WORDS)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'word' not in session:
        session['word'] = pick_word()
        session['guessed'] = []
        session['tries'] = 0

    word = session['word']
    guessed = session['guessed']
    tries = session['tries']

    if request.method == 'POST':
        letter = request.form['letter'].lower()
        if letter not in guessed and letter.isalpha() and len(letter) == 1:
            guessed.append(letter)
            if letter not in word:
                tries += 1
        session['guessed'] = guessed
        session['tries'] = tries

    display_word = ' '.join([l if l in guessed else '_' for l in word])
    game_over = tries >= MAX_TRIES
    game_won = all(l in guessed for l in word)

    return render_template(
        'index.html',
        display_word=display_word,
        guessed=guessed,
        tries=tries,
        max_tries=MAX_TRIES,
        game_over=game_over,
        game_won=game_won,
        word=word
    )

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
