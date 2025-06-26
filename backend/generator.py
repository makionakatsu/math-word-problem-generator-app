"""
generator.py - 数学文章問題とヒント生成機能（リファクタリング版）

学年・難易度に基づいて文章問題を生成し、7段階のヒントを提供します。
"""

import random
from typing import List, Dict, Any

from .curriculum_map import get_templates_for_grade, get_problem_count_for_grade
from .number_generator import generate_question_from_template
from .hint_generator import generate_hints
from .ruby_utils import add_ruby_for_elementary


class Problem:
    """数学文章問題を表すクラス"""
    
    def __init__(self, problem_id: str, question: str, hints: List[str]):
        """
        問題インスタンスを初期化
        
        Args:
            problem_id: 問題の一意識別子
            question: 問題文
            hints: ヒントのリスト（7つ）
        """
        self.id = problem_id
        self.question = question
        self.hints = hints
    
    def to_dict(self) -> Dict[str, Any]:
        """
        辞書形式で返す（API レスポンス用）
        
        Returns:
            問題データの辞書
        """
        return {
            "id": self.id,
            "question": self.question,
            "hints": self.hints
        }


class ProblemGenerator:
    """問題生成クラス"""
    
    @staticmethod
    def generate_problems(grade: int, difficulty: int) -> List[Dict[str, Any]]:
        """
        指定された学年・難易度に基づいて文章問題を生成
        
        Args:
            grade: 学年 (1-12)
            difficulty: 難易度 (1-5)
        
        Returns:
            問題とヒントのリスト
            
        Raises:
            ValueError: 無効な学年または難易度が指定された場合
        """
        # 入力値検証
        ProblemGenerator._validate_inputs(grade, difficulty)
        
        # カリキュラムデータ取得
        templates = get_templates_for_grade(grade)
        problem_count = get_problem_count_for_grade(grade)
        
        if not templates:
            raise ValueError(f"学年{grade}のテンプレートが見つかりません")
        
        # 問題生成
        problems = []
        for i in range(problem_count):
            problem = ProblemGenerator._generate_single_problem(
                templates, grade, difficulty, i + 1
            )
            problems.append(problem.to_dict())
        
        return problems
    
    @staticmethod
    def _validate_inputs(grade: int, difficulty: int) -> None:
        """
        入力値を検証
        
        Args:
            grade: 学年
            difficulty: 難易度
            
        Raises:
            ValueError: 無効な値の場合
        """
        if not (1 <= grade <= 12):
            raise ValueError("学年は1から12の間で指定してください")
        if not (1 <= difficulty <= 5):
            raise ValueError("難易度は1から5の間で指定してください")
    
    @staticmethod
    def _generate_single_problem(templates: List[str], grade: int, difficulty: int, problem_number: int) -> Problem:
        """
        単一の問題を生成
        
        Args:
            templates: 問題テンプレートのリスト
            grade: 学年
            difficulty: 難易度
            problem_number: 問題番号
            
        Returns:
            生成された問題
        """
        # ランダムにテンプレートを選択
        template = random.choice(templates)
        
        # 問題文生成
        question, numbers_used = generate_question_from_template(template, grade, difficulty)
        
        # 小学生の問題文にルビを追加
        if grade <= 6:
            question = add_ruby_for_elementary(question, grade)
        
        # ヒント生成
        hints = generate_hints(template, grade, difficulty, numbers_used)
        
        # 問題インスタンス作成
        problem_id = f"problem_{grade}_{difficulty}_{problem_number}"
        return Problem(problem_id, question, hints)


# APIとの互換性のための関数
def generate_problems(grade: int, difficulty: int) -> List[Dict[str, Any]]:
    """
    問題生成関数（既存APIとの互換性のため）
    
    Args:
        grade: 学年 (1-12)
        difficulty: 難易度 (1-5)
    
    Returns:
        問題とヒントのリスト
    """
    return ProblemGenerator.generate_problems(grade, difficulty)


# テスト用関数
def test_problem_generation():
    """問題生成機能のテスト"""
    print("=== リファクタリング後の問題生成テスト ===")
    
    # 各学年での問題生成テスト
    test_cases = [
        (1, 2, "小学1年生"),
        (3, 3, "小学3年生"),
        (6, 2, "小学6年生"),
        (7, 3, "中学1年生"),
        (10, 4, "高校1年生")
    ]
    
    for grade, difficulty, description in test_cases:
        try:
            problems = ProblemGenerator.generate_problems(grade, difficulty)
            print(f"\\n{description} (難易度{difficulty}):")
            print(f"  問題数: {len(problems)}")
            print(f"  問題例: {problems[0]['question'][:50]}...")
            print(f"  ヒント数: {len(problems[0]['hints'])}")
            
            # ルビの確認
            if grade <= 6:
                ruby_count = problems[0]['question'].count('<ruby>')
                print(f"  ルビ数: {ruby_count}")
            
        except Exception as e:
            print(f"  エラー: {e}")
    
    print("\\n=== テスト完了 ===")


if __name__ == "__main__":
    test_problem_generation()