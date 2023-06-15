from pytube import YouTube
import torch
import os
from transformers import pipeline
import whisper
import re
import numpy as np
import webbrowser
import math
model=whisper.load_model('small')
import pandas as pd
import string
import csv
from moviepy.editor import VideoFileClip
import sys
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
departmentId=0
predSc=[]
predLa=[]
class Classifier:
  def __init__(self, pipeline):
    self.pipeline = pipeline

  def predict_proba(self, text):
    print('-')
    return np.array(classifier(text,departments)['scores'])
      #sent=t.split('.')
      #for eachSent in sent:
      #  for word in l:
      #    print(word)
      #    sentwordlist=eachSent.split()
      #    for sentword in sentwordlist:
      #      if isinstance(word, str):
      #        sentword=sentword.lower()
      #        if word.lower() in sentword:
      #          res=classifier(eachSent,departments)['scores']
      #          for i in range(7):
      #            s[i]+=res[i]
      #          n+=1
    #s= [elt/n for elt in s]
    #print(s)
    #return np.array(s)
def getColVals(csvfile,colname):
  df=pd.read_csv(csvfile)
  colvals=df[colname].tolist()
  return colvals

def find_max_value(csv_file, column_name):
  with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    max_value = float('-inf')  # Initialize with negative infinity
    rows = list(reader)
    if len(rows) == 0:
      return 0
    else:
      for row in rows:
        value = float(row[column_name])
        max_value = max(max_value, value)
  return int(max_value)

def writeTocsv(csv_file,data):
  with open(csv_file, 'a',newline='') as f:
    if f.tell() != 0:
      f.write('\n')
    writer = csv.writer(f)
    writer.writerow(data)

def highlight_text(paragraph, words):
  modwords=[word.lower() for word in words]
  newmod=[]
  for word in modwords:
    string=word.split()
    if len(string)>2:
      newmod.append(s for s in string)
    else:
      newmod.append(word)
  modparagraph=paragraph.lower()
  orgPara=modparagraph
  modPara=re.findall(r'\b\w+\b',modparagraph)
  modPara = set(modPara)
  modwords = set(newmod)
  common_words = modPara.intersection(modwords)
  for word in common_words:
    orgPara = orgPara.replace(word, f"<span style='background-color:yellow'>{word}</span>")
  orgPara=orgPara.split(".")
  orgPara=[newl.strip().capitalize() for newl in orgPara]
  return '. '.join(orgPara)

finposts=['Payroll Clerk','Financial Manager','Finance Advisor Assistant','Management analyst','Junior Financial analyst','Financial examiner','Budget analyst','Accountant','Treasurer','Economist']
hrposts=['Compensation Manager','Assessment Consultant','Training Manager','Labor Relations Manager','Talent Officer','Health, Safety and Environment advisor','Administrative Assistant','Resources Manager','Facilities manager','Human Resources Associate']
healthposts=['Home Health Aide','Physician Assistant','Nursing Assistant','Psychologist','Nutritionist','Pharmacist','Dentist','Paediatrician','Chiropractor','Veterinarian']
edposts=['Teacher', 'Professor', 'School Administrator', 'Guidance Counselor', 'Curriculum Developer', 'Sports Coach', 'Special Education Teacher', 'Librarian', 'Admissions Counselor', 'Education Consultant']
csposts=['Software Engineer', 'Data Scientist', 'Network Administrator', 'Database Administrator', 'Cybersecurity Analyst', 'Machine Learning Engineer', 'Web Developer', 'Systems Analyst', 'Mobile App Developer', 'Artificial Intelligence Researcher']
manuposts=['Production Supervisor', 'Machine Operator', 'Quality Control Technician', 'Assembly Technician', 'Maintenance Technician', 'Manufacturing Engineer', 'Warehouse Manager', 'Purchasing Agent', 'Logistics Coordinator', 'Inventory Control Specialist']
marposts=['Marketing Manager', 'Marketing Coordinator', 'Social Media Manager', 'Content Marketing Specialist', 'Email Marketing Manager', 'Marketing Analyst', 'Product Marketing Manager', 'Digital Marketing Manager', 'Brand Manager', 'Search Engine Optimization Specialist']
scores=None
ordDepts=None
def getTextFromAudio(ytlink):
    yt=YouTube(ytlink)
    aud=yt.streams.filter(only_audio=True).first()
    out_aud=aud.download('/venv/Interview Files')
    name, ext=os.path.splitext(out_aud)
    newout_aud='Interview Audio.wav'
    os.rename(out_aud,newout_aud)
    result=model.transcribe(newout_aud,fp16=False)
    return result['text']

