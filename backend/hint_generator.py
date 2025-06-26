"""
hint_generator.py - ヒント生成機能

7段階のヒント生成機能を提供します。
段階1-2: 軽いヒント、段階3-5: 核心的ヒント、段階6-7: 解答ヒント
"""

from typing import List, Dict
from .ruby_utils import add_ruby_for_elementary


def generate_hints(template: str, grade: int, difficulty: int, numbers_used: Dict[str, str]) -> List[str]:
    """
    7段階のヒントを生成
    
    Args:
        template: 問題テンプレート
        grade: 学年 (1-12)
        difficulty: 難易度 (1-5)
        numbers_used: 使用された数値の辞書
    
    Returns:
        7つのヒントのリスト
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
    """
    問題のタイプを識別
    
    Args:
        template: 問題テンプレート
    
    Returns:
        問題タイプ ('addition', 'subtraction', 'multiplication', 'division', 
                  'area', 'volume', 'equation', 'function', 'general')
    """
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


def generate_light_hints(problem_type: str, grade: int) -> List[str]:
    """
    軽いヒント（段階1-2）を生成
    
    Args:
        problem_type: 問題タイプ
        grade: 学年
    
    Returns:
        2つの軽いヒント
    """
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
    """
    核心的ヒント（段階3-5）を生成
    
    Args:
        problem_type: 問題タイプ
        grade: 学年
    
    Returns:
        3つの核心的ヒント
    """
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


def generate_solution_hints(problem_type: str, grade: int, template: str, numbers_used: Dict[str, str]) -> List[str]:
    """
    解答ヒント（段階6-7）を生成
    
    Args:
        problem_type: 問題タイプ
        grade: 学年
        template: 問題テンプレート
        numbers_used: 使用された数値の辞書
    
    Returns:
        2つの解答ヒント（式と答え）
    """
    # 実際に使用された数値から具体的な式と答えを生成
    nums = [int(v) for k, v in numbers_used.items() if k.startswith('num') and str(v).isdigit()]
    
    if problem_type == 'addition' and len(nums) >= 2:
        calculation = f"{nums[0]} + {nums[1]}"
        result = nums[0] + nums[1]
        answer = format_answer_with_unit(result, template)
        return [f'式: {calculation}', f'答え: {answer}']
    
    elif problem_type == 'subtraction' and len(nums) >= 2:
        calculation = f"{nums[0]} - {nums[1]}"
        result = nums[0] - nums[1]
        answer = format_answer_with_unit(result, template)
        return [f'式: {calculation}', f'答え: {answer}']
    
    elif problem_type == 'multiplication' and len(nums) >= 2:
        calculation = f"{nums[0]} × {nums[1]}"
        result = nums[0] * nums[1]
        answer = f"{result}個"
        return [f'式: {calculation}', f'答え: {answer}']
    
    elif problem_type == 'division' and len(nums) >= 2 and nums[1] != 0:
        result = nums[0] // nums[1]
        calculation = f"{nums[0]} ÷ {nums[1]}"
        answer = f"{result}個ずつ"
        return [f'式: {calculation}', f'答え: {answer}']
    
    elif problem_type == 'area' and len(nums) >= 2:
        area = nums[0] * nums[1]
        calculation = f"{nums[0]} × {nums[1]}"
        answer = f"{area}㎠"
        return [f'式: {calculation}', f'答え: {answer}']
    
    elif problem_type == 'volume' and len(nums) >= 3:
        volume = nums[0] * nums[1] * nums[2]
        calculation = f"{nums[0]} × {nums[1]} × {nums[2]}"
        answer = f"{volume}㎤"
        return [f'式: {calculation}', f'答え: {answer}']
    
    else:
        # デフォルトのヒント（数値が足りない場合など）
        if nums and len(nums) >= 2:
            # 基本的な計算パターンを推測
            if '合わせて' in template or '全部で' in template:
                calculation = f"{nums[0]} + {nums[1]}"
                result = nums[0] + nums[1]
            elif '残り' in template:
                calculation = f"{nums[0]} - {nums[1]}"
                result = nums[0] - nums[1]
            else:
                calculation = f"{nums[0]} + {nums[1]}"
                result = nums[0] + nums[1]
            
            answer = format_answer_with_unit(result, template)
            return [f'式: {calculation}', f'答え: {answer}']
        else:
            return [
                '問題文の数値を使って計算式を立てましょう。',
                '計算して答えを求めましょう。'
            ]


def format_answer_with_unit(result: int, template: str) -> str:
    """
    結果に適切な単位を付けてフォーマット
    
    Args:
        result: 計算結果
        template: 問題テンプレート
    
    Returns:
        単位付きの答え
    """
    # 単位を推測
    if 'mL' in template:
        return f"{result}mL"
    elif 'g' in template:
        return f"{result}g"
    elif 'cm' in template:
        return f"{result}cm"
    elif '円' in template:
        return f"{result}円"
    else:
        return f"{result}個"


# テスト用関数
def test_hint_generation():
    """ヒント生成機能のテスト"""
    print("=== ヒント生成テスト ===")
    
    # 小学1年生のたし算問題
    template = "りんごが{num1}個あります。みかんを{num2}個もらいました。全部で何個になるでしょうか。"
    numbers_used = {'num1': '5', 'num2': '3'}
    hints = generate_hints(template, 1, 2, numbers_used)
    
    print("小学1年生のたし算問題のヒント:")
    for i, hint in enumerate(hints, 1):
        print(f"  {i}. {hint}")
    
    print(f"\\nルビタグ数: {sum(hint.count('<ruby>') for hint in hints)}")


if __name__ == "__main__":
    test_hint_generation()