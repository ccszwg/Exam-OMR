from docx import *


def generate_questions():
    while True:
        try:
            num_questions = int(input("How many question are there? "))
        except:
            print("Please type a number")
            continue
        break

    while True:
        try:
            num_options = int(input("How many options per questions are there? "))
        except:
            print("Please type a number")
            continue
        break

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = ""


    for i in range(1, num_questions+1):
        text += "Question %s: \n   " % (str(i))

        for j in alphabet[0:num_options]:
            text += "%s   ◯      " % j

        if i == 10:
            text += "\n\n\n"
        else:
            text += "\n\n"

    return text


def replace_string(old_text, new_text, filename):
    doc = Document(filename)
    for p in doc.paragraphs:
        if old_text in p.text:
            inline = p.runs
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                if old_text in inline[i].text:
                    text = inline[i].text.replace(old_text, new_text)
                    inline[i].text = text

    doc.save('marking script.docx')
    return 1


def activate_replacement():
    replace_string("{{QUESTIONS}}", generate_questions(), "resources/template.docx")

activate_replacement()
