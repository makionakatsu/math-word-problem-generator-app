/**
 * 数学文章問題ジェネレーター - メインJavaScript
 */

// API設定
const API_BASE_URL = 'http://127.0.0.1:5001';

// DOM要素の取得
const gradeSelect = document.getElementById('grade');
const difficultySelect = document.getElementById('difficulty');
const generateBtn = document.getElementById('generateBtn');
const printBtn = document.getElementById('printBtn');
const retryBtn = document.getElementById('retryBtn');

const problemsSection = document.getElementById('problemsSection');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const problemsContainer = document.getElementById('problemsContainer');
const errorText = document.getElementById('errorText');

// 状態管理
let currentProblems = [];

// イベントリスナーの設定
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateGenerateButtonState();
    showInitialState();
});

function initializeEventListeners() {
    // 生成ボタン
    generateBtn.addEventListener('click', handleGenerate);
    
    // 印刷ボタン
    printBtn.addEventListener('click', handlePrint);
    
    // 再試行ボタン
    retryBtn.addEventListener('click', handleGenerate);
    
    // 選択変更時の処理
    gradeSelect.addEventListener('change', updateGenerateButtonState);
    difficultySelect.addEventListener('change', updateGenerateButtonState);
}

function updateGenerateButtonState() {
    const gradeSelected = gradeSelect.value !== '';
    const difficultySelected = difficultySelect.value !== '';
    
    generateBtn.disabled = !(gradeSelected && difficultySelected);
}

async function handleGenerate() {
    const grade = parseInt(gradeSelect.value);
    const difficulty = parseInt(difficultySelect.value);
    
    if (!grade || !difficulty) {
        showError('学年と難易度を選択してください。');
        return;
    }
    
    // 問題生成を試行したことを記録
    hasGeneratedProblems = true;
    
    try {
        showLoading();
        const problems = await generateProblems(grade, difficulty);
        currentProblems = problems;
        displayProblems(problems);
        printBtn.disabled = false;
    } catch (error) {
        showError(error.message);
        printBtn.disabled = true;
    }
}

async function generateProblems(grade, difficulty) {
    // タイムアウト処理を追加
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10秒でタイムアウト
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                grade: grade,
                difficulty: difficulty
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('APIサーバーに接続できません。サーバーが起動しているか確認してください。');
            }
            
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `サーバーエラーが発生しました (${response.status})`);
        }
        
        const data = await response.json();
        return data.problems;
        
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new Error('サーバーへの接続がタイムアウトしました。サーバーが起動しているか確認してください。');
        }
        
        if (error.message.includes('Failed to fetch')) {
            throw new Error('サーバーに接続できません。サーバーが起動しているか確認してください。');
        }
        
        throw error;
    }
}

function displayProblems(problems) {
    hideAllSections();
    problemsSection.style.display = 'block';
    
    // 印刷用に学年・難易度情報をbodyに追加
    const grade = gradeSelect.value;
    const difficulty = difficultySelect.value;
    document.body.setAttribute('data-grade', grade);
    document.body.setAttribute('data-difficulty', difficulty);
    
    problemsContainer.innerHTML = '';
    
    problems.forEach((problem, index) => {
        const problemCard = createProblemCard(problem, index + 1);
        problemsContainer.appendChild(problemCard);
    });
}

function createProblemCard(problem, number) {
    const card = document.createElement('div');
    card.className = 'problem-card';
    
    card.innerHTML = `
        <div class="problem-header">
            <div class="problem-number">問題 ${number}</div>
            <button class="show-hints-btn" data-problem-id="${problem.id}">
                ヒントを表示
            </button>
        </div>
        <div class="problem-question">${problem.question}</div>
        <div class="hints-container" id="hints-${problem.id}">
            <h4>7段階ヒント</h4>
            <div class="hints-list">
                ${createHintsHTML(problem.hints, problem.id)}
            </div>
        </div>
    `;
    
    // ヒント表示ボタンのイベントリスナー
    const showHintsBtn = card.querySelector('.show-hints-btn');
    showHintsBtn.addEventListener('click', () => toggleHints(problem.id));
    
    // 各ヒントアイテムのイベントリスナー
    const hintItems = card.querySelectorAll('.hint-item');
    hintItems.forEach(item => {
        item.addEventListener('click', () => revealHint(item));
    });
    
    return card;
}

