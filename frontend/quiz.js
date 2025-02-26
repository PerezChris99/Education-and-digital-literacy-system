// Quiz logic
function displayQuiz(quizData) {
    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = '<h2>Quiz</h2>';

    if (!quizData || !Array.isArray(quizData.questions)) {
        contentDiv.innerHTML += '<p>No quiz questions available.</p>';
        return;
    }

    const quizForm = document.createElement('form');
    quizData.questions.forEach((question, questionIndex) => {
        const questionDiv = document.createElement('div');
        questionDiv.innerHTML = `<p>${questionIndex + 1}. ${question.text}</p>`;

        question.answers.forEach((answer, answerIndex) => {
            const answerInput = document.createElement('input');
            answerInput.type = 'radio';
            answerInput.name = `question-${questionIndex}`;
            answerInput.value = answerIndex;
            answerInput.id = `question-${questionIndex}-answer-${answerIndex}`;

            const answerLabel = document.createElement('label');
            answerLabel.innerText = answer.text;
            answerLabel.setAttribute('for', `question-${questionIndex}-answer-${answerIndex}`);

            questionDiv.appendChild(answerInput);
            questionDiv.appendChild(answerLabel);
            questionDiv.appendChild(document.createElement('br'));
        });

        quizForm.appendChild(questionDiv);
    });

    const submitButton = document.createElement('button');
    submitButton.innerText = 'Submit Quiz';
    submitButton.type = 'button';
    submitButton.onclick = function() {
        gradeQuiz(quizData);
    };
    quizForm.appendChild(submitButton);

    contentDiv.appendChild(quizForm);
}

function gradeQuiz(quizData) {
    let score = 0;
    quizData.questions.forEach((question, questionIndex) => {
        const selectedAnswer = document.querySelector(`input[name="question-${questionIndex}"]:checked`);
        if (selectedAnswer) {
            const answerIndex = parseInt(selectedAnswer.value);
            if (question.answers[answerIndex].correct) {
                score++;
            }
        }
    });

    alert(`You scored ${score} out of ${quizData.questions.length}`);
}
