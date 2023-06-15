import pandas as pd
import streamlit as st
import appFunc as af
import os
import librosa
import soundfile as sf
import time
progress_text = "Prediction in progress. Please wait..."
icons = ['🔈', '🎥', '📕']
options = ['Upload Audio Recording','Upload Video Recording','Candidate Database']
formatted_options = [f'{option} {icon}' for icon, option in zip(icons, options)]
st.set_page_config(page_title='Job Role Recommender',layout='wide')
hide_footer='''
<style>
footer{
visibility:visible;
bottom:10px;
}
footer:after{
content:'Designed by Rishikesh : Version 1.0';
display:block;
position:relative;
color:grey;
}
</style>
'''
st.markdown(hide_footer,unsafe_allow_html=True)
nav=st.sidebar.radio("Navigation",formatted_options)
if 'Upload Audio Recording' in nav:
    allDepts=True
    st.title('Job Role Recommender')
    audio=st.file_uploader('Upload Interview Recording',type=['mp3','wav'])
    deptCh=st.radio('Do you want to predict best department from all available departments?',['Yes','No'],index=0)
    if deptCh=='Yes':
      if st.button('Submit'):
        if audio is None:
            st.error('Upload audio recording !!')
        else:
            if os.path.isfile('/temp_audfile'):
                os.remove('/temp_audfile')
            with open("temp_audfile", "wb") as f:
                f.write(audio.getbuffer())
            abs_path = os.path.abspath("temp_audfile")
            my_bar = st.progress(0, text=progress_text)
            transText = af.getText(abs_path)
            my_bar.progress(25, text=(progress_text+' 25% complete.'))
            DeptId = af.getBestDept(transText, True)
            my_bar.progress(50, text=(progress_text + ' 50% complete.'))
            bestPost = af.getBestPost(transText, DeptId)
            my_bar.progress(75, text=(progress_text + ' 75% complete.'))
            bestqualid, bestqual = af.bestQual(transText)
            my_bar.progress(100, text=(progress_text + ' 100% complete.'))
            st.session_state.status=f'{transText}'
            st.subheader('Department')
            if DeptId == 0:
                st.write('Finance')
                seldept = 'Finance'
            elif DeptId == 1:
                st.write('Human Resources')
                seldept = 'Human Resources'
            elif DeptId == 2:
                st.write('Health Care')
                seldept = 'Health Care'
            elif DeptId == 3:
                st.write('Education')
                seldept = 'Education'
            elif DeptId == 4:
                st.write('Information Technology')
                seldept = 'Information Technology'
            elif DeptId == 5:
                st.write('Manufacturing')
                seldept = 'Manufacturing'
            else:
                st.write('Marketing')
                seldept = 'Marketing'
            af.writeDetails(seldept, bestPost)
            st.subheader('Best Job Role')
            st.write(bestPost)
            st.subheader('Best Quality the candidate possesses')
            st.write(bestqual)
            if bestqualid == 0:
                st.write('The candidate possesses exceptional leadership skills, which in turn can inspire and guide their assigned team towards success.')
            elif bestqualid == 1:
                st.write('The candidate excels in developing collaborative relationships and achieving collective goals.')
            elif bestqualid == 2:
                st.write('The candidate demonstrates exceptional analytical abilities hence he/she can make strategic decision-making and drive business success.')

            elif bestqualid == 3:
                st.write('The candidate is very dependable, and will consistently deliver high-quality work and meet deadlines with precision.')

            elif bestqualid == 4:
                st.write('The candidate possesses strong adaptability skills hence he/she can readily adjust to changing circumstances.')

            elif bestqualid == 5:
                st.write('The candidate showcases exceptional creativity and will consistently develop innovative ideas and solutions to drive growth and success.')

            elif bestqualid == 6:
                st.write('The candidate has exceptional initiative, and can proactively identify opportunities for improvement.')

            elif bestqualid == 7:
                st.write('The candidate excels in communication, has exceptional clarity, empathy, and persuasion to build strong relationships and achieve shared goals.')

            elif bestqualid == 8:
                st.write('The candidate exhibits a strong work ethic, and can consistently go above and beyond to achieve excellence and deliver outstanding results.')

            else:
                st.write('The candidate is highly punctual, consistently meeting deadlines with precision and reliability.')
      if st.button('Get Explanation'):
          try:
              text = st.session_state.status
              af.explainPred(text)
          except:
              st.error('Upload Audio !!')
    else:
      allDepts=False
      deptselect=st.multiselect('Select department(s)',['Finance', 'Human Resources', 'Health Care', 'Education', 'Information Technology','Manufacturing','Marketing'])
      if st.button('Submit'):
          if audio is None:
              st.error('Upload audio recording !!')
          elif len(deptselect)==0:
              st.error('Select Departments !!')
          else:
              if os.path.isfile('/temp_audfile'):
                  os.remove('/temp_audfile')
              with open("temp_audfile", "wb") as f:
                  f.write(audio.getbuffer())
              abs_path = os.path.abspath("temp_audfile")
              my_bar = st.progress(0, text=progress_text)
              transText = af.getText(abs_path)
              my_bar.progress(25, text=(progress_text + ' 25% complete.'))
              DeptId = af.getBestDept(transText, False,deptselect)
              my_bar.progress(50, text=(progress_text + ' 50% complete.'))
              seldept=deptselect[DeptId]
              if deptselect[DeptId]=='Finance':
                  DeptId=0
              elif deptselect[DeptId]=='Human Resources':
                  DeptId=1
              elif deptselect[DeptId]=='Health Care':
                  DeptId=2
              elif deptselect[DeptId]=='Education':
                  DeptId=3
              elif deptselect[DeptId]=='Information Technology':
                  DeptId=4
              elif deptselect[DeptId]=='Manufacturing':
                  DeptId=5
              else:
                  DeptId=6
              bestPost = af.getBestPost(transText, DeptId)
              af.writeDetails(seldept, bestPost)
              my_bar.progress(75, text=(progress_text + ' 75% complete.'))
              bestqualid, bestqual = af.bestQual(transText)
              my_bar.progress(100, text=(progress_text + ' 100% complete.'))
              st.session_state.status = f'{transText}'
              st.subheader('Department')
              st.write(seldept)
              st.subheader('Best Job Role')
              st.write(bestPost)
              st.subheader('Best Quality the candidate possesses')
              st.write(bestqual)
              if bestqualid == 0:
                  st.write(
                      'The candidate possesses exceptional leadership skills, which in turn can inspire and guide their assigned team towards success.')
              elif bestqualid == 1:
                  st.write(
                      'The candidate excels in developing collaborative relationships and achieving collective goals.')
              elif bestqualid == 2:
                  st.write(
                      'The candidate demonstrates exceptional analytical abilities hence he/she can make strategic decision-making and drive business success.')

              elif bestqualid == 3:
                  st.write(
                      'The candidate is very dependable, and will consistently deliver high-quality work and meet deadlines with precision.')

              elif bestqualid == 4:
                  st.write(
                      'The candidate possesses strong adaptability skills hence he/she can readily adjust to changing circumstances.')

              elif bestqualid == 5:
                  st.write(
                      'The candidate showcases exceptional creativity and will consistently develop innovative ideas and solutions to drive growth and success.')

              elif bestqualid == 6:
                  st.write(
                      'The candidate has exceptional initiative, and can proactively identify opportunities for improvement.')

              elif bestqualid == 7:
                  st.write(
                      'The candidate excels in communication, has exceptional clarity, empathy, and persuasion to build strong relationships and achieve shared goals.')

              elif bestqualid == 8:
                  st.write(
                      'The candidate exhibits a strong work ethic, and can consistently go above and beyond to achieve excellence and deliver outstanding results.')

              else:
                  st.write(
                      'The candidate is highly punctual, consistently meeting deadlines with precision and reliability.')
      if st.button('Get Explanation'):
          if allDepts == False:
              st.error('The explanation may be incorrect, hence the Get Explanation button is disabled')
          else:
              try:
                  text = st.session_state.status
                  af.explainPred(text)
              except:
                  st.error('Upload Audio !!')

