from flask import Flask, render_template, request, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

RESPONSES_KEY="responses"

@app.route('/')
def homepage():
    """Show the start of survey"""

    return render_template('home.html', survey=survey)

@app.route('/begin', methods=['POST'])
def start_survey():
    """Clear session and redirect to questions.html"""
    
    session[RESPONSES_KEY] = []
    
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_question():
    """Store answers and redirect to next question"""
    
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses    

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    else: 
        return redirect (f'/questions/{len(responses)}')


@app.route('/questions/<int:question_id>')
def show_questions(question_id):
    """Show current questions"""
    responses = session.get(RESPONSES_KEY)
        
    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != question_id):
        flash(f'Invalid Input')
        return redirect (f'/questions/{len(responses)}')    
    
    question = survey.questions[question_id]
    return render_template(
        "questions.html", question_num=question_id, question=question)
    

@app.route('/complete')
def show_thankyou():
    """Redirect to thank you page"""
    return render_template('completion.html')