def getText(file):
  result=model.transcribe(file,fp16=False)
  return result['text']

def getBestDept(text,predAllDept,deptChoices=None):
  global departmentId
  global predSc
  global predLa
  if predAllDept and deptChoices==None:
    departments = ['Finance', 'Human Resources', 'Health Care', 'Education', 'Information Technology', 'Manufacturing',
                   'Marketing']
    counter = [0, 0, 0, 0, 0, 0, 0]
    res=classifier(text,departments)
    predSc=res['scores']
    predLa=res['labels']
    if res['labels'][0]==departments[0]:
      counter[0]=1
    elif res['labels'][0]==departments[1]:
      counter[1]=1
    elif res['labels'][0]==departments[2]:
      counter[2]=1
    elif res['labels'][0]==departments[3]:
      counter[3]=1
    elif res['labels'][0]==departments[4]:
      counter[4]=1
    elif res['labels'][0]==departments[5]:
      counter[5]=1
    else:
      counter[6]=1
    for deptid in range(len(counter)):
      if counter[deptid] == 1:
        departmentId = deptid
        return deptid
  else:
    departments=[]
    counter=[0]*len(deptChoices)
    for i in range(len(deptChoices)):
      departments.append(deptChoices[i])
    res=classifier(text,departments)
    predSc = res['scores']
    predLa = res['labels']
    for i in range(len(deptChoices)):
      if res['labels'][0]==departments[i]:
        counter[i]=1
    for deptid in range(len(counter)):
      if counter[deptid] == 1:
        departmentId = deptid
        return deptid


def convert_video_to_audio_moviepy(video_file, output_ext="mp3"):
  """Converts video to audio using MoviePy library
  that uses `ffmpeg` under the hood"""
  filename, ext = os.path.splitext(video_file)
  output_file = f"{filename}.{output_ext}"
  clip = VideoFileClip(video_file)
  clip.audio.write_audiofile(output_file)
  return output_file