elif 'Upload Video Recording' in nav:
    allDepts=True
    st.title('Job Role Recommender')
    video=st.file_uploader('Upload Interview Recording',type='mp4')
    deptCh=st.radio('Do you want to predict best department from all available departments?',['Yes','No'],index=0)
    if deptCh=='Yes':
      if st.button('Submit'):
        if video is None:
            st.error('Upload video recording !!')
        else:
            if os.path.isfile('/temp_vidfile'):
                os.remove('/temp_vidfile')
            with open("temp_vidfile", "wb") as f:
                f.write(video.getbuffer())
            vidFile=os.path.abspath("temp_vidfile")
            my_bar = st.progress(0, text=progress_text)
            transText = af.getText(vidFile)
            my_bar.progress(25, text=(progress_text+' 25% complete.'))
            DeptId = af.getBestDept(transText, True)
            my_bar.progress(50, text=(progress_text + ' 50% complete.'))
            bestPost = af.getBestPost(transText, DeptId)
            my_bar.progress(75, text=(progress_text + ' 75% complete.'))
            bestqualid, bestqual = af.bestQual(transText)
            my_bar.progress(100, text=(progress_text + ' 100% complete.'))
            st.session_state.status=f'{transText}'
            st.subheader('Department')
            if DeptId == 0:
                st.write('Finance')
                seldept='Finance'
            elif DeptId == 1:
                st.write('Human Resources')
                seldept = 'Human Resources'
            elif DeptId == 2:
                st.write('Health Care')
                seldept = 'Health Care'
            elif DeptId == 3:
                st.write('Education')
                seldept = 'Education'
            elif DeptId == 4:
                st.write('Information Technology')
                seldept = 'Information Technology'
            elif DeptId == 5:
                st.write('Manufacturing')
                seldept = 'Manufacturing'
            else:
                st.write('Marketing')
                seldept = 'Marketing'
            af.writeDetails(seldept,bestPost)
            st.subheader('Best Job Role')
            st.write(bestPost)
            st.subheader('Best Quality the candidate possesses')
            st.write(bestqual)
            if bestqualid == 0:
                st.write('The candidate possesses exceptional leadership skills, which in turn can inspire and guide their assigned team towards success.')
            elif bestqualid == 1:
                st.write('The candidate excels in developing collaborative relationships and achieving collective goals.')
            elif bestqualid == 2:
                st.write('The candidate demonstrates exceptional analytical abilities hence he/she can make strategic decision-making and drive business success.')

            elif bestqualid == 3:
                st.write('The candidate is very dependable, and will consistently deliver high-quality work and meet deadlines with precision.')

            elif bestqualid == 4:
                st.write('The candidate possesses strong adaptability skills hence he/she can readily adjust to changing circumstances.')

            elif bestqualid == 5:
                st.write('The candidate showcases exceptional creativity and will consistently develop innovative ideas and solutions to drive growth and success.')

            elif bestqualid == 6:
                st.write('The candidate has exceptional initiative, and can proactively identify opportunities for improvement.')

            elif bestqualid == 7:
                st.write('The candidate excels in communication, has exceptional clarity, empathy, and persuasion to build strong relationships and achieve shared goals.')

            elif bestqualid == 8:
                st.write('The candidate exhibits a strong work ethic, and can consistently go above and beyond to achieve excellence and deliver outstanding results.')

            else:
                st.write('The candidate is highly punctual, consistently meeting deadlines with precision and reliability.')
      if st.button('Get Explanation'):
          try:
              text = st.session_state.status
              af.explainPred(text)
          except:
              st.error('Upload Video !!')
    else:
      allDepts=False
      deptselect=st.multiselect('Select department(s)',['Finance', 'Human Resources', 'Health Care', 'Education', 'Information Technology','Manufacturing','Marketing'])
      if st.button('Submit'):
          if video is None:
              st.error('Upload video recording !!')
          elif len(deptselect)==0:
              st.error('Select Departments !!')
          else:
              if os.path.isfile('/temp_vidfile'):
                  os.remove('/temp_vidfile')
              with open("temp_vidfile", "wb") as f:
                  f.write(video.getbuffer())
              vidFile = os.path.abspath("temp_vidfile")
              my_bar = st.progress(0, text=progress_text)
              transText = af.getText(vidFile)
              my_bar.progress(25, text=(progress_text + ' 25% complete.'))
              DeptId = af.getBestDept(transText, False,deptselect)
              my_bar.progress(50, text=(progress_text + ' 50% complete.'))
              seldept=deptselect[DeptId]
              if deptselect[DeptId]=='Finance':
                  DeptId=0
              elif deptselect[DeptId]=='Human Resources':
                  DeptId=1
              elif deptselect[DeptId]=='Health Care':
                  DeptId=2
              elif deptselect[DeptId]=='Education':
                  DeptId=3
              elif deptselect[DeptId]=='Information Technology':
                  DeptId=4
              elif deptselect[DeptId]=='Manufacturing':
                  DeptId=5
              else:
                  DeptId=6
              bestPost = af.getBestPost(transText, DeptId)
              my_bar.progress(75, text=(progress_text + ' 75% complete.'))
              af.writeDetails(seldept,bestPost)
              bestqualid, bestqual = af.bestQual(transText)
              my_bar.progress(100, text=(progress_text + ' 100% complete.'))
              st.session_state.status = f'{transText}'
              st.subheader('Department')
              st.write(seldept)
              st.subheader('Best Job Role')
              st.write(bestPost)
              st.subheader('Best Quality the candidate possesses')
              st.write(bestqual)
              if bestqualid == 0:
                  st.write(
                      'The candidate possesses exceptional leadership skills, which in turn can inspire and guide their assigned team towards success.')
              elif bestqualid == 1:
                  st.write(
                      'The candidate excels in developing collaborative relationships and achieving collective goals.')
              elif bestqualid == 2:
                  st.write(
                      'The candidate demonstrates exceptional analytical abilities hence he/she can make strategic decision-making and drive business success.')

              elif bestqualid == 3:
                  st.write(
                      'The candidate is very dependable, and will consistently deliver high-quality work and meet deadlines with precision.')

              elif bestqualid == 4:
                  st.write(
                      'The candidate possesses strong adaptability skills hence he/she can readily adjust to changing circumstances.')

              elif bestqualid == 5:
                  st.write(
                      'The candidate showcases exceptional creativity and will consistently develop innovative ideas and solutions to drive growth and success.')

              elif bestqualid == 6:
                  st.write(
                      'The candidate has exceptional initiative, and can proactively identify opportunities for improvement.')

              elif bestqualid == 7:
                  st.write(
                      'The candidate excels in communication, has exceptional clarity, empathy, and persuasion to build strong relationships and achieve shared goals.')

              elif bestqualid == 8:
                  st.write(
                      'The candidate exhibits a strong work ethic, and can consistently go above and beyond to achieve excellence and deliver outstanding results.')

              else:
                  st.write(
                      'The candidate is highly punctual, consistently meeting deadlines with precision and reliability.')
      if st.button('Get Explanation'):
          if allDepts==False:
              st.error('The explanation may be incorrect, hence the Get Explanation button is disabled')
          else:
              try:
                  text = st.session_state.status
                  af.explainPred(text)
              except:
                  st.error('Upload Video !!')


elif 'Candidate Database' in nav:
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)




    st.title('Candidate Database')
    df=pd.read_csv('/Users/rishi/PycharmProjects/JobRoleRecommender/venv/CandDB.csv',dtype={'Candidate ID': int})
    st.table(df)