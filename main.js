let correct_ind;  // Correct choice index

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
}

function setContent() {
    let json = fetch("./content/test.json").then(response => response.json());
    json.then(function(data) {
        correct_ind = randint(0, 4);
        let correct = randint(0, data.length);
        let wrongs = getWrongs(data.length, correct);

        document.getElementById("ans").innerHTML = data[correct][0];

        let next = 0;
        for (let i = 0; i < 4; i++) {
            if (i == correct_ind) {
                setChoice(i, data[correct][0]);
            } else {
                setChoice(i, data[wrongs[next]][1]);
                next++;
            }
        }
    })
}
