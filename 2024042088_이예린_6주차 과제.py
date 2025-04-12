##############################
#프로그램명: 성적 관리 프로그램
#작성자: 소프트웨어학부 / 이예린
#작성일: 2025-04-12
#프로그램 설명: 
# 1) Student 클래스 정의 : 학생의 학번, 이름, 점수(영어, C-언어, 파이썬), 총점, 평균, 학점, 등수 정보를 저장.
# 2) StudentManagement 클래스 정의 : 학생 목록 관리 및 기능 구현.
# 3) 메뉴 제공 (menu)
# 4) 종료 시 프로그램 종료 메시지 출력
##############################

class Student:
    def __init__(self, 학번, 이름, 영어, C_언어, 파이썬):
        self.학번 = 학번
        self.이름 = 이름
        self.영어 = 영어
        self.C_언어 = C_언어
        self.파이썬 = 파이썬
        self.총점 = 0
        self.평균 = 0
        self.학점 = ''
        self.등수 = 0

    def calculate_total_avg(self):
        self.총점 = self.영어 + self.C_언어 + self.파이썬
        self.평균 = round(self.총점 / 3, 2)

    def calculate_grade(self):
        if self.평균 >= 90:
            self.학점 = 'A'
        elif self.평균 >= 80:
            self.학점 = 'B'
        elif self.평균 >= 70:
            self.학점 = 'C'
        elif self.평균 >= 60:
            self.학점 = 'D'
        else:
            self.학점 = 'F'

class StudentManagement:
    def __init__(self):
        self.students = []

    def input_score(self):
        for i in range(5):
            print(f"\n학생 {i + 1} 정보 입력: ")
            학번 = int(input("학번: "))
            이름 = input("이름: ")
            영어 = float(input("영어: "))
            C_언어 = float(input("C-언어: "))
            파이썬 = float(input("파이썬: "))
            student = Student(학번, 이름, 영어, C_언어, 파이썬)
            self.students.append(student)
        self.update_all()

    def update_all(self):
        for student in self.students:
            student.calculate_total_avg()
            student.calculate_grade()
        self.calculate_rank()

    def calculate_rank(self):
        sorted_students = sorted(self.students, key=lambda x: x.평균, reverse=True)
        for i, student in enumerate(sorted_students):
            if i > 0 and student.평균 == sorted_students[i - 1].평균:
                student.등수 = sorted_students[i - 1].등수
            else:
                student.등수 = i + 1

    def print_results(self):
        print("\n                                                 성적관리 프로그램")
        print("=" * 120)
        print(f"{'학번':<20}{'이름':<10}{'영어':<10}{'C-언어':<10}{'파이썬':<10}{'총점':<10}{'평균':<10}{'학점':<10}{'등수':<10}")
        print("=" * 120)
        for student in self.students:
            print(f"{student.학번:<21}{student.이름:<13}{student.영어:<11}{student.C_언어:<11}{student.파이썬:<12}{student.총점:<10}{student.평균:<17}{student.학점:<13}{student.등수:<15}")

    def insert_student(self):
        print("학생 정보 입력: ")
        학번 = int(input("학번: "))
        이름 = input("이름: ")
        영어 = float(input("영어 점수: "))
        C_언어 = float(input("C-언어 점수: "))
        파이썬 = float(input("파이썬 점수: "))
        student = Student(학번, 이름, 영어, C_언어, 파이썬)
        self.students.append(student)
        self.update_all()
        print("학생 정보가 추가되었습니다.")

    def delete_student(self):
        학번 = int(input("삭제할 학생의 학번: "))
        original_length = len(self.students)
        self.students = [student for student in self.students if student.학번 != 학번]
        if len(self.students) < original_length:
            print("학생 정보가 삭제되었습니다.")
        else:
            print("해당 학번의 학생을 찾을 수 없습니다.")
        self.update_all()

    def search_student(self):
        criteria = input("검색 기준 (학번/이름): ")
        if criteria not in ["학번", "이름"]:
            print("올바른 검색 기준을 입력하세요 (학번/이름).")
            return
        keyword = input("검색어: ")
        results = [student for student in self.students if str(getattr(student, criteria)) == keyword]
        if results:
            print("\n검색 결과:")
            for student in results:
                print(student.__dict__)
        else:
            print("검색 결과가 없습니다.")

    def sort_students_by_total(self):
        self.students.sort(key=lambda x: x.총점, reverse=True)
        print("학생 정보가 총점 기준으로 정렬되었습니다.")
        self.print_results()

    def count_high_achievers(self):
        count = sum(1 for student in self.students if student.평균 >= 80)
        print(f"80점 이상 학생 수: {count}")

    def menu(self):
        while True:
            print("\n메뉴:")
            print("1. 학생 삽입")
            print("2. 학생 삭제")
            print("3. 학생 검색")
            print("4. 총점 정렬")
            print("5. 80점 이상 학생 세기")
            print("6. 성적 출력")
            print("7. 프로그램 종료")

            choice = input("원하는 기능의 번호를 입력하세요: ")

            if choice == '1':
                self.insert_student()
            elif choice == '2':
                self.delete_student()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.sort_students_by_total()
            elif choice == '5':
                self.count_high_achievers()
            elif choice == '6':
                self.print_results()
            elif choice == '7':
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 번호입니다. 다시 입력하세요.")

if __name__ == "__main__":
    sm = StudentManagement()
    sm.input_score()
    sm.menu()
