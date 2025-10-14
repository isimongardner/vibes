//let items = ['Birmingham', 'London', 'Manchester', 'Glasgow', 'Belfast', 'Cardiff'];
let items = [
    "Birmingham Bears",
    "Derbyshire Falcons",
    "Durham Cricket",
    "Lancashire Lightning",
    "Leicestershire Foxes",
    "Notts Outlaws",
    "Northamptonshire Steelbacks",
    "Worcestershire Rapids",
    "Yorkshire Vikings",
    "Essex Eagles",
    "Glamorgan",
    "Gloucestershire",
    "Hampshire Hawks",
    "Kent Spitfires",
    "Middlesex",
    "Somerset",
    "Surrey",
    "Sussex Sharks"
  ]

// Function to compare items
function compareItems(arr) {
    const comparisons = [];
    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr.length; j++) {
            if (i !== j) { // Compare only if the indices are different
                const comparison = {
                    item1: arr[i],
                    item2: arr[j],
                    result: arr[i] === arr[j] ? "Equal" : "Not Equal"
                };
                comparisons.push(comparison);
            }
        }
    }
    return comparisons;
}

// Compare items in the array
const result = compareItems(items);

// Output comparisons
console.log(`Number of matches:${result.length}`);
console.log(result)
