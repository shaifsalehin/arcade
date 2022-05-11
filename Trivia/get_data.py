#  get_data.py
#  
#  Copyright 2022  <Shaif Salehin, Arianna Martinez, I'munique Hill>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Created by: Shaif Salehin

import json
import pandas as pd
from urllib.request import urlopen
import random
import ftfy
import os

offline = False
choices = []


def connect():
    global offline
    try:
        offline = False
        # https://opentdb.com/api.php?amount=20&type=multiple
        with urlopen('https://opentdb.com/api.php?amount=50&type=multiple') as page:
            data = json.loads(page.read().decode())
            df = pd.DataFrame(data["results"])
            
            return df
    except:
        offline = True
        with urlopen('file:Assets/misc/trivia_backup_questions.json') as page:
            data = json.loads(page.read().decode())
            df = pd.DataFrame(data["results"])
          
            return df


def get_trivia_data(i):
    global choices, offline

    df = connect()
    vals = df.values

    random.seed(os.urandom(128))
    random_question = random.randint(0, (len(vals)-1))

    category = vals[random_question][0]
    difficulty = vals[random_question][2]
    question = vals[random_question][3]
    question = ftfy.fix_text(question)
    answer = vals[random_question][4]
    answer = ftfy.fix_text(answer)
    choices = list(vals[random_question][5])
    choices.append(vals[random_question][4])
    random.shuffle(choices)
    return category, difficulty, question, answer


# fix encoding symbols in 'choices' list, eg: N&uuml;rnberg is fixed to Nürnberg
def get_choices():
    global choices
    for i in range(len(choices)):
        tmp = choices[i]  # save element in temp variable
        choices.pop(i)  # pop the element
        # fix text and insert element in correct spot
        choices.insert(i, ftfy.fix_text(tmp))
    return choices
