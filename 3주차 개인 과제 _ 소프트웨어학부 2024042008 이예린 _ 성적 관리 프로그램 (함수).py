#성적 관리 프로그램(함수)

# 입력함수
def input_score():
    students = [] # 학생들 데이터 저장할 리스트
    for i in range(5):
        student = {} # 각 학생 정보 저장할 딕셔너리
        print("\n학생", i+1, "정보 입력: ")
        student["학번"] = int(input("학번: "))
        student["이름"] = input("이름: ")
        student["영어"] = float(input("영어: "))
        student["C-언어"] = float(input("C-언어: "))
        student["파이썬"] = float(input("파이썬: "))
        students.append(student)
    return students

# 총점/평균 계산 함수
def total_avg(students):
    for student in students:
        student["총점"] = student["영어"] + student["C-언어"] + student["파이썬"]
        student["평균"] = round(student["총점"] / 3, 2)
    
# 학점계산 함수
def grade(students):
    for student in students:
        avg = student["평균"]
        if avg >= 90:
            student['학점'] = 'A'
        elif avg >= 80:
            student['학점'] = 'B'
        elif avg >= 70:
            student['학점'] = 'C'
        elif avg >= 60:
            student['학점'] = 'D'
        else:
            student['학점'] = 'F'

# 등수계산 함수
def rank(students):
    students_sort = sorted(students, key=lambda x: x["평균"], reverse=True)

    for i, student in enumerate(students_sort):
        if i > 0 and student["평균"] == students_sort[i - 1]["평균"]:
            student["등수"] = students_sort[i - 1]["등수"]
        else:
            student["등수"] = i + 1

    for student in students:
        for sorted_student in students_sort:
            if student["학번"] == sorted_student["학번"]:
                student["등수"] = sorted_student["등수"]
                break


# 출력 함수
def print_results(students):
    print("\n                                                 성적관리 프로그램")
    print("=" * 120)
    print(f"{'학번':<20}{'이름':<10}{'영어':<10}{'C-언어':<10}{'파이썬':<10}{'총점':<10}{'평균':<10}{'학점':<10}{'등수':<10}")
    print("=" * 120)
    for student in students:
        print(f"{student['학번']:<20}{student['이름']:<10}{student['영어']:<10}{student['C-언어']:<10}{student['파이썬']:<10}{student['총점']:<10}{student['평균']:<10}{student['학점']:<10}{student['등수']:<10}")
        
        
students=input_score()
total_avg(students)
grade(students)
rank(students)
print_results(students)