def getBestPost(text,deptid):
  if deptid==0:
    cfin=[0,0,0,0,0,0,0,0,0,0]
    res=classifier(text,finposts)
    if res['labels'][0]==finposts[0]:
      cfin[0]+=1
    elif res['labels'][0]==finposts[1]:
      cfin[1]+=1
    elif res['labels'][0]==finposts[2]:
      cfin[2]+=1
    elif res['labels'][0]==finposts[3]:
      cfin[3]+=1
    elif res['labels'][0]==finposts[4]:
      cfin[4]+=1
    elif res['labels'][0]==finposts[5]:
      cfin[5]+=1
    elif res['labels'][0]==finposts[6]:
      cfin[6]+=1
    elif res['labels'][0]==finposts[7]:
      cfin[7]+=1
    elif res['labels'][0]==finposts[8]:
      cfin[8]+=1
    else:
      cfin[9]+=1
    for i in range(10):
      if cfin[i]==1:
        return finposts[i]
  elif deptid==1:
    chr=[0,0,0,0,0,0,0,0,0,0]
    res=classifier(text,hrposts)
    if res['labels'][0]==hrposts[0]:
      chr[0]+=1
    elif res['labels'][0]==hrposts[1]:
      chr[1]+=1
    elif res['labels'][0]==hrposts[2]:
      chr[2]+=1
    elif res['labels'][0]==hrposts[3]:
      chr[3]+=1
    elif res['labels'][0]==hrposts[4]:
      chr[4]+=1
    elif res['labels'][0]==hrposts[5]:
      chr[5]+=1
    elif res['labels'][0]==hrposts[6]:
      chr[6]+=1
    elif res['labels'][0]==hrposts[7]:
      chr[7]+=1
    elif res['labels'][0]==hrposts[8]:
      chr[8]+=1
    else:
      chr[9]+=1
    for i in range(10):
      if chr[i]==1:
        return hrposts[i]
  elif deptid==2:
    chealth=[0,0,0,0,0,0,0,0,0,0]
    res=classifier(text,healthposts)
    if res['labels'][0]==healthposts[0]:
      chealth[0]+=1
    elif res['labels'][0]==healthposts[1]:
      chealth[1]+=1
    elif res['labels'][0]==healthposts[2]:
      chealth[2]+=1
    elif res['labels'][0]==healthposts[3]:
      chealth[3]+=1
    elif res['labels'][0]==healthposts[4]:
      chealth[4]+=1
    elif res['labels'][0]==healthposts[5]:
      chealth[5]+=1
    elif res['labels'][0]==healthposts[6]:
      chealth[6]+=1
    elif res['labels'][0]==healthposts[7]:
      chealth[7]+=1
    elif res['labels'][0]==healthposts[8]:
      chealth[8]+=1
    else:
      chealth[9]+=1
    for i in range(10):
      if chealth[i]==1:
        return healthposts[i]
  elif deptid==3:
    ced=[0,0,0,0,0,0,0,0,0,0]
    res=classifier(text,edposts)
    if res['labels'][0]==edposts[0]:
      ced[0]+=1
    elif res['labels'][0]==edposts[1]:
      ced[1]+=1
    elif res['labels'][0]==edposts[2]:
      ced[2]+=1
    elif res['labels'][0]==edposts[3]:
      ced[3]+=1
    elif res['labels'][0]==edposts[4]:
      ced[4]+=1
    elif res['labels'][0]==edposts[5]:
      ced[5]+=1
    elif res['labels'][0]==edposts[6]:
      ced[6]+=1
    elif res['labels'][0]==edposts[7]:
      ced[7]+=1
    elif res['labels'][0]==edposts[8]:
      ced[8]+=1
    else:
      ced[9]+=1
    for i in range(10):
      if ced[i]==1:
        return edposts[i]
  elif deptid==4:
    ccs=[0,0,0,0,0,0,0,0,0,0]
    res=classifier(text,csposts)
    if res['labels'][0]==csposts[0]:
      ccs[0]+=1
    elif res['labels'][0]==csposts[1]:
      ccs[1]+=1
    elif res['labels'][0]==csposts[2]:
      ccs[2]+=1
    elif res['labels'][0]==csposts[3]:
      ccs[3]+=1
    elif res['labels'][0]==csposts[4]:
      ccs[4]+=1
    elif res['labels'][0]==csposts[5]:
      ccs[5]+=1
    elif res['labels'][0]==csposts[6]:
      ccs[6]+=1
    elif res['labels'][0]==csposts[7]:
      ccs[7]+=1
    elif res['labels'][0]==csposts[8]:
      ccs[8]+=1
    else:
      ccs[9]+=1
    for i in range(10):
      if ccs[i]==1:
        return csposts[i]
  elif deptid==5:
    cman=[0,0,0,0,0,0,0,0,0,0]
    res=classifier(text,manuposts)
    if res['labels'][0]==manuposts[0]:
      cman[0]+=1
    elif res['labels'][0]==manuposts[1]:
      cman[1]+=1
    elif res['labels'][0]==manuposts[2]:
      cman[2]+=1
    elif res['labels'][0]==manuposts[3]:
      cman[3]+=1
    elif res['labels'][0]==manuposts[4]:
      cman[4]+=1
    elif res['labels'][0]==manuposts[5]:
      cman[5]+=1
    elif res['labels'][0]==manuposts[6]:
      cman[6]+=1
    elif res['labels'][0]==manuposts[7]:
      cman[7]+=1
    elif res['labels'][0]==manuposts[8]:
      cman[8]+=1
    else:
      cman[9]+=1
    for i in range(10):
      if cman[i]==1:
        return manuposts[i]
  else:
    cmar=[0,0,0,0,0,0,0,0,0,0]
    res=classifier(text,marposts)
    if res['labels'][0]==marposts[0]:
      cmar[0]+=1
    elif res['labels'][0]==marposts[1]:
      cmar[1]+=1
    elif res['labels'][0]==marposts[2]:
      cmar[2]+=1
    elif res['labels'][0]==marposts[3]:
      cmar[3]+=1
    elif res['labels'][0]==marposts[4]:
      cmar[4]+=1
    elif res['labels'][0]==marposts[5]:
      cmar[5]+=1
    elif res['labels'][0]==marposts[6]:
      cmar[6]+=1
    elif res['labels'][0]==marposts[7]:
      cmar[7]+=1
    elif res['labels'][0]==marposts[8]:
      cmar[8]+=1
    else:
      cmar[9]+=1
    for i in range(10):
      if cmar[i]==1:
        return marposts[i]

