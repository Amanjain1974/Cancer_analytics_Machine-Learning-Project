function initializeCharts(positive,negative){
new Chart(document.getElementById("pieChart"),{
type:"pie",
data:{labels:["Positive","Negative"],
datasets:[{data:[positive,negative]}]}
});

new Chart(document.getElementById("barChart"),{
type:"bar",
data:{labels:["Positive","Negative"],
datasets:[{label:"Predictions",data:[positive,negative]}]}
});
}
