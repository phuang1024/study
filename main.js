console.log("hi");

let data = fetch("./content/test.json").then(response => response.json());
data.then(function(result) {
    console.log(result);
})
