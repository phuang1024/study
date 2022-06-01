let category;
let correct_ind;
let user_prompt;
let user_correct;
const user_choices = [null, null, null, null];

/**
 * Start inclusive, end exclusive.
 */
function randint(start, end) {
    return Math.floor(Math.random() * (end-start)) + start;
}


function getWrongs(length, correct) {
    const choices = [];
    while (choices.length < 3) {
        let index = randint(0, length);
        if (index == correct || choices.includes(index))
            continue;
        choices.push(index);
    }

    return choices;
}


function setChoice(index, content) {
    document.getElementById("word"+(index+1)).innerHTML = content;
    user_choices[index] = content;
}


function initialize() {
    document.getElementById("last").style.display = "none";
    category = "spanish";
    setContent();
}


function setContent() {
    let json = fetch("./content/" + category + ".json").then(response => response.json());
    json.then(function(data) {
        let zero = randint(0, 2);
        let one = (zero == 0) ? 1 : 0;

        correct_ind = randint(0, 4);
        let correct = randint(0, data.length);
        let wrongs = getWrongs(data.length, correct);

        document.getElementById("ans").innerHTML = data[correct][zero];
        user_prompt = data[correct][zero];
        user_correct = data[correct][one];

        let next = 0;
        for (let i = 0; i < 4; i++) {
            if (i == correct_ind) {
                setChoice(i, data[correct][one]);
            } else {
                setChoice(i, data[wrongs[next]][one]);
                next++;
            }
        }
    })
}


function answer(index) {
    document.getElementById("last").style.display = "block";

    let isCorrect = document.getElementById("isCorrect");
    if (index == correct_ind) {
        isCorrect.innerHTML = "<p>Correct</p>";
    } else {
        let html = "<p>Incorrect.</p>";
        html += "<p>- Prompt: <b>" + user_prompt + "</b></p>";
        html += "<p>- Correct: <b>" + user_correct + "</b></p>";
        html += "<p>- Your choice: <b>" + user_choices[index] + "</b></p>";
        isCorrect.innerHTML = html;
    }

    setContent();
}
