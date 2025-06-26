"""
test_generator.py - 数学文章問題生成機能のテスト

generator.py の機能を検証するためのユニットテスト
"""

import pytest
from backend.generator import (
    generate_problems,
    generate_number,
    generate_fraction,
    generate_price,
    get_items_for_grade,
    identify_problem_type,
    generate_light_hints,
    generate_core_hints,
    generate_solution_hints
)
from backend.curriculum_map import get_problem_count_for_grade


class TestGenerateProblems:
    """問題生成機能のテスト"""
    
    def test_generate_problems_valid_input(self):
        """有効な入力での問題生成テスト"""
        # 小学3年生、難易度2の問題を生成
        problems = generate_problems(3, 2)
        
        # 問題数が正しいか確認
        expected_count = get_problem_count_for_grade(3)
        assert len(problems) == expected_count
        
        # 各問題の構造を確認
        for problem in problems:
            assert 'id' in problem
            assert 'question' in problem
            assert 'hints' in problem
            assert isinstance(problem['hints'], list)
            assert len(problem['hints']) == 7  # 7段階ヒント
            assert problem['question'] != ""
            assert all(hint != "" for hint in problem['hints'])
    
    def test_generate_problems_all_grades(self):
        """全学年での問題生成テスト"""
        for grade in range(1, 13):
            problems = generate_problems(grade, 3)
            expected_count = get_problem_count_for_grade(grade)
            assert len(problems) == expected_count
            
            # 各問題が適切な構造を持つか確認
            for problem in problems:
                assert isinstance(problem, dict)
                assert 'id' in problem
                assert 'question' in problem
                assert 'hints' in problem
                assert len(problem['hints']) == 7
    
    def test_generate_problems_all_difficulties(self):
        """全難易度での問題生成テスト"""
        for difficulty in range(1, 6):
            problems = generate_problems(6, difficulty)  # 小学6年生で固定
            assert len(problems) == 5  # 小学生は5問
            
            # 問題が生成されているか確認
            for problem in problems:
                assert problem['question'] != ""
                assert len(problem['hints']) == 7
    
    def test_generate_problems_invalid_grade(self):
        """無効な学年での例外処理テスト"""
        with pytest.raises(ValueError, match="学年は1から12の間で指定してください"):
            generate_problems(0, 3)
        
        with pytest.raises(ValueError, match="学年は1から12の間で指定してください"):
            generate_problems(13, 3)
    
    def test_generate_problems_invalid_difficulty(self):
        """無効な難易度での例外処理テスト"""
        with pytest.raises(ValueError, match="難易度は1から5の間で指定してください"):
            generate_problems(5, 0)
        
        with pytest.raises(ValueError, match="難易度は1から5の間で指定してください"):
            generate_problems(5, 6)


class TestGenerateNumber:
    """数値生成機能のテスト"""
    
    def test_generate_number_range(self):
        """数値範囲のテスト"""
        # 小学1年生の数値範囲
        for _ in range(100):
            num = generate_number(1, 1)
            assert 1 <= num <= 13  # 1-10 × 1.3 = 1-13
        
        # 小学6年生の数値範囲
        for _ in range(100):
            num = generate_number(6, 1)
            assert 1 <= num <= 130000  # 基本範囲 × 難易度調整
    
    def test_generate_number_difficulty_scaling(self):
        """難易度による数値スケーリングのテスト"""
        # 同じ学年で難易度を変えて比較
        grade = 3
        easy_nums = [generate_number(grade, 1) for _ in range(50)]
        hard_nums = [generate_number(grade, 5) for _ in range(50)]
        
        # 難易度5の方が平均的に大きな数値が生成されることを確認
        assert max(hard_nums) >= max(easy_nums)


class TestGenerateFraction:
    """分数生成機能のテスト"""
    
    def test_generate_fraction_format(self):
        """分数フォーマットのテスト"""
        for grade in [3, 5, 8]:
            for _ in range(20):
                fraction = generate_fraction(grade, 3)
                assert '/' in fraction
                parts = fraction.split('/')
                assert len(parts) == 2
                numerator, denominator = int(parts[0]), int(parts[1])
                assert 1 <= numerator < denominator
    
    def test_generate_fraction_grade_scaling(self):
        """学年による分数の複雑さテスト"""
        # 小学3年生の分数は比較的単純
        for _ in range(10):
            fraction = generate_fraction(3, 3)
            denominator = int(fraction.split('/')[1])
            assert denominator <= 4
        
        # 中学生の分数はより複雑
        for _ in range(10):
            fraction = generate_fraction(8, 3)
            denominator = int(fraction.split('/')[1])
            assert denominator <= 10


