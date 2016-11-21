import docx


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


def replace_string(doc, holder, newtext):

    for paragraph in doc.paragraphs:
        if holder in paragraph.text:
            paragraph.text = newtext

    return doc


def activate_replacement(template):

    doc = docx.Document(template)

    replace_string(doc, "{{IDENTITY}}", "name")
    replace_string(doc, "{{QUESTIONS}}", generate_questions())

    doc.save("test.docx")

activate_replacement("resources/template.docx")
