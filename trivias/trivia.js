const timers = {};

    function startTimer(questionId, correctAnswer) {
        clearInterval(timers[questionId]);
        const timerSpan = document.getElementById(`timer-${questionId}`);
        const feedbackDiv = document.getElementById(`feedback-${questionId}`);
        const form = document.getElementById(`form-${questionId}`);
        let timeLeft = 15;

        timerSpan.innerText = timeLeft;
        timers[questionId] = setInterval(() => {
            timeLeft--;
            timerSpan.innerText = timeLeft;

            if (timeLeft <= 0) {
                clearInterval(timers[questionId]);
                const inputs = form.querySelectorAll(`input[name="question${questionId}"]`);
                inputs.forEach(input => input.disabled = true);
                feedbackDiv.innerHTML = `<span class="text-danger">Time's up! The correct answer is: <strong>${correctAnswer}</strong></span>`;
                form.querySelector('button[type="submit"]').disabled = true;
            }
        }, 1000);
    }

    function checkAnswer(event, questionId, correctAnswer) {
        event.preventDefault();
        const form = document.getElementById(`form-${questionId}`);
        const selected = form.querySelector(`input[name="question${questionId}"]:checked`);
        const feedbackDiv = document.getElementById(`feedback-${questionId}`);

        if (!selected) {
            feedbackDiv.innerHTML = '<span class="text-warning">Please select an answer.</span>';
            return;
        }

        clearInterval(timers[questionId]);
        const inputs = form.querySelectorAll(`input[name="question${questionId}"]`);
        inputs.forEach(input => input.disabled = true);

        if (selected.value === correctAnswer) {
            feedbackDiv.innerHTML = '<span class="text-success">Correct!</span>';
        } else {
            feedbackDiv.innerHTML = `<span class="text-danger">Incorrect. The correct answer is: <strong>${correctAnswer}</strong></span>`;
        }

        form.querySelector('button[type="submit"]').disabled = true;
    }
