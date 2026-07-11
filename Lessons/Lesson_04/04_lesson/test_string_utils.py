import pytest
from string_utils import StringUtils

class TestStringUtils:

 @pytest.fixture
 def utils(self):
    return StringUtils()

 @pytest.mark.positive
 @pytest.mark.parametrize("input_str, expected",[
    ("skypro", "Skypro"),
    ("hello world", "Hello world"),
 ])
 def test_capitalize_positive(self,utils,input_str,expected):
    assert utils.capitalize(input_str) == expected


 @pytest.mark.negative("input_str, expected",[("123sky")])
 def test_capitalize_string_with_numbers(self,utils):
   """Проверка: строка с цифрами в начале"""
   assert utils.capitalize("123sky") == "123sky"



 @pytest.mark.positive
 @pytest.mark.parametrize("input_str, expected",[
    (" skypro","skypro "),   #пробелы в начале и в конце
    (" hello ","hello "),
 ])
 def test_trim_positiv(self,utils,input_str,expected):
    """Проверка: удаляются только пробелы в начале"""
    assert utils.trim(input_str) == expected


 @pytest.mark.negative
 @pytest.mark.parametrize("input_str, expected",[
   (""),     #Проверка: пустая строка 
   ("None")  #Проверка: пустая строка (если так задумано)
 ])
 def test_trim_empty_or_none(self,utils,input_str, expected):
   assert utils.trim(input_str) == expected



 @pytest.mark.positive
 @pytest.mark.parametrize("string, symbol, expected",[
    ("SkyPro", "S", True),      # символ в начале
    ("SkyPro", "o", True),      # символ в конце
    ("SkyPro", "y", True),      # символ в середине
    ("Hello\nWorld", "W", True), # символ в строке с переносом
    ("SkyPro", "k", True),      # символ в слове
    ("123abc", "3", True),      # цифра
    ("Hello World", " ", True), # пробел
    ("Привет", "и", True),      # кириллица
    ("SkyPro", "P", True),      # заглавная буква
    ("abcABC", "b", True),      # строчная буква
    ("abcABC", "B", True),      # заглавная буква
    ("!@#$%", "@", True),       # специальный символ
 ])
 def test_contains_positive(self, utils, string, symbol, expected):
    """Проверка: искомый символ присутствует"""
    assert utils.contains(string, symbol) is expected


 @pytest.mark.negative
 @pytest.mark.parametrize("string, symbol, expected",[
    ("", "a", False),   #пустая строка
    ("Skypro", "", True),   #пустой символ (особенность)
    ])
 def test_contains_negative(self,utils,string,symbol,expected):
    """Проверка: пустая строка -> False"""
    assert utils.contains(string,symbol) is expected



 @pytest.mark.positive
 @pytest.mark.parametrize("input_str,symbol,expected",[
    ("SkyPro", "k", "SyPro"),      # удаление одного символа
    ("SkyPro", "Pro", "Sky"),      # удаление подстроки
    ("abacaba", "a", "bcb"),       # удаление всех вхождений
 ])
 def test_delete_symbol_positive(self,utils,input_str,symbol,expected):
    """Проверка: удаление символов"""
    assert utils.delete_symbol(input_str,symbol) == expected

 @pytest.mark.negative
 @pytest.mark.parametrize("input_str,symbol,expected",[
    ("SkyPro", "X", "SkyPro"),   #символ не найден
    ("SkyPro", "", "SkyPro"),   #пустой символ
    ])  
 def test_delete_symbol_negativ(self,utils,input_str,symbol,expected):
    """Проверка: символ не найден -> возвращается исходная строка"""
    assert utils.delete_symbol(input_str,symbol) == expected