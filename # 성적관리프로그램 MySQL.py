import mysql.connector # MySQL 데이터베이스와의 연결을 위한 라이브러리 임포트트

# MySQL 연결 설정
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Lyl213711^^",
    "database": "student_management" # 사용할 데이터베이스 이름(사전에 생성되어 있어야 함함)
}

# mysql 데이터베이스에 연결
def get_connection():
    return mysql.connector.connect(**db_config)

# 학생 정보 입력 받는 함수
def input_student():
    print("\n=== 학생 정보 입력 ===")
    id = input("학번: ")
    name = input("이름: ")
    english = int(input("영어 점수: "))
    c = int(input("C-언어 점수: "))
    python = int(input("파이썬 점수: "))
    return id, name, english, c, python

# 세 과목의 점수 이용해 총점, 평균 계산하는 함수
def calculate_total_average(english, c, python):
    total = english + c + python
    average = round(total / 3, 2)
    return total, average

# 평균 -> 학점으로 변환해주는 함수수
def calculate_grade(average):
    if average >= 95:
        return 'A+'
    elif average >= 90:
        return 'A'
    elif average >= 85:
        return 'B+'
    elif average >= 80:
        return 'B'
    elif average >= 75:
        return 'C+'
    elif average >= 70:
        return 'C'
    elif average >= 65:
        return 'D+'
    elif average >= 60:
        return 'D'
    else:
        return 'F'

# 학생 정보를 입력받고 총점, 평균, 학점을 계산한 후 데이터베이스 students 테이블에 삽입하는 함수수
def insert_student():
    conn = get_connection() # 연결 객체 초기화 ?
    cursor = conn.cursor() # 커서 객체 초기화 ?

    id, name, english, c, python = input_student()
    total, average = calculate_total_average(english, c, python)
    grade = calculate_grade(average)
    rank_num = 0  # 일단 0 넣고 나중에 등수 재계산

    sql = """
    INSERT INTO students (id, name, english_score, c_score, python_score, total, average, grade, rank_num)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (id, name, english, c, python, total, average, grade, rank_num))
    conn.commit() # 변경 사항 데이터베이스에 커밋밋

    update_ranks(conn)  # 삽입 후 등수 다시 계산
    print("학생이 추가되었습니다.")

    cursor.close()
    conn.close()

# 학생 정보 삭제 함수
def delete_student():
    conn = get_connection()
    cursor = conn.cursor()

    id = input("삭제할 학생 학번 입력: ")
    sql = "DELETE FROM students WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    update_ranks(conn) # 삭제 후 등수 재계산산

    print("학생이 삭제되었습니다.")
    cursor.close()
    conn.close()

# 학번 학생 정보 탐색 함수
def search_student_by_id():
    conn = get_connection()
    cursor = conn.cursor()

    id = input("검색할 학생 학번 입력: ")
    sql = "SELECT * FROM students WHERE id = %s"
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    display_students(result)

    cursor.close()
    conn.close()

# 이름 학생 정보 탐색 함수
def search_student_by_name():
    conn = get_connection()
    cursor = conn.cursor()

    name = input("검색할 학생 이름 입력: ")
    sql = "SELECT * FROM students WHERE name = %s"
    cursor.execute(sql, (name,))
    result = cursor.fetchall()
    display_students(result)

    cursor.close()
    conn.close()

# 학생 추가, 삭제 시 자동으로 호출되어 등수 최신 상태로 update 해주는 함수수
def update_ranks(conn=None):
    """총점 기준으로 등수 계산 및 DB 업데이트"""
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True
    cursor = conn.cursor()

    cursor.execute("SELECT id, total FROM students ORDER BY total DESC")
    students = cursor.fetchall()

    rank = 1
    prev_total = None
    same_rank_count = 0

    for i, (student_id, total) in enumerate(students):
        if total == prev_total:
            # 같은 점수면 같은 등수
            pass
        else:
            rank = i + 1
        sql_update = "UPDATE students SET rank_num = %s WHERE id = %s"
        cursor.execute(sql_update, (rank, student_id))
        prev_total = total

    conn.commit()
    cursor.close()
    if close_conn:
        conn.close()

# 학생 총점 기준 정렬 함수
def sort_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY total DESC")
    result = cursor.fetchall()
    display_students(result)
    cursor.close()
    conn.close()

# 평균 점수 80점 이상 학생 카운트해주는 함수
def count_above_80():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students WHERE average >= 80")
    (count,) = cursor.fetchone()
    print(f"평균 80점 이상인 학생 수: {count}")
    cursor.close()
    conn.close()

# 조회된 학생 정보 리스트 표 형식으로 출력하는 함수
def display_students(students):
    if not students:
        print("조회된 학생이 없습니다.")
        return

    # 제목 행 (헤더)
    print(f"{'학번':<13} {'이름':<7} {'영어':>6} {'C언어':>6} {'파이썬':>6} {'총점':>6} {'평균':>6} {'학점':>4} {'등수':>4}")
    
    for s in students:
        # s는 튜플: (id, name, english_score, c_score, python_score, total, average, grade, rank_num)
        print(f"{s[0]:<15} {s[1]:<7} {s[2]:>6} {s[3]:>6} {s[4]:>8} {s[5]:>11} {float(s[6]):>10.2f} {s[7]:>4} {s[8]:>4}")

def main():
    while True:
        print("\n===== 학생 성적 관리 프로그램 =====")
        print("1. 학생 추가")
        print("2. 학생 삭제")
        print("3. 학번으로 학생 탐색")
        print("4. 이름으로 학생 탐색")
        print("5. 총점 기준 정렬 출력")
        print("6. 평균 80점 이상 학생 수 카운트")
        print("7. 종료")

        choice = input("선택: ")
        if choice == '1':
            insert_student()
        elif choice == '2':
            delete_student()
        elif choice == '3':
            search_student_by_id()
        elif choice == '4':
            search_student_by_name()
        elif choice == '5':
            sort_students()
        elif choice == '6':
            count_above_80()
        elif choice == '7':
            print("프로그램 종료")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()
