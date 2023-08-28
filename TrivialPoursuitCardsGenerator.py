import random, csv
from PIL import Image, ImageDraw, ImageFont

# Categories colors
colors = ['orange','blue','red','green','brown','yellow']
bg_color = 'snow' #'Honeydew' #'snow' # 'grey'
categories = []
questions = dict()

def category_color(category_name):
    return colors[categories.index(category_name) % len(colors)]

global_width, global_height = 180, 255
global_spacing = 4
trivial_font = ImageFont.truetype("arial.ttf", 10)
skyjo_big_font = ImageFont.truetype("arial.ttf", 36)
skyjo_small_font = ImageFont.truetype("arial.ttf", 16)
global_nb_questions_to_generate = 64
questions_filename='Periode 1 - questions trivialPursuit.csv'


# read questions in csv file named questions_filename
with open(questions_filename,'r',encoding="utf8") as csvfile :
    question_reader = csv.reader(csvfile, delimiter=',')
    next(question_reader)
    for question_row in question_reader :
        category_name = question_row[0]
        if category_name not in categories :
            categories.append(category_name) # create new category
            questions[category_name] = []

        questions[category_name].append({'question' : question_row[1].replace('*','\N{MULTIPLICATION SIGN}'),'answer' : question_row[2]},)        


# permet un retour à la ligne si on excède la largeur de la carte
def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        _, _, w, h = draw.textbbox((0,0),t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    _, _, w, h = draw.textbbox((0,0), t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)

def fit_text(img, text, color, font, xy):
    width = img.size[0] - 3
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = xy[1]
    for t, w, h in pieces:
        x = xy[0]
        draw.text((x, y), t, font=font, fill=color)
        y += h
    return y

# Fonction pour générer une carte aléatoire
def generate_card(use_random=True,question_number=0):
    card_questions = []
    card_reponses = []
    for c in categories :
        if use_random :
            q = random.choice(questions[c])
        else:
            q = questions[c][question_number%len(questions[c])]

        card_questions.append(q['question'])
        card_reponses.append(q['answer'])
    return {
        'questions': card_questions,
        'answers': card_reponses
    }

# Création d'une image de carte du jeu
def create_trivialPursuit_card(card, show_answer=True):
    # Création de l'image
    img = Image.new('RGB', (global_width, global_height), color=bg_color)

    # Création de l'objet Draw pour dessiner sur l'image
    draw = ImageDraw.Draw(img)

    line = 0
    number = 0
    for c in categories :
        # Ajout de la catégorie et de la question
        line = global_spacing + fit_text(img, card['questions'][number], category_color(c), trivial_font, (5, line)) # removed category to gain space c + ' : ' + 
        number += 1
    number = 0
    if show_answer :
        draw.line((0,line,img.width,line), fill=128)
        line += global_spacing
        for c in categories :
            # Ajout de la réponse
            line = global_spacing + fit_text(img, c + ' : ' + card['answers'][number], category_color(c), trivial_font, (5, line))
            number += 1

    return img

#skyjo cards contains only one question centered in card
def create_skyjo_card(card):
    # Création de l'image
    img = Image.new('RGB', (global_width, global_height), color='snow')

    # Création de l'objet Draw pour dessiner sur l'image
    draw = ImageDraw.Draw(img)
    
    question_lenght = len(card['questions'][0])
    if question_lenght > 13 :
        placement = (5,110)
        font = skyjo_small_font
    else :
        placement = (73 -question_lenght*6 , 115-5*question_lenght)
        font = ImageFont.truetype("arial.ttf", 75-5*question_lenght)
    fit_text(img, card['questions'][0], 'blue', font, placement)

    return img

# Génération de cartes aléatoires
for i in range(global_nb_questions_to_generate):
    card = generate_card(True,i)
    img = create_trivialPursuit_card(card)
    #img = create_skyjo_card(card)
    img.save(f"carte_{i+1}.jpg")