function createHintsHTML(hints, problemId) {
    const hintLabels = [
        'ヒント1: キーワード',
        'ヒント2: 注目点',
        'ヒント3: 解法の方向性',
        'ヒント4: 計算方法',
        'ヒント5: 詳細な手順',
        'ヒント6: 計算式',
        'ヒント7: 答え'
    ];
    
    return hints.map((hint, index) => `
        <div class="hint-item" data-hint-index="${index}">
            <div class="hint-stage">${hintLabels[index] || `ヒント${index + 1}`}</div>
            <div class="hint-content">${hint}</div>
        </div>
    `).join('');
}

function toggleHints(problemId) {
    console.log('toggleHints called with problemId:', problemId);
    const hintsContainer = document.getElementById(`hints-${problemId}`);
    const showHintsBtn = document.querySelector(`[data-problem-id="${problemId}"]`);
    
    console.log('hintsContainer found:', hintsContainer);
    console.log('showHintsBtn found:', showHintsBtn);
    
    if (hintsContainer && showHintsBtn) {
        if (hintsContainer.classList.contains('show')) {
            hintsContainer.classList.remove('show');
            showHintsBtn.textContent = 'ヒントを表示';
            console.log('Hints hidden');
        } else {
            hintsContainer.classList.add('show');
            showHintsBtn.textContent = 'ヒントを隠す';
            console.log('Hints shown');
        }
    } else {
        console.error('Elements not found - hintsContainer:', hintsContainer, 'showHintsBtn:', showHintsBtn);
    }
}

function revealHint(hintItem) {
    if (!hintItem.classList.contains('revealed')) {
        hintItem.classList.add('revealed');
        
        // 軽いアニメーション効果
        hintItem.style.transform = 'scale(1.02)';
        setTimeout(() => {
            hintItem.style.transform = 'scale(1)';
        }, 200);
    }
}

function handlePrint() {
    // 印刷前にすべてのヒントを表示状態にする
    const hintsContainers = document.querySelectorAll('.hints-container');
    hintsContainers.forEach(container => {
        container.classList.add('show');
    });
    
    // すべてのヒントを表示状態にする
    const hintItems = document.querySelectorAll('.hint-item');
    hintItems.forEach(item => {
        item.classList.add('revealed');
    });
    
    // 印刷実行
    window.print();
}

function showLoading() {
    hideAllSections();
    loadingSection.style.display = 'block';
}

function showError(message) {
    hideAllSections();
    errorText.textContent = message;
    errorSection.style.display = 'block';
}

function hideAllSections() {
    problemsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    errorSection.style.display = 'none';
}

function showInitialState() {
    // 初期状態では全てのセクションを非表示にして、エラーも表示しない
    hideAllSections();
    printBtn.disabled = true;
    
    // コンソールに初期化完了メッセージ
    console.log('数学文章問題ジェネレーター初期化完了');
}

// ユーティリティ関数
function getGradeName(grade) {
    const gradeNames = {
        1: '小学1年生', 2: '小学2年生', 3: '小学3年生',
        4: '小学4年生', 5: '小学5年生', 6: '小学6年生',
        7: '中学1年生', 8: '中学2年生', 9: '中学3年生',
        10: '高校1年生', 11: '高校2年生', 12: '高校3年生'
    };
    return gradeNames[grade] || `${grade}年生`;
}

function getDifficultyName(difficulty) {
    const difficultyNames = {
        1: '易しい',
        2: 'やや易しい',
        3: '普通',
        4: 'やや難しい',
        5: '難しい'
    };
    return difficultyNames[difficulty] || `難易度${difficulty}`;
}

// エラーハンドリング（問題生成後のみ）
let hasGeneratedProblems = false;

window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);
    // 問題生成を試行した後のみエラー表示
    if (hasGeneratedProblems) {
        showError('予期しないエラーが発生しました。ページを再読み込みしてください。');
    }
});

// 未処理のPromise拒否をキャッチ
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled Promise Rejection:', event.reason);
    // 問題生成を試行した後のみエラー表示
    if (hasGeneratedProblems) {
        showError('通信エラーが発生しました。インターネット接続を確認してください。');
    }
});

// デバッグ用（開発時のみ）
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.debugAPI = {
        getCurrentProblems: () => currentProblems,
        testAPI: async (grade = 3, difficulty = 2) => {
            try {
                const problems = await generateProblems(grade, difficulty);
                console.log('API Test Success:', problems);
                return problems;
            } catch (error) {
                console.error('API Test Failed:', error);
                throw error;
            }
        }
    };
}