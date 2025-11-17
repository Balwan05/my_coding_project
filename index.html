let questions = [];
let correctAnswers = [];
let current = 0;
let answers = {}; 
let score = 0;

let totalTime = 5 * 60; 
let timerInterval = null;

// ---------------------- LOAD ANSWERS ----------------------
async function loadAnswers() {
    const res = await fetch("answers_20251117_231902.txt");
    const text = await res.text();

    correctAnswers = text
        .split("\n")
        .map(a => a.trim())
        .filter(a => a.length > 0);

    console.log("Loaded correct answers:", correctAnswers);
}

// ---------------------- LOAD QUESTIONS ----------------------
async function fetchQuestions() {
    const res = await fetch("questions.json");
    const data = await res.json();
    questions = data;
}

// ---------------------- START QUIZ ----------------------
async function startQuiz() {
    await loadAnswers();
    await fetchQuestions();

    renderQuestion();
    updateProgress();
    startTimer();
}

// ---------------------- RENDER QUESTION ----------------------
function renderQuestion(){
  if (!questions.length) return;

  const q = questions[current];

  document.getElementById("qtext").innerText = Q${current+1}. ${q.q};

  const opts = document.getElementById("options");
  opts.innerHTML = "";

  q.options.forEach(opt => {
    const div = document.createElement("div");
    div.className = "option";
    
    if (answers[current] === opt) div.classList.add("selected");

    div.innerText = opt;
    div.onclick = () => {
      answers[current] = opt;
      document.querySelectorAll(".option").forEach(o => o.classList.remove("selected"));
      div.classList.add("selected");
      saveLocal();
    };

    div.style.opacity = 0;
    opts.appendChild(div);
    setTimeout(() => { 
      div.style.opacity = 1; 
      div.style.transform = "translateY(0)"; 
    }, 50);
  });

  updateProgress();
}

// ---------------------- NAVIGATION ----------------------
function prev(){
  if (current > 0){ 
    current--; 
    renderQuestion(); 
  }
}

function nextQ(){
  if (current < questions.length - 1){
    current++; 
    renderQuestion();
  } else {
    submitExam();
  }
}

// ---------------------- PROGRESS ----------------------
function updateProgress(){
  const bar = document.getElementById("bar");
  const percent = ((current+1) / Math.max(1, questions.length)) * 100;
  bar.style.width = percent + "%";
}

// ---------------------- TIMER ----------------------
function startTimer(){
  let left = totalTime;
  const el = document.getElementById("timer");

  timerInterval = setInterval(() => {
    left--;
    const mm = String(Math.floor(left/60)).padStart(2,"0");
    const ss = String(left%60).padStart(2,"0");
    el.innerText = ${mm}:${ss};

    if (left <= 0){
      clearInterval(timerInterval);
      submitExam();
    }
  }, 1000);
}

// ---------------------- SUBMIT (LOCAL SCORING) ----------------------
function submitExam(){
  if (!confirm("Submit exam now?")) return;

  // calculate score
  score = 0;
  const wrongList = document.getElementById("wrongList");
  wrongList.innerHTML = "";

  questions.forEach((q, index) => {
    const userAns = answers[index] || "";
    const correct = correctAnswers[index];

    if (userAns.trim().toLowerCase() === correct.trim().toLowerCase()) {
      score++;
    } else {
      const p = document.createElement("p");
      p.innerText = Q${index+1}: Correct → ${correct} | Your → ${userAns};
      wrongList.appendChild(p);
    }
  });

  showResultLocal();
}

// ---------------------- SHOW RESULT ----------------------
function showResultLocal() {
    document.getElementById("card").classList.add("hidden");
    document.getElementById("resultPanel").classList.remove("hidden");

    document.getElementById("scoreText").innerText =
        Score: ${score} / ${questions.length};

    clearInterval(timerInterval);
}

// ---------------------- LOCAL SAVE / LOAD ----------------------
function saveLocal(){
  localStorage.setItem("neonexam_answers", JSON.stringify(answers));
}

function loadLocal(){
  const d = JSON.parse(localStorage.getItem("neonexam_answers") || "{}");
  answers = d;
}

// ---------------------- INIT ----------------------
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("prevBtn").onclick = prev;
  document.getElementById("nextBtn").onclick = nextQ;
  document.getElementById("saveBtn").onclick = () => { 
    saveLocal(); 
    alert("Answers saved locally");
  };

  loadLocal();
  startQuiz();
});