def bestQual(text):
  qualities=['Leadership','Teamwork','Analytical skills','Dependability','Adaptablity','Creativity','Initiative','Communication skills','Strong work ethic','Punctuality']
  cqual=[0,0,0,0,0,0,0,0,0,0]
  res=classifier(text,qualities)
  if res['labels'][0]==qualities[0]:
    cqual[0]+=1
  elif res['labels'][0]==qualities[1]:
    cqual[1]+=1
  elif res['labels'][0]==qualities[2]:
    cqual[2]+=1
  elif res['labels'][0]==qualities[3]:
    cqual[3]+=1
  elif res['labels'][0]==qualities[4]:
    cqual[4]+=1
  elif res['labels'][0]==qualities[5]:
    cqual[5]+=1
  elif res['labels'][0]==qualities[6]:
    cqual[6]+=1
  elif res['labels'][0]==qualities[7]:
    cqual[7]+=1
  elif res['labels'][0]==qualities[8]:
    cqual[8]+=1
  else:
    cqual[9]+=1
  for i in range(10):
    if cqual[i]==1:
      return i,qualities[i]

def writeDetails(dept,role):
  maxId = find_max_value('CandDB.csv', 'Candidate ID')
  newDetails = [maxId + 1, dept, role]
  writeTocsv('CandDB.csv', newDetails)



