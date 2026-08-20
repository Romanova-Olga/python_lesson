import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseClass import TeacherTable, Base, DB_URL

# Подключение к БД
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

# Фикстура для создания/удаления таблиц и сессии
@pytest.fixture
def session():
    # Создаём таблицы, если их нет
    Base.metadata.create_all(engine)
    db_session = Session()
    yield db_session
    # Откатываем изменения после каждого теста
    db_session.rollback()
    db_session.close()

# Фикстура для создания тестового учителя (чтобы не дублировать код)
@pytest.fixture
def test_teacher(session):
    teacher = TeacherTable(name="Иван Петров", subject="Математика")
    session.add(teacher)
    session.commit()
    yield teacher
    # Удаляем после теста
    session.delete(teacher)
    session.commit()

# ============= ТЕСТЫ =============

def test_add_teacher(session):
    """Тест добавления нового учителя"""
    # Создаём нового учителя
    new_teacher = TeacherTable(name="Анна Смирнова", subject="Физика")
    session.add(new_teacher)
    session.commit()
    
    # Проверяем, что он появился в БД
    saved_teacher = session.query(TeacherTable).filter_by(name="Анна Смирнова").first()
    assert saved_teacher is not None
    assert saved_teacher.subject == "Физика"
    
    # Очищаем за собой (удаляем созданные данные)
    session.delete(saved_teacher)
    session.commit()


def test_update_teacher(session, test_teacher):
    """Тест изменения данных учителя"""
    # Меняем предмет у тестового учителя
    test_teacher.subject = "Информатика"
    session.commit()
    
    # Проверяем, что изменения сохранились
    updated_teacher = session.query(TeacherTable).filter_by(id=test_teacher.id).first()
    assert updated_teacher.subject == "Информатика"
    assert updated_teacher.name == "Иван Петров"  # Имя не изменилось


def test_delete_teacher(session):
    """Тест удаления учителя"""
    # Создаём учителя специально для удаления
    teacher_to_delete = TeacherTable(name="Пётр Сидоров", subject="Химия")
    session.add(teacher_to_delete)
    session.commit()
    
    # Сохраняем его ID для проверки
    teacher_id = teacher_to_delete.id
    
    # Удаляем
    session.delete(teacher_to_delete)
    session.commit()
    
    # Проверяем, что его больше нет в БД
    deleted_teacher = session.query(TeacherTable).filter_by(id=teacher_id).first()
    assert deleted_teacher is None
