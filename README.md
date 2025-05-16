# AI Resume Generator

This project can write or tailor resumes and cover letters based on user input to meet different job descriptions, and modify the output by user feedback. Then the resume and cover letter can be downloaded as txt file.

Tech used: ChatGPT (openAI API), streamlit, dock2txt, pdfplumber

To run:
Step1: clone the repository(I made this repo public so it should be fine):
git clone https://github.com/YD293/CS485.git
cd CS485

step 2: create virtual environment
python3 -m venv venv
source venv/bin/activate

step3: install dependencies
pip install -r requirements.txt

step4: the secret key may block the clone and pull request, then a file have to be manually made, and check openai_key and see if they are availiable to use, and then paste into this file:
openai_key.txt

step5: run the app
streamlit run gui.py

OR: another way to run the code
cd dist
./launch_app

step6: input
In the UI, just input everything you want to, file upload is also allowed, and then it will generate the resume or the cover letter. If you dont like the output, you can tell the program where you think it can improve, then it will improve. Finally you can download the output in txt file.