class TestGeneratePrice:
    """価格生成機能のテスト"""
    
    def test_generate_price_range(self):
        """価格範囲のテスト"""
        # 小学1年生の価格
        for _ in range(20):
            price = generate_price(1, 3)
            assert 10 <= price <= 100
        
        # 小学6年生の価格
        for _ in range(20):
            price = generate_price(6, 3)
            assert 50 <= price <= 500
        
        # 中学生の価格
        for _ in range(20):
            price = generate_price(8, 3)
            assert 100 <= price <= 1000


class TestGetItemsForGrade:
    """学年別アイテム取得のテスト"""
    
    def test_get_items_elementary(self):
        """小学生用アイテムのテスト"""
        items = get_items_for_grade(3)
        assert isinstance(items, list)
        assert len(items) > 0
        assert 'りんご' in items or 'みかん' in items
    
    def test_get_items_middle_school(self):
        """中学生用アイテムのテスト"""
        items = get_items_for_grade(8)
        assert isinstance(items, list)
        assert len(items) > 0
        assert '商品' in items or '部品' in items
    
    def test_get_items_high_school(self):
        """高校生用アイテムのテスト"""
        items = get_items_for_grade(11)
        assert isinstance(items, list)
        assert len(items) > 0
        assert '商品' in items or '製品' in items


class TestProblemTypeIdentification:
    """問題タイプ識別のテスト"""
    
    def test_identify_addition_problem(self):
        """加算問題の識別テスト"""
        template = "りんごが3個あります。みかんを2個もらいました。全部で何個になるでしょうか。"
        assert identify_problem_type(template) == 'addition'
    
    def test_identify_subtraction_problem(self):
        """減算問題の識別テスト"""
        template = "りんごが5個ありました。2個あげました。残りは何個でしょうか。"
        assert identify_problem_type(template) == 'subtraction'
    
    def test_identify_multiplication_problem(self):
        """乗算問題の識別テスト"""
        template = "りんごが1つずつ3箱に入っています。全部で何個あるでしょうか。"
        assert identify_problem_type(template) == 'multiplication'
    
    def test_identify_division_problem(self):
        """除算問題の識別テスト"""
        template = "りんごが12個あります。3人で等しく分けると何個ずつもらえるでしょうか。"
        assert identify_problem_type(template) == 'division'
    
    def test_identify_area_problem(self):
        """面積問題の識別テスト"""
        template = "長方形の縦が5cm、横が3cmのとき、面積は何㎠でしょうか。"
        assert identify_problem_type(template) == 'area'


class TestHintGeneration:
    """ヒント生成機能のテスト"""
    
    def test_generate_light_hints(self):
        """軽いヒント生成のテスト"""
        hints = generate_light_hints('addition', 3)
        assert isinstance(hints, list)
        assert len(hints) == 2
        assert all(isinstance(hint, str) and hint != "" for hint in hints)
    
    def test_generate_core_hints(self):
        """核心的ヒント生成のテスト"""
        hints = generate_core_hints('multiplication', 5)
        assert isinstance(hints, list)
        assert len(hints) == 3
        assert all(isinstance(hint, str) and hint != "" for hint in hints)
    
    def test_generate_solution_hints(self):
        """解答ヒント生成のテスト"""
        # テスト用の数値辞書
        numbers_used = {'num1': '5', 'num2': '3'}
        hints = generate_solution_hints('area', 6, '長方形の面積', numbers_used)
        assert isinstance(hints, list)
        assert len(hints) == 2
        assert all(isinstance(hint, str) and hint != "" for hint in hints)
    
    def test_hint_content_relevance(self):
        """ヒント内容の関連性テスト"""
        # 加算問題のヒント
        light_hints = generate_light_hints('addition', 3)
        assert any('たし算' in hint for hint in light_hints)
        
        # 面積問題のヒント
        core_hints = generate_core_hints('area', 5)
        assert any('面積' in hint for hint in core_hints)


class TestEdgeCases:
    """エッジケースのテスト"""
    
    def test_boundary_grades(self):
        """境界値の学年テスト"""
        # 最小値
        problems = generate_problems(1, 1)
        assert len(problems) == 5  # 小学生は5問
        
        # 最大値
        problems = generate_problems(12, 5)
        assert len(problems) == 1  # 高校生は1問
    
    def test_boundary_difficulties(self):
        """境界値の難易度テスト"""
        # 最小値
        problems = generate_problems(5, 1)
        assert len(problems) == 5
        
        # 最大値
        problems = generate_problems(5, 5)
        assert len(problems) == 5
    
    def test_problem_uniqueness(self):
        """問題の一意性テスト"""
        problems = generate_problems(4, 3)
        questions = [p['question'] for p in problems]
        
        # 同じ問題が生成される可能性は低いはず（完全に同じでなければOK）
        # ただし、ランダム性により同じ問題が生成される可能性もある
        assert len(problems) == len(set(p['id'] for p in problems))  # IDは一意


if __name__ == "__main__":
    # テスト実行
    pytest.main([__file__, "-v"])