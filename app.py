import os, io
from google.cloud import vision
from docx import Document

def detect_text(name, path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    file = open("results/" + name + ".txt", "w+")
    document = Document()
    p = document.add_paragraph("")

    for text in texts:
        if text.description.find("-") != -1:
            temp_content = text.description.replace("-\n","").replace("-", "")
            p.add_run(temp_content)
            file.write(temp_content)
        else:
            p.add_run(text.description + " ")
            file.write(text.description + " ")

        #vertices = (['({},{})'.format(vertex.x, vertex.y)
                    #for vertex in text.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))

    document.add_page_break()
    document.save("results/" + name + ".docx")
    file.close()

    print("Completed", name)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"Token.json"

paths = ["images/" + i for i in os.listdir("images")]
names = [i[:i.find(".")] for i in os.listdir("images")]

for name, path in zip(names, paths): detect_text(name,path)

print("Completed")