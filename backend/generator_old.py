"""
generator.py - 数学文章問題とヒント生成機能

学年・難易度に基づいて文章問題を生成し、7段階のヒントを提供します。
"""

import random
import re
from typing import List, Dict, Any
from .curriculum_map import get_templates_for_grade, get_problem_count_for_grade

class Problem:
    """数学文章問題を表すクラス"""
    def __init__(self, problem_id: str, question: str, hints: List[str]):
        self.id = problem_id
        self.question = question
        self.hints = hints
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式で返す（API レスポンス用）"""
        return {
            "id": self.id,
            "question": self.question,
            "hints": self.hints
        }

def generate_problems(grade: int, difficulty: int) -> List[Dict[str, Any]]:
    """
    指定された学年・難易度に基づいて文章問題を生成
    
    Args:
        grade: 学年 (1-12)
        difficulty: 難易度 (1-5)
    
    Returns:
        問題とヒントのリスト
    """
    if not (1 <= grade <= 12):
        raise ValueError("学年は1から12の間で指定してください")
    if not (1 <= difficulty <= 5):
        raise ValueError("難易度は1から5の間で指定してください")
    
    templates = get_templates_for_grade(grade)
    problem_count = get_problem_count_for_grade(grade)
    
    if not templates:
        raise ValueError(f"学年{grade}のテンプレートが見つかりません")
    
    problems = []
    for i in range(problem_count):
        # ランダムにテンプレートを選択
        template = random.choice(templates)
        
        # 難易度に応じた問題を生成
        question, numbers_used = generate_question_from_template(template, grade, difficulty)
        
        # 小学生の問題文にルビを追加
        if grade <= 6:
            question = add_ruby_for_elementary(question, grade)
        
        hints = generate_hints(template, grade, difficulty, numbers_used)
        
        problem = Problem(
            problem_id=f"problem_{grade}_{difficulty}_{i+1}",
            question=question,
            hints=hints
        )
        
        problems.append(problem.to_dict())
    
    return problems

def generate_question_from_template(template: str, grade: int, difficulty: int) -> tuple[str, dict]:
    """
    テンプレートから具体的な問題文を生成
    
    Args:
        template: 問題テンプレート
        grade: 学年
        difficulty: 難易度
    
    Returns:
        (具体的な問題文, 使用した数値の辞書)
    """
    # テンプレート内のプレースホルダーを抽出
    placeholders = re.findall(r'\{(\w+)\}', template)
    
    # プレースホルダーを具体的な値に置換
    replacements = {}
    
    # ひき算の問題の場合、適切な数値関係を保つ
    if '短く' in template or '使い' in template or 'あげ' in template or '残り' in template:
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
    else:
        # 通常の場合
        for placeholder in placeholders:
            replacements[placeholder] = generate_value_for_placeholder(placeholder, grade, difficulty)
    
    # テンプレートに値を代入
    question = template
    for key, value in replacements.items():
        question = question.replace(f'{{{key}}}', str(value))
    
    return question, replacements

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
    """学年と難易度に応じた数値を生成"""
    base_ranges = {
        1: (1, 10),    # 小1: 1桁
        2: (1, 20),    # 小2: 20まで
        3: (1, 100),   # 小3: 100まで
        4: (1, 1000),  # 小4: 1000まで
        5: (1, 10000), # 小5: 10000まで
        6: (1, 100000), # 小6: 100000まで
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
    """分数を生成"""
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
    """価格を生成"""
    if grade <= 3:
        return random.randint(10, 100)
    elif grade <= 6:
        return random.randint(50, 500)
    else:
        return random.randint(100, 1000)

def get_items_for_grade(grade: int) -> List[str]:
    """学年に応じたアイテムリストを取得"""
    if grade <= 3:
        return ['りんご', 'みかん', 'あめ', 'えんぴつ', 'ノート', 'ボール']
    elif grade <= 6:
        return ['本', '文房具', 'お菓子', 'シール', 'カード', 'おもちゃ']
    elif grade <= 9:
        return ['商品', '部品', '材料', '道具', '機器', '製品']
    else:
        return ['商品', '製品', '部品', '材料', '機器', '装置']

def generate_hints(template: str, grade: int, difficulty: int, numbers_used: dict) -> List[str]:
    """
    7段階のヒントを生成
    
    段階:
    1-2: 軽いヒント（キーワード、注目点）
    3-5: 核心的ヒント（解法の方向性、計算方法）
    6-7: 解答に近いヒント（具体的な計算、完全解答）
    """
    hints = []
    
    # 問題のタイプを判定
    problem_type = identify_problem_type(template)
    
    # 段階1-2: 軽いヒント
    hints.extend(generate_light_hints(problem_type, grade))
    
    # 段階3-5: 核心的ヒント
    hints.extend(generate_core_hints(problem_type, grade))
    
    # 段階6-7: 解答ヒント（具体的な式と答え）
    hints.extend(generate_solution_hints(problem_type, grade, template, numbers_used))
    
    return hints

def identify_problem_type(template: str) -> str:
    """問題のタイプを識別"""
    # より具体的なパターンを優先して判定
    if any(word in template for word in ['わり算', '÷', '等しく分け']):
        return 'division'
    elif any(word in template for word in ['かけ算', '×', 'ずつ', '箱に入って']):
        return 'multiplication'
    elif any(word in template for word in ['ひき算', 'あげ', '使い', '残り']):
        return 'subtraction'
    elif any(word in template for word in ['合わせて', '全部で', 'たし算', 'もらい', '買い']):
        return 'addition'
    elif any(word in template for word in ['面積', '㎠', '長方形', '三角形']):
        return 'area'
    elif any(word in template for word in ['体積', '㎤', '直方体', '円柱']):
        return 'volume'
    elif any(word in template for word in ['方程式', '=', 'x']):
        return 'equation'
    elif any(word in template for word in ['関数', 'y', 'グラフ']):
        return 'function'
    else:
        return 'general'

def add_ruby_for_elementary(text: str, grade: int) -> str:
    """小学生用にルビを追加"""
    if grade > 6:
        return text
    
    # 小学生向けのルビ辞書（問題文とヒント共通）
    ruby_dict = {
        # ヒント用
        '問題': 'もんだい',
        '計算': 'けいさん',
        '方法': 'ほうほう',
        '確認': 'かくにん',
        '注目': 'ちゅうもく',
        '全部': 'ぜんぶ',
        '残り': 'のこり',
        '最初': 'さいしょ',
        '追加': 'ついか',
        '筆算': 'ひっさん',
        '具体的': 'ぐたいてき',
        '単位': 'たんい',
        '公式': 'こうしき',
        '数値': 'すうち',
        '結果': 'けっか',
        
        # 問題文用
        '長さ': 'ながさ',
        '重さ': 'おもさ',
        '時間': 'じかん',
        '時刻': 'じこく',
        '分数': 'ぶんすう',
        '面積': 'めんせき',
        '体積': 'たいせき',
        '温度': 'おんど',
        '半径': 'はんけい',
        '直径': 'ちょっけい',
        '高さ': 'たかさ',
        '底辺': 'ていへん',
        '頂角': 'ちょうかく',
        '底角': 'ていかく',
        '三角形': 'さんかくけい',
        '四角形': 'しかくけい',
        '長方形': 'ちょうほうけい',
        '正方形': 'せいほうけい',
        '直方体': 'ちょくほうたい',
        '円柱': 'えんちゅう',
        '合計': 'ごうけい',
        '平均': 'へいきん',
        '速度': 'そくど',
        '距離': 'きょり',
        '出発': 'しゅっぱつ',
        '到着': 'とうちゃく',
        '料金': 'りょうきん',
        '代金': 'だいきん',
        '値段': 'ねだん',
        '買い物': 'かいもの',
        '個数': 'こすう',
        '人数': 'にんずう',
        '枚数': 'まいすう',
        '本数': 'ほんすう',
        
        # 基本動詞・形容詞
        '持って': 'もって',
        '買いました': 'かいました',
        '短く': 'みじかく',
        '食べました': 'たべました',
        '分けると': 'わけると',
        '等しく': 'ひとしく',
        '大きい': 'おおきい',
        '小さい': 'ちいさい',
        '何個': 'なんこ',
        '何分': 'なんぷん',
        '何時': 'なんじ',
        '何cm': 'なんセンチメートル',
        '何g': 'なんグラム',
        '何mL': 'なんミリリットル',
        '何円': 'なんえん',
        
        # その他
        'リボン': 'リボン',
        'テープ': 'テープ',
        'ケーキ': 'ケーキ',
        'コップ': 'コップ',
        '水': 'みず',
        '底面': 'ていめん'
    }
    
    for word, reading in ruby_dict.items():
        if word in text:
            text = text.replace(word, f'<ruby>{word}<rt>{reading}</rt></ruby>')
    
    return text

def generate_light_hints(problem_type: str, grade: int) -> List[str]:
    """軽いヒント（段階1-2）を生成"""
    hint_patterns = {
        'addition': [
            'この問題は「たし算」の問題です。',
            '「全部で」という言葉に注目しましょう。'
        ],
        'subtraction': [
            'この問題は「ひき算」の問題です。',
            '「残り」という言葉に注目しましょう。'
        ],
        'multiplication': [
            'この問題は「かけ算」の問題です。',
            '「ずつ」という言葉に注目しましょう。'
        ],
        'division': [
            'この問題は「わり算」の問題です。',
            '「等しく分ける」という言葉に注目しましょう。'
        ],
        'area': [
            'この問題は「面積」を求める問題です。',
            '図形の縦と横の長さを確認しましょう。'
        ],
        'volume': [
            'この問題は「体積」を求める問題です。',
            '縦、横、高さの3つの長さを確認しましょう。'
        ],
        'equation': [
            'この問題は「方程式」を解く問題です。',
            '未知数をxとして式を立てましょう。'
        ],
        'function': [
            'この問題は「関数」の問題です。',
            'xとyの関係を確認しましょう。'
        ],
        'general': [
            'まず、問題文をよく読みましょう。',
            '求めるものは何かを確認しましょう。'
        ]
    }
    
    hints = hint_patterns.get(problem_type, hint_patterns['general'])
    return [add_ruby_for_elementary(hint, grade) for hint in hints]

def generate_core_hints(problem_type: str, grade: int) -> List[str]:
    """核心的ヒント（段階3-5）を生成"""
    hint_patterns = {
        'addition': [
            '2つの数をたし算します。',
            '計算式は「最初の数 + 追加した数」です。',
            '筆算で計算してみましょう。'
        ],
        'subtraction': [
            '大きい数から小さい数をひき算します。',
            '計算式は「最初の数 - 使った数」です。',
            '筆算で計算してみましょう。'
        ],
        'multiplication': [
            '同じ数を何回もたし算するのがかけ算です。',
            '計算式は「1つ分の数 × いくつ分」です。',
            '九九を使って計算しましょう。'
        ],
        'division': [
            '全体を等しく分けるのがわり算です。',
            '計算式は「全体の数 ÷ 分ける数」です。',
            'かけ算の逆を考えてみましょう。'
        ],
        'area': [
            '長方形の面積は「縦 × 横」で求めます。',
            '三角形の面積は「底辺 × 高さ ÷ 2」で求めます。',
            '単位を㎠で答えましょう。'
        ],
        'volume': [
            '直方体の体積は「縦 × 横 × 高さ」で求めます。',
            '円柱の体積は「底面積 × 高さ」で求めます。',
            '単位を㎤で答えましょう。'
        ],
        'equation': [
            '等式の性質を使って解きます。',
            '両辺に同じ数をたしたりひいたりします。',
            'xの係数を1にするように計算します。'
        ],
        'function': [
            '関数の式にxの値を代入します。',
            'グラフを描いて確認しましょう。',
            'yの値を求めてみましょう。'
        ],
        'general': [
            '問題文から必要な数値を抜き出します。',
            'どんな計算をすればよいか考えます。',
            '式を立てて計算しましょう。'
        ]
    }
    
    hints = hint_patterns.get(problem_type, hint_patterns['general'])
    return [add_ruby_for_elementary(hint, grade) for hint in hints]

def generate_solution_hints(problem_type: str, grade: int, template: str, numbers_used: dict) -> List[str]:
    """解答ヒント（段階6-7）を生成"""
    # 実際に使用された数値から具体的な式と答えを生成
    nums = [int(v) for k, v in numbers_used.items() if k.startswith('num') and str(v).isdigit()]
    
    if problem_type == 'addition' and len(nums) >= 2:
        calculation = f"{nums[0]} + {nums[1]}"
        result = nums[0] + nums[1]
        # 単位を推測
        if 'mL' in template:
            answer = f"{result}mL"
        elif 'g' in template:
            answer = f"{result}g"
        elif 'cm' in template:
            answer = f"{result}cm"
        elif '円' in template:
            answer = f"{result}円"
        else:
            answer = f"{result}個"
        return [
            f'式: {calculation}',
            f'答え: {answer}'
        ]
    elif problem_type == 'subtraction' and len(nums) >= 2:
        calculation = f"{nums[0]} - {nums[1]}"
        result = nums[0] - nums[1]
        # 単位を推測
        if 'mL' in template:
            answer = f"{result}mL"
        elif 'g' in template:
            answer = f"{result}g"
        elif 'cm' in template:
            answer = f"{result}cm"
        elif '円' in template:
            answer = f"{result}円"
        else:
            answer = f"{result}個"
        return [
            f'式: {calculation}',
            f'答え: {answer}'
        ]
    elif problem_type == 'multiplication' and len(nums) >= 2:
        calculation = f"{nums[0]} × {nums[1]}"
        result = nums[0] * nums[1]
        answer = f"{result}個"
        return [
            f'式: {calculation}',
            f'答え: {answer}'
        ]
    elif problem_type == 'division' and len(nums) >= 2 and nums[1] != 0:
        result = nums[0] // nums[1]
        calculation = f"{nums[0]} ÷ {nums[1]}"
        answer = f"{result}個ずつ"
        return [
            f'式: {calculation}',
            f'答え: {answer}'
        ]
    elif problem_type == 'area' and len(nums) >= 2:
        area = nums[0] * nums[1]
        calculation = f"{nums[0]} × {nums[1]}"
        answer = f"{area}㎠"
        return [
            f'式: {calculation}',
            f'答え: {answer}'
        ]
    elif problem_type == 'volume' and len(nums) >= 3:
        volume = nums[0] * nums[1] * nums[2]
        calculation = f"{nums[0]} × {nums[1]} × {nums[2]}"
        answer = f"{volume}㎤"
        return [
            f'式: {calculation}',
            f'答え: {answer}'
        ]
    else:
        # デフォルトのヒント（数値が足りない場合など）
        if nums:
            # 基本的な計算パターンを推測
            if len(nums) >= 2:
                if '合わせて' in template or '全部で' in template:
                    calculation = f"{nums[0]} + {nums[1]}"
                    answer = f"{nums[0] + nums[1]}"
                elif '残り' in template:
                    calculation = f"{nums[0]} - {nums[1]}"
                    answer = f"{nums[0] - nums[1]}"
                else:
                    calculation = f"{nums[0]} + {nums[1]}"
                    answer = f"{nums[0] + nums[1]}"
                
                # 単位を推測
                if 'g' in template:
                    answer += 'g'
                elif 'cm' in template:
                    answer += 'cm'
                elif 'mL' in template:
                    answer += 'mL'
                elif '個' in template:
                    answer += '個'
                elif '円' in template:
                    answer += '円'
                
                return [
                    f'式: {calculation}',
                    f'答え: {answer}'
                ]
            else:
                return [
                    f'数値 {", ".join(map(str, nums))} を使って計算式を立てましょう。',
                    '計算して答えを求めましょう。'
                ]
        else:
            return [
                '問題文の数値を使って計算式を立てましょう。',
                '計算して答えを求めましょう。'
            ]