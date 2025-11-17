let questions = [];
let correctAnswers = [];
let current = 0;
let answers = {};
let score = 0;
let timerInterval = null;
let timeLeft = 300; // 5 minutes

// ------------------------------
// LOAD QUESTIONS + ANSWERS
// ------------------------------
async function loadQuestions() {
    const res = await fetch("questions.json");
    questions = await res.json();
}

async function loadCorrectAnswers() {
    const res = await fetch("answers_20251117_231902.txt");
    const text = await res.text();
    correctAnswers = text.split("\n").map(a => a.trim());
}

// ------------------------------
// START QUIZ
// ------------------------------
async function startQuiz() {
    await loadQuestions();
    await loadCorrectAnswers();
    renderQuestion();
    startTimer();
    updateProgress();
}

// ------------------------------
// RENDER QUESTION
// ------------------------------
function renderQuestion() {
    const q = questions[current];
    document.getElementById("qtext").innerText = Q${current + 1}. ${q.q};

    const opts = document.getElementById("options");
    opts.innerHTML = "";

    q.options.forEach(opt => {
        const div = document.createElement("div");
        div.className = "option";
        div.innerText = opt;

        if (answers[current] === opt) div.classList.add("selected");

        div.onclick = () => {
            answers[current] = opt;
            document.querySelectorAll(".option").forEach(e => e.classList.remove("selected"));
            div.classList.add("selected");
        };

        opts.appendChild(div);
    });
}

// ------------------------------
// NAVIGATION
// ------------------------------
function nextQ() {
    if (current < questions.length - 1) {
        current++;
        renderQuestion();
        updateProgress();
    } else {
        finishQuiz();
    }
}

function prevQ() {
    if (current > 0) {
        current--;
        renderQuestion();
        updateProgress();
    }
}

function updateProgress() {
    const bar = document.getElementById("bar");
    bar.style.width = ((current + 1) / questions.length) * 100 + "%";
}

// ------------------------------
// TIMER
// ------------------------------
function startTimer() {
    timerInterval = setInterval(() => {
        timeLeft--;
        const mm = String(Math.floor(timeLeft / 60)).padStart(2, "0");
        const ss = String(timeLeft % 60).padStart(2, "0");
        document.getElementById("timer").innerText = ${mm}:${ss};

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            finishQuiz();
        }
    }, 1000);
}

// ------------------------------
// FINISH QUIZ
// ------------------------------
function finishQuiz() {
    clearInterval(timerInterval);

    score = 0;
    questions.forEach((q, index) => {
        if (
            answers[index] &&
            answers[index].toLowerCase().trim() === correctAnswers[index].toLowerCase().trim()
        ) {
            score++;
        }
    });

    // hide quiz
    document.getElementById("quiz-container").style.display = "none";

    // show score
    document.getElementById("score-page").style.display = "block";
    document.getElementById("score-text").innerText =
        You scored ${score} / ${questions.length};
}

function restartQuiz() {
    current = 0;
    answers = {};
    score = 0;
    timeLeft = 300;

    document.getElementById("quiz-container").style.display = "block";
    document.getElementById("score-page").style.display = "none";

    renderQuestion();
    startTimer();
    updateProgress();
}

// ------------------------------
// BUTTON EVENTS
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("nextBtn").onclick = nextQ;
    document.getElementById("prevBtn").onclick = prevQ;
    document.getElementById("saveBtn").onclick = () =>
        alert("Saved locally (not needed).");

    startQuiz();
});
