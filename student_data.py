# 学生数据管理
# 用于存储和管理学生信息

import json
import os
from datetime import datetime

# 数据文件路径
STUDENT_DATA_FILE = "student_data.json"


# 学生数据结构
def load_student_data():
    """从文件加载学生数据"""
    if os.path.exists(STUDENT_DATA_FILE):
        try:
            with open(STUDENT_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []


def save_student_data(students):
    """保存学生数据到文件"""
    with open(STUDENT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


# 初始化学生数据
students = load_student_data()


def add_student(student_info):
    """
    添加新学生

    Args:
        student_info (dict): 学生信息，包含name, age, grade, class_name等

    Returns:
        dict: 添加结果
    """
    # 生成学生ID
    student_id = str(len(students) + 1).zfill(4)

    student = {
        "id": student_id,
        "name": student_info.get("name", ""),
        "age": student_info.get("age", ""),
        "grade": student_info.get("grade", ""),
        "class_name": student_info.get("class_name", ""),
        "phone": student_info.get("phone", ""),
        "email": student_info.get("email", ""),
        "address": student_info.get("address", ""),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    students.append(student)
    save_student_data(students)

    return {"success": True, "student": student}


def update_student(student_id, student_info):
    """
    更新学生信息

    Args:
        student_id (str): 学生ID
        student_info (dict): 更新的学生信息

    Returns:
        dict: 更新结果
    """
    for student in students:
        if student["id"] == student_id:
            student.update(student_info)
            student["updated_at"] = datetime.now().isoformat()
            save_student_data(students)
            return {"success": True, "student": student}

    return {"success": False, "error": "学生不存在"}


def delete_student(student_id):
    """
    删除学生

    Args:
        student_id (str): 学生ID

    Returns:
        dict: 删除结果
    """
    global students
    students = [s for s in students if s["id"] != student_id]
    save_student_data(students)
    return {"success": True}


def get_student(student_id):
    """
    获取单个学生信息

    Args:
        student_id (str): 学生ID

    Returns:
        dict: 学生信息或None
    """
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def get_all_students():
    """获取所有学生信息"""
    return students


def search_students(query):
    """
    搜索学生

    Args:
        query (str): 搜索关键词

    Returns:
        list: 匹配的学生列表
    """
    if not query:
        return students

    results = []
    query_lower = query.lower()

    for student in students:
        if (
            query_lower in student.get("name", "").lower()
            or query_lower in student.get("grade", "").lower()
            or query_lower in student.get("class_name", "").lower()
        ):
            results.append(student)

    return results
