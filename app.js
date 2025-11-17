let correctAnswers = [];
let correctAnswers = [];

async function loadAnswers() {
    const res = await fetch("answers_20251117_231902.txt");
    const text = await res.text();

    // Split each answer by new line
    correctAnswers = text
        .split("\n")
        .map(line => line.trim())
        .filter(line => line.length > 0);
}
let questions = [];
let current = 0;
let answers = {}; // id -> selected option text
let totalTime = 5 * 60; // seconds (change if you want)
let timerInterval = null;

async function loadCorrectAnswers() {
  const res = await
    fetch("answers_20251117_231902.txt");
  const text = await res.text();

  correctAnswers = text
  .split("\n")
  .map(ans=>ans.trim())
  .filter(ans=>ans.length > 0);
  console.log("Loaded Correct Answers: ", correctAnswers);
}

async function startQuiz() {
    await loadAnswers();      // <-- loads answers
    await fetchQuestions();   // <-- loads questions
  renderQuestion();
  updateProgress();
  startTimer();
}

function renderQuestion(){
  if (!questions.length) return;
  const q = questions[current];
  document.getElementById("qtext").innerText = `Q${current+1}. ${q.q}`;
  const opts = document.getElementById("options");
  opts.innerHTML = "";
  q.options.forEach(opt=>{
    const div = document.createElement("div");
    div.className = "option";
    if (answers[q.id] === opt) div.classList.add("selected");
    div.innerText = opt;
    div.onclick = () => {
      answers[q.id] = opt;
      document.querySelectorAll(".option").forEach(o=>o.classList.remove("selected"));
      div.classList.add("selected");
      saveLocal();
    }
    // small stagger animation
    div.style.opacity = 0;
    opts.appendChild(div);
    setTimeout(()=>{ div.style.opacity = 1; div.style.transform = 'translateY(0)'; }, 50 + Math.random()*200);
  });
  updateProgress();
}

function prev(){
  if (current>0){ current--; renderQuestion(); }
}
function nextQ(){
  if (current < questions.length-1){ current++; renderQuestion(); }
}
function updateProgress(){
  const bar = document.getElementById("bar");
  const percent = ((current+1)/Math.max(1,questions.length))*100;
  bar.style.width = percent + "%";
}

function startTimer(){
  let left = totalTime;
  const el = document.getElementById("timer");
  if (!el) return;
  timerInterval = setInterval(()=>{
    left--;
    const mm = String(Math.floor(left/60)).padStart(2,"0");
    const ss = String(left%60).padStart(2,"0");
    el.innerText = `${mm}:${ss}`;
    if (left<=0){
      clearInterval(timerInterval);
      submitExam();
    }
  }, 1000);
}

function checkAnswer(user Answer) {
  const correct = correctAnswer[currentQuestionIndex];
  if
    (userAnswer.trim().tolowerCase() === correct.trim().tolowerCase()) {
      score++;
    }
  currentQuestionIndex++;
  loadnextQuestion();
}

function saveLocal(){
  try{ localStorage.setItem("neonexam_answers", JSON.stringify(answers)); }catch(e){}
}

function loadLocal(){
  try{ const d = JSON.parse(localStorage.getItem("neonexam_answers")||"{}"); answers = d; }catch(e){ answers = {}; }
  renderQuestion();
}

async function submitExam(){
  if (!confirm("Submit exam now?")) return;
  const payload = { answers: {} };
  questions.forEach(q=>{
    payload.answers[String(q.id)] = answers[q.id] || "";
  });

  const res = await fetch("/api/submit", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });

  if (!res.ok) { alert("Submission failed"); return; }
  const data = await res.json();
  showResult(data);
}
function checkAnswer(userAnswer) {
    const correct = correctAnswers[currentQuestionIndex];

    if (userAnswer.trim().toLowerCase() === correct.trim().toLowerCase()) {
        score++;
    }

    currentQuestionIndex++;

    if (currentQuestionIndex >= questions.length) {
        showScorePage();
    } else {
        renderQuestion();
        updateProgress();
        startTimer();
    }
}
function showScorePage() {
    document.getElementById("quiz-container").style.display = "none";
    document.getElementById("score-page").style.display = "block";

    document.getElementById("score-text").innerText =
        You scored ${score} out of ${questions.length};
}

function showResult(data){
  document.getElementById("resultPanel").classList.remove("hidden");
  document.getElementById("scoreText").innerText = `Score: ${data.score} / ${data.total}   (${data.percent}%)`;
  const wl = document.getElementById("wrongList");
  wl.innerHTML = "";
  if (data.wrong && data.wrong.length){
    data.wrong.forEach(w=>{
      const p = document.createElement("p");
      p.innerText = `Q${w.id}: Correct: ${w.correct}  |  Your: ${w.given}`;
      wl.appendChild(p);
    });
  } else {
    wl.innerText = "All correct — great job!";
  }
  const dl = document.getElementById("downloadCsv");
  dl.href = data.csv;
  dl.style.display = "inline-block";
  clearInterval(timerInterval);
}

function restartQuiz() {
    score = 0;
    currentQuestionIndex = 0;

    document.getElementById("score-page").style.display = "none";
    document.getElementById("quiz-container").style.display = "block";

    renderQuestion();
    updateProgress();
    startTimer();
}

document.addEventListener("DOMContentLoaded", ()=>{
  document.getElementById("prevBtn").onclick = prev;
  document.getElementById("nextBtn").onclick = nextQ;
  document.getElementById("saveBtn").onclick = ()=>{ saveLocal(); alert("Answers saved locally"); };
  startQuiz();
  loadLocal();
});