def explainPred(text):
  global departmentId
  global predSc
  global predLa
  fileName = '/Users/rishi/PycharmProjects/JobRoleRecommender/venv/Job dept with keywords data.csv'
  if departmentId == 0:
    l = getColVals(fileName, "Business, Finance, Law")
  elif departmentId == 1:
    l = getColVals(fileName, "Customer Service, Retail, Human Resources, Tourism")
  elif departmentId == 2:
    l = getColVals(fileName, "Health Care, Medicine")
  elif departmentId == 3:
    l = getColVals(fileName, "Education")
  elif departmentId == 4:
    l = getColVals(fileName, "Information Technology, Computer Science")
  elif departmentId == 5:
    l = getColVals(fileName, "Manufacturing, Transportation")
  else:
    l = getColVals(fileName, "Marketing, Media, Publishing, Graphic Design")
  l = [x for x in l if str(x) != 'nan']
  if os.path.isfile('output.html'):
    os.remove('output.html')
  html1text=f'''<html>
  <title>Explanation</title>
<body>
<h2>Predicted probabilities</h2>'''
  if len(predSc)==7:
    predProb = f'''<table>
      <tr>
        <td>{predLa[0]}</td>
        <td>
          <div style='background-color:lightblue; width:{predSc[0] * 200}px'>&nbsp;</div></td>
       <td>{round((predSc[0] * 100), 2)}%</td>
      </tr>
      <tr>
        <td>{predLa[1]}</td>
        <td>
          <div style='background-color:lime; width:{predSc[1] * 200}px'>&nbsp;</div></td>
       <td>{round((predSc[1] * 100), 2)}%</td>
      </tr>
  	<tr>
        <td>{predLa[2]}</td>
        <td>
          <div style='background-color:pink; width:{predSc[2] * 200}px'>&nbsp;</div></td>
       <td>{round((predSc[2] * 100), 2)}%</td>
      </tr>
  <tr>
        <td>{predLa[3]}</td>
        <td>
          <div style='background-color:yellow; width:{predSc[3] * 200}px'>&nbsp;</div></td>
       <td>{round((predSc[3] * 100), 2)}%</td>
      </tr>
  <tr>
        <td>Others</td>
        <td>
          <div style='background-color:aquamarine; width:{(predSc[4] + predSc[5] + predSc[6]) * 200}px'>&nbsp;</div></td>
       <td>{round(((predSc[4] + predSc[5] + predSc[6]) * 100), 2)}%</td>
      </tr>
    </table>
  '''
  elif len(predSc)==6:
    predProb = f'''<table>
          <tr>
            <td>{predLa[0]}</td>
            <td>
              <div style='background-color:lightblue; width:{predSc[0] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[0] * 100), 2)}%</td>
          </tr>
          <tr>
            <td>{predLa[1]}</td>
            <td>
              <div style='background-color:lime; width:{predSc[1] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[1] * 100), 2)}%</td>
          </tr>
      	<tr>
            <td>{predLa[2]}</td>
            <td>
              <div style='background-color:pink; width:{predSc[2] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[2] * 100), 2)}%</td>
          </tr>
      <tr>
      <tr>
            <td>{predLa[3]}</td>
            <td>
              <div style='background-color:yellow; width:{predSc[3] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[3] * 100), 2)}%</td>
          </tr>
      <tr>
            <td>Others</td>
            <td>
              <div style='background-color:aquamarine; width:{(predSc[4]+predSc[5]) * 200}px'>&nbsp;</div></td>
           <td>{round(((predSc[4]+predSc[5]) * 100), 2)}%</td>
          </tr>
      <tr>
        </table>
      '''
  elif len(predSc)==5:
    predProb = f'''<table>
          <tr>
            <td>{predLa[0]}</td>
            <td>
              <div style='background-color:lightblue; width:{predSc[0] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[0] * 100), 2)}%</td>
          </tr>
          <tr>
            <td>{predLa[1]}</td>
            <td>
              <div style='background-color:lime; width:{predSc[1] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[1] * 100), 2)}%</td>
          </tr>
          <tr>
            <td>{predLa[2]}</td>
            <td>
              <div style='background-color:pink; width:{predSc[2] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[2] * 100), 2)}%</td>
          </tr>
          <tr>
            <td>{predLa[3]}</td>
            <td>
              <div style='background-color:yellow; width:{predSc[3] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[3] * 100), 2)}%</td>
          </tr>
      	<tr>
            <td>{predLa[4]}</td>
            <td>
              <div style='background-color:aquamarine; width:{predSc[4] * 200}px'>&nbsp;</div></td>
           <td>{round((predSc[4] * 100), 2)}%</td>
          </tr>
        </table>
      '''
  elif len(predSc)==4:
    predProb = f'''<table>
              <tr>
                <td>{predLa[0]}</td>
                <td>
                  <div style='background-color:lightblue; width:{predSc[0] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[0] * 100), 2)}%</td>
              </tr>
              <tr>
                <td>{predLa[1]}</td>
                <td>
                  <div style='background-color:lime; width:{predSc[1] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[1] * 100), 2)}%</td>
              </tr>
              <tr>
                <td>{predLa[2]}</td>
                <td>
                  <div style='background-color:pink; width:{predSc[2] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[2] * 100), 2)}%</td>
              </tr>
              <tr>
                <td>{predLa[3]}</td>
                <td>
                  <div style='background-color:yellow; width:{predSc[3] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[3] * 100), 2)}%</td>
              </tr>
            </table>
          '''
  elif len(predSc)==3:
    predProb = f'''<table>
              <tr>
                <td>{predLa[0]}</td>
                <td>
                  <div style='background-color:lightblue; width:{predSc[0] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[0] * 100), 2)}%</td>
              </tr>
              <tr>
                <td>{predLa[1]}</td>
                <td>
                  <div style='background-color:lime; width:{predSc[1] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[1] * 100), 2)}%</td>
              </tr>
              <tr>
                <td>{predLa[2]}</td>
                <td>
                  <div style='background-color:pink; width:{predSc[2] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[2] * 100), 2)}%</td>
              </tr>
            </table>
          '''
  else:
    predProb = f'''<table>
              <tr>
                <td>{predLa[0]}</td>
                <td>
                  <div style='background-color:lightblue; width:{predSc[0] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[0] * 100), 2)}%</td>
              </tr>
              <tr>
                <td>{predLa[1]}</td>
                <td>
                  <div style='background-color:lime; width:{predSc[1] * 200}px'>&nbsp;</div></td>
               <td>{round((predSc[1] * 100), 2)}%</td>
              </tr>
            </table>
          '''
  htext='<h2>Transcript with highlighted text</h2>'
  endText='''</body>
  </html>'''
  html=highlight_text(text, l)
  with open("output.html", "w") as f:
     f.write(html1text+predProb+htext+html+endText)
     f.close()
  webbrowser.open('file:///Users/rishi/PycharmProjects/JobRoleRecommender/venv/output.html')
  #for word, weight in important_words:
  #  text = text.replace(word, f"<span style='background-color:yellow'>{word}</span>")
  #st.markdown(text,unsafe_allow_html=True)
