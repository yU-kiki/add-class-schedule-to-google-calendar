# シラバスからcsvファイルを作成する

import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://syllabus.sfc.keio.ac.jp/courses?button=&locale=ja&page={}&search%5Bsemester%5D=&search%5Bsfc_guide_title%5D=&search%5Bsub_semester%5D=&search%5Bsummary%5D=&search%5Bteacher_name%5D=&search%5Btitle%5D=&search%5Byear%5D=2023'

header = ['コース名', '学部・研究科', '登録番号', '科目ソート', '分野', '単位', '開講年度・学期', '授業教員名', '実施形態', '授業形態', '曜日・時限', '授業で使う言語', '研究会テーマ', '概要', '詳細URL']
# CSVファイルを作成し、ヘッダー行とデータ行を書き込む
with open('syllabus.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for page in range(1, 55):
        url = base_url.format(page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result_div = soup.find("div", {"class": "result"})
        uls = result_div.find('ul')
        lis = uls.find_all('li')
        for li in lis:
          # 目的の要素を指定して、内容を取得する
          course_name_elem = li.find('h2')
          course_name = course_name_elem.text if course_name_elem else ''

          faculty_elem = li.find('dt', text='学部・研究科')
          faculty = faculty_elem.find_next_sibling('dd').text if faculty_elem else ''

          registration_number_elem = li.find('dt', text='登録番号')
          registration_number = registration_number_elem.find_next_sibling('dd').text if registration_number_elem else ''

          subject_sort_elem = li.find('dt', text='科目ソート')
          subject_sort = subject_sort_elem.find_next_sibling('dd').text if subject_sort_elem else ''

          field_elem = li.find('dt', text='分野')
          field = field_elem.find_next_sibling('dd').text if field_elem else ''

          unit_elem = li.find('dt', text='単位')
          unit = unit_elem.find_next_sibling('dd').text if unit_elem else ''

          term_elem = li.find('dt', text='開講年度・学期')
          term = term_elem.find_next_sibling('dd').text if term_elem else ''

          instructor_elem = li.find('dt', text='授業教員名')
          instructor = instructor_elem.find_next_sibling('dd').text.replace(" ", "") if instructor_elem else ''

          hidden_field = li.find('div', {'class': 'hidden-field'})

          if hidden_field is None:
            writer.writerow([course_name, faculty, registration_number, subject_sort, field, unit, term, instructor])

          else:

            syllabus = li.find('div', {'class': 'syllabus-info'})
            outline = li.find('div', {'class': 'outline'})

            implementation_form_elem = syllabus.find('dt', text='実施形態')
            implementation_form = implementation_form_elem.find_next_sibling('dd').text.replace(" ", "") if implementation_form_elem else ''
  
            class_style_elem = syllabus.find('dt', text='授業形態')
            class_style = class_style_elem.find_next_sibling('dd').text.replace(" ", "") if class_style_elem else ''
  
            day_and_time_elem = syllabus.find('dt', text='曜日・時限')
            day_and_time = day_and_time_elem.find_next_sibling('dd').text.replace(" ", "") if day_and_time_elem else ''
  
            language_used_elem = syllabus.find('dt', text='授業で使う言語')
            language_used = language_used_elem.find_next_sibling('dd').text.replace(" ", "") if language_used_elem else ''

            theme_elem = syllabus.find('dt', text='研究会テーマ')
            theme = theme_elem.find_next_sibling('dd').text.replace(" ", "") if theme_elem else ''

            outline_elem = outline.find('p')
            outline = outline_elem.text if outline_elem else ''

            detail_url_elem = li.find('a', {'class': 'detail-btn'})['href']
            detail_url = 'https://syllabus.sfc.keio.ac.jp' + detail_url_elem if detail_url_elem else ''
            
            writer.writerow([course_name, faculty, registration_number, subject_sort, field, unit, term, instructor, implementation_form, class_style, day_and_time, language_used, theme, outline, detail_url])
