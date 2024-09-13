from flask import Flask, Response, render_template
import cv2
import csv
import os
from functions import detect_face
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
app = Flask(__name__)
CORS(app)

questions = [
    {"id": 1, "text": "I am often troubled by discomfort in my chest or stomach.", "options": ["True", "False"], },
    {"id": 2, "text": "I feel sad most of the time.", "options": ["True", "False"], },
    {"id": 3, "text": "I often feel weak and tired.", "options": ["True", "False"], },
    {"id": 4, "text": "I have trouble following rules.", "options": ["True", "False"], },
    {"id": 5, "text": "I prefer jobs or hobbies that are typically associated with the opposite gender", "options": ["True", "False"], },
    {"id": 6, "text": "I believe that people often talk about me behind my back.", "options": ["True", "False"], },
    {"id": 7, "text": "I often feel overwhelmed by anxiety.", "options": ["True", "False"], },
    {"id": 8, "text": "I sometimes hear voices that others do not.", "options": ["True", "False"], },
    {"id": 9, "text": "I often feel more energetic than others.", "options": ["True", "False"], },
    {"id": 10, "text": "I prefer solitary activities.", "options": ["True", "False"], },
    {"id": 11, "text": "I get headaches more frequently than most people.", "options": ["True", "False"], },
    {"id": 12, "text": "It is hard for me to get started on tasks.", "options": ["True", "False"], },
    {"id": 13, "text": "I get dizzy spells that doctors cannot explain.", "options": ["True", "False"], },
    {"id": 14, "text": "I have been in trouble with the law.", "options": ["True", "False"], },
    {"id": 15, "text": "I feel that I am being watched or followed.", "options": ["True", "False"], },
    {"id": 16, "text": "I have obsessions I cannot get rid of.", "options": ["True", "False"], },
    {"id": 17, "text": "I see things that are not there.", "options": ["True", "False"], },
    {"id": 18, "text": "I have grand plans that others think are unrealistic.", "options": ["True", "False"], },
    {"id": 19, "text": "I am uncomfortable in social situations.", "options": ["True", "False"], },
    {"id": 20, "text": "My heart often races without any reason.", "options": ["True", "False"], },
    {"id": 21, "text": "I feel hopeless about the future.", "options": ["True", "False"], },
    {"id": 22, "text": "I sometimes lose feeling in parts of my body.", "options": ["True", "False"], },
    {"id": 23, "text": "I feel little remorse for things I have done wrong.", "options": ["True", "False"], },
    {"id": 24, "text": "I often feel misunderstood by the opposite sex.", "options": ["True", "False"], },
    {"id": 25, "text": "I trust very few people.", "options": ["True", "False"], },
    {"id": 26, "text": "I frequently check things (like locks, stoves).", "options": ["True", "False"], },
    {"id": 27, "text": "I believe in controlling forces that others find irrational.", "options": ["True", "False"], },
    {"id": 28, "text": "I talk much more rapidly than usual.", "options": ["True", "False"], },
    {"id": 29, "text": "I have few close friends.", "options": ["True", "False"], },
    {"id": 30, "text": "I am easily tired by everyday activities.", "options": ["True", "False"], },
    {"id": 31, "text": "I no longer enjoy things I used to.", "options": ["True", "False"], },
    {"id": 32, "text": "I am often not aware of my surroundings.", "options": ["True", "False"], },
    {"id": 33, "text": "I find it hard to maintain relationships.", "options": ["True", "False"], },
    {"id": 34, "text": "My interests align more with those typical of the opposite gender.", "options": ["True", "False"], },
    {"id": 35, "text": "I suspect others have secret motives.", "options": ["True", "False"], },
    {"id": 36, "text": "I have compulsions that I must repeat.", "options": ["True", "False"], },
    {"id": 37, "text": "My thoughts are often jumbled and disconnected.", "options": ["True", "False"], },
    {"id": 38, "text": "I need less sleep than most people.", "options": ["True", "False"], },
    {"id": 39, "text": "I often feel awkward around people.", "options": ["True", "False"], },
    {"id": 40, "text": "I worry a lot about physical problems that doctors say are minor.", "options": ["True", "False"], },
    {"id": 41, "text": "I feel like I am being punished.", "options": ["True", "False"], },
    {"id": 42, "text": "I feel like I have to be perfect at everything.", "options": ["True", "False"], },
    {"id": 43, "text": "I quickly get bored with routine.", "options": ["True", "False"], },
    {"id": 44, "text": "I prefer the company of the opposite sex.", "options": ["True", "False"], },
    {"id": 45, "text": "I find hidden meanings in casual remarks.", "options": ["True", "False"], },
    {"id": 46, "text": "I worry about thoughts I cannot control.", "options": ["True", "False"], },
    {"id": 47, "text": "I feel detached from reality.", "options": ["True", "False"], },
    {"id": 48, "text": "I can be irritable without any particular reason.", "options": ["True", "False"], },
    {"id": 49, "text": "I am quiet in groups.", "options": ["True", "False"], },
    {"id": 50, "text": "I feel that I have many health problems.", "options": ["True", "False"], },
    {"id": 51, "text": "I have thoughts of ending my life.", "options": ["True", "False"], },
    {"id": 52, "text": "Emotional situations make me feel physically ill.", "options": ["True", "False"], },
    {"id": 53, "text": "I enjoy doing things that are risky or dangerous.", "options": ["True", "False"], },
    {"id": 54, "text": "I do not conform to typical masculine/feminine behaviors.", "options": ["True", "False"], },
    {"id": 55, "text": "I feel people will take advantage of me if I let them.", "options": ["True", "False"], },
    {"id": 56, "text": "I am troubled by frequent feelings of guilt.", "options": ["True", "False"], },
    {"id": 57, "text": "Others find my beliefs unusual or bizarre.", "options": ["True", "False"], },
    {"id": 58, "text": "I often make impulsive decisions.", "options": ["True", "False"], },
    {"id": 59, "text": "I feel anxious at parties or large gatherings.", "options": ["True", "False"], },
    {"id": 60, "text": "I am rarely free from aches and pains.", "options": ["True", "False"], },
    {"id": 61, "text": "I cry more often than others.", "options": ["True", "False"], },
    {"id": 62, "text": "I often find myself unable to cope with stressful situations.", "options": ["True", "False"], },
    {"id": 63, "text": "I often act without thinking of the consequences.", "options": ["True", "False"], },
    {"id": 64, "text": "Traditional gender roles do not appeal to me.", "options": ["True", "False"], },
    {"id": 65, "text": "I have to be alert or people will deceive me.", "options": ["True", "False"], },
    {"id": 66, "text": "I tend to overanalyze my relationships.", "options": ["True", "False"], },
    {"id": 67, "text": "I have strange thoughts that I cannot explain.", "options": ["True", "False"], },
    {"id": 68, "text": "I have racing thoughts.", "options": ["True", "False"], },
    {"id": 69, "text": "I find it hard to make new friends.", "options": ["True", "False"], },
    {"id": 70, "text": "I find I am susceptible to various illnesses.", "options": ["True", "False"], },
    {"id": 71, "text": "I feel lonely even when I am with people.", "options": ["True", "False"], },
    {"id": 72, "text": "I have episodes of amnesia or forgetting.", "options": ["True", "False"], },
    {"id": 73, "text": "I have been rebellious toward authority figures.", "options": ["True", "False"], },
    {"id": 74, "text": "I question my sexual orientation.", "options": ["True", "False"], },
    {"id": 75, "text": "I feel there are plots to harm me or exclude me.", "options": ["True", "False"], },
    {"id": 76, "text": "I have irrational fears of certain objects or situations.", "options": ["True", "False"], },
    {"id": 77, "text": "I feel very nervous when I am around people.", "options": ["True", "False"], },
    {"id": 78, "text": "I feel a constant high without drugs.", "options": ["True", "False"], },
    {"id": 79, "text": "I prefer reading or solitary hobbies to socializing.", "options": ["True", "False"], },
    {"id": 80, "text": "I believe there is something wrong with my body.", "options": ["True", "False"], },
    {"id": 81, "text": "I feel like a failure.", "options": ["True", "False"], },
    {"id": 82, "text": "I tend to dramatize more than others.", "options": ["True", "False"], },
    {"id": 83, "text": "I have used deceit or lied to get my way.", "options": ["True", "False"], },
    {"id": 84, "text": "I feel pressure to behave in a way that matches my gender.", "options": ["True", "False"], },
    {"id": 85, "text": "Others are responsible for most of my troubles.", "options": ["True", "False"], },
    {"id": 86, "text": "I feel I must follow strict routines..", "options": ["True", "False"], },
    {"id": 87, "text": "I have periods of intense paranoia.", "options": ["True", "False"], },
    {"id": 88, "text": "I can be excessively happy or extremely irritable.", "options": ["True", "False"], },
    {"id": 89, "text": "I feel drained after being in social situations.", "options": ["True", "False"], },
    {"id": 90, "text": "Even minor physical problems make me anxious.", "options": ["True", "False"], },
    {"id": 91, "text": "I have trouble sleeping due to sad thoughts.", "options": ["True", "False"], },
    {"id": 92, "text": "My mood can change very quickly.", "options": ["True", "False"], },
    {"id": 93, "text": "I find it hard to set long-term goals.", "options": ["True", "False"], },
    {"id": 94, "text": "I am sensitive to discussions about gender roles.", "options": ["True", "False"], },
    {"id": 95, "text": "I find it hard to forgive and forget.", "options": ["True", "False"], },
    {"id": 96, "text": "I get stuck on details and miss the broader picture.", "options": ["True", "False"], },
    {"id": 97, "text": "My mood can be unpredictable.", "options": ["True", "False"], },
    {"id": 98, "text": "I often engage in spending sprees.", "options": ["True", "False"], },
    {"id": 99, "text": "I am often happier being alone.", "options": ["True", "False"], }
]

def save_answers_to_csv(answers):
    # Check if the file already exists to determine if we need to write the header
    file_exists = os.path.isfile('answers.csv')
    
    with open('answers.csv', 'a', newline='') as csvfile:
        # Define the column headers for the CSV file
        fieldnames = ['question_id', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        # Write each question ID and answer to the CSV file
        for question_id, answer in answers.items():
            writer.writerow({'question_id': question_id, 'answer': answer})



def get_results_from_csv():
    try:
        df = pd.read_csv('answers.csv')
        result = df['answer'].value_counts().to_dict()
        return result
    except FileNotFoundError:
        return {"error": "Results file not found. Please submit answers first."}

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = detect_face(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')
@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

@app.route('/api/submit', methods=['POST'])
def submit_answers():
    data = request.get_json()
    answers = data['answers']
    save_answers_to_csv(answers)
    return jsonify({"message": "Answers saved"})

@app.route('/api/results', methods=['GET'])
def get_results():
    results = get_results_from_csv()
    return jsonify(results)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # Get form data
    full_name = request.form['full_name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    
    # Create a DataFrame with the form data
    data = {
        'Full Name': [full_name],
        'Email': [email],
        'Phone': [phone],
        'Message': [message]
    }
    df = pd.DataFrame(data)
    
    # Check if the file exists
    file_exists = os.path.isfile('contact_responses.xlsx')
    
    # If the file exists, append the data; otherwise, create a new file
    if file_exists:
        df_existing = pd.read_excel('contact_responses.xlsx')
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        df_combined.to_excel('contact_responses.xlsx', index=False)
    else:
        df.to_excel('contact_responses.xlsx', index=False)
    
    return "Your message has been sent successfully!"

if __name__ == "__main__":
    app.run(debug=True)
