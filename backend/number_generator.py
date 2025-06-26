"""
number_generator.py - 数値生成ロジック

問題文で使用する数値やプレースホルダーの値を生成する機能を提供します。
"""

import random
import re
from typing import List, Dict, Tuple


def generate_question_from_template(template: str, grade: int, difficulty: int) -> Tuple[str, Dict[str, str]]:
    """
    テンプレートから具体的な問題文を生成
    
    Args:
        template: 問題テンプレート
        grade: 学年 (1-12)
        difficulty: 難易度 (1-5)
    
    Returns:
        (具体的な問題文, 使用した数値の辞書)
    """
    # テンプレート内のプレースホルダーを抽出
    placeholders = re.findall(r'\{(\w+)\}', template)
    
    # プレースホルダーを具体的な値に置換
    replacements = {}
    
    # ひき算の問題の場合、適切な数値関係を保つ
    if is_subtraction_problem(template):
        replacements = generate_subtraction_numbers(placeholders, grade, difficulty)
    else:
        # 通常の場合
        for placeholder in placeholders:
            replacements[placeholder] = generate_value_for_placeholder(placeholder, grade, difficulty)
    
    # テンプレートに値を代入
    question = template
    for key, value in replacements.items():
        question = question.replace(f'{{{key}}}', str(value))
    
    return question, replacements


def is_subtraction_problem(template: str) -> bool:
    """
    テンプレートがひき算問題かどうかを判定
    
    Args:
        template: 問題テンプレート
    
    Returns:
        ひき算問題の場合True
    """
    subtraction_keywords = ['短く', '使い', 'あげ', '残り', '飲みました']
    return any(keyword in template for keyword in subtraction_keywords)


def generate_subtraction_numbers(placeholders: List[str], grade: int, difficulty: int) -> Dict[str, str]:
    """
    ひき算問題用の適切な数値関係を保った数値を生成
    
    Args:
        placeholders: プレースホルダーのリスト
        grade: 学年
        difficulty: 難易度
    
    Returns:
        プレースホルダーと値の辞書
    """
    replacements = {}
    
    # 最初の数を大きく、2番目の数を小さくする
    num1 = generate_number(grade, difficulty)
    num2 = random.randint(1, max(1, num1 - 1))  # num1より小さくする
    
    num_count = 0
    for placeholder in placeholders:
        if placeholder.startswith('num'):
            if num_count == 0:
                replacements[placeholder] = str(num1)
            elif num_count == 1:
                replacements[placeholder] = str(num2)
            else:
                replacements[placeholder] = generate_value_for_placeholder(placeholder, grade, difficulty)
            num_count += 1
        else:
            replacements[placeholder] = generate_value_for_placeholder(placeholder, grade, difficulty)
    
    return replacements


def generate_value_for_placeholder(placeholder: str, grade: int, difficulty: int) -> str:
    """
    プレースホルダーに対応する値を生成
    
    Args:
        placeholder: プレースホルダー名
        grade: 学年
        difficulty: 難易度
    
    Returns:
        プレースホルダーに対応する値
    """
    # 基本的な数値範囲を学年と難易度で調整
    if 'num' in placeholder:
        return str(generate_number(grade, difficulty))
    elif 'item' in placeholder:
        return random.choice(get_items_for_grade(grade))
    elif 'person' in placeholder:
        return random.choice(['太郎', 'さくら', 'けんじ', 'みゆき', 'りょう', 'あい'])
    elif 'fraction' in placeholder:
        return generate_fraction(grade, difficulty)
    elif 'price' in placeholder:
        return str(generate_price(grade, difficulty))
    elif 'time' in placeholder:
        return str(random.randint(1, 12))
    elif 'min' in placeholder:
        return str(random.randint(0, 59))
    elif 'angle' in placeholder:
        return str(random.randint(10, 80))
    elif placeholder in ['a', 'b', 'c', 'd']:
        return str(random.randint(1, 5))
    elif 'slope' in placeholder:
        return str(random.randint(1, 5))
    elif 'intercept' in placeholder:
        return str(random.randint(1, 10))
    else:
        return str(generate_number(grade, difficulty))


def generate_number(grade: int, difficulty: int) -> int:
    """
    学年と難易度に応じた数値を生成
    
    Args:
        grade: 学年 (1-12)
        difficulty: 難易度 (1-5)
    
    Returns:
        生成された数値
    """
    base_ranges = {
        1: (1, 10),      # 小1: 1桁
        2: (1, 20),      # 小2: 20まで
        3: (1, 100),     # 小3: 100まで
        4: (1, 1000),    # 小4: 1000まで
        5: (1, 10000),   # 小5: 10000まで
        6: (1, 100000),  # 小6: 100000まで
    }
    
    if grade <= 6:
        min_val, max_val = base_ranges.get(grade, (1, 10))
    elif grade <= 9:
        min_val, max_val = (1, 100)
    else:
        min_val, max_val = (1, 50)
    
    # 難易度による調整
    difficulty_multiplier = difficulty * 0.3 + 0.7
    max_val = int(max_val * difficulty_multiplier)
    
    return random.randint(min_val, max_val)


def generate_fraction(grade: int, difficulty: int) -> str:
    """
    分数を生成
    
    Args:
        grade: 学年
        difficulty: 難易度
    
    Returns:
        分数の文字列表現 (例: "1/2")
    """
    if grade <= 3:
        denominators = [2, 3, 4]
    elif grade <= 6:
        denominators = [2, 3, 4, 5, 6, 8]
    else:
        denominators = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    denominator = random.choice(denominators)
    numerator = random.randint(1, denominator - 1)
    
    return f"{numerator}/{denominator}"


def generate_price(grade: int, difficulty: int) -> int:
    """
    価格を生成
    
    Args:
        grade: 学年
        difficulty: 難易度
    
    Returns:
        価格（円）
    """
    if grade <= 3:
        return random.randint(10, 100)
    elif grade <= 6:
        return random.randint(50, 500)
    else:
        return random.randint(100, 1000)


def get_items_for_grade(grade: int) -> List[str]:
    """
    学年に応じたアイテムリストを取得
    
    Args:
        grade: 学年
    
    Returns:
        アイテム名のリスト
    """
    if grade <= 3:
        return ['りんご', 'みかん', 'あめ', 'えんぴつ', 'ノート', 'ボール']
    elif grade <= 6:
        return ['本', '文房具', 'お菓子', 'シール', 'カード', 'おもちゃ']
    elif grade <= 9:
        return ['商品', '部品', '材料', '道具', '機器', '製品']
    else:
        return ['商品', '製品', '部品', '材料', '機器', '装置']


# 数値生成のテスト用関数
def test_number_generation():
    """数値生成機能のテスト"""
    print("=== 数値生成テスト ===")
    
    # 各学年の数値範囲テスト
    for grade in [1, 3, 6, 9, 12]:
        numbers = [generate_number(grade, 3) for _ in range(5)]
        print(f"学年{grade}: {numbers}")
    
    # 分数生成テスト
    fractions = [generate_fraction(3, 2) for _ in range(5)]
    print(f"分数: {fractions}")
    
    # ひき算問題テスト
    template = "テープの長さは{num1}cmです。{num2}cm短くしました。残りの長さは何cmでしょうか。"
    question, replacements = generate_question_from_template(template, 2, 2)
    print(f"ひき算問題: {question}")
    print(f"数値: {replacements}")


if __name__ == "__main__":
    test_number_generation()