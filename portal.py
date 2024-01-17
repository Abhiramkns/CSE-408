import gradio as gr
import random
import os
from tqdm import tqdm

class Student:
    def __init__(self, id=None) -> None:
        # TODO: read student details from json file
        self.id = id
        self.count = 0

student = None
selected_image = None
folder_path = "./images"
images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg'))]
total_items = 20

def get_image():
    global images
    image_id = random.choice(images) if images else None
    return image_id

def start(studentId):
    global student 
    global selected_image
    
    # TODO: write student id to json file.    
    student = Student(studentId)
    selected_image = get_image()
    return gr.update(visible=True), gr.update(visible=False), gr.update(value=selected_image, visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)

def go_to_nextq(answer1, answer2):
    # TODO: write input1 and input2 to json file
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=True)

def got_to_nextexe(answer3, answer4):
    global student
    global selected_image
    global total_items
    
    # TODO: write input1 and input2 to json file
    
    student.count += 1
    if student.count == total_items:
      return  gr.update(value=f"{student.count}/{total_items}"), gr.update(visible=True), gr.update(value=selected_image, visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    
    selected_image = get_image()
    return gr.update(value=f"{student.count}/{total_items}"), gr.update(visible=False), gr.update(value=selected_image, visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    

with gr.Blocks() as iface:
    studentId = gr.Textbox(label="ASU ID")
    counter = gr.Textbox(value=f"{0}/{total_items}", show_label=False, visible=False)
    img = gr.Image(value=None, interactive=False, show_download_button=False, show_share_button=False, height=512, width=512, elem_id="output_image")
    q2 = gr.Textbox(label="Q1")
    q3 = gr.Textbox(label="Q2")
    q4 = gr.Slider(label="Q3", maximum=9)
    q5 = gr.Textbox(label="Q4")
    finish = gr.Textbox(value="Task finshed", interactive=False, visible=False, label="")
    nextexe_btn = gr.Button("Submit")
    nextq_btn = gr.Button("Next")
    start_btn = gr.Button("Start")
    
    # Set initial visibility
    studentId.visible = True
    img.visible = False
    q2.visible = False
    q3.visible = False
    q4.visible = False
    q5.visible = False
    nextexe_btn.visible = False
    nextq_btn.visible = False

    start_btn.click(start, inputs=studentId, outputs=[counter, studentId, img, q2, q3, nextq_btn, start_btn])
    nextq_btn.click(go_to_nextq, inputs=[q2, q3], outputs=[q2, q3, q4, q5, nextq_btn, nextexe_btn])
    nextexe_btn.click(got_to_nextexe, inputs=[q4, q5], outputs=[counter, finish, img, q2, q3, q4, q5, nextq_btn, nextexe_btn])

    
iface.launch()
