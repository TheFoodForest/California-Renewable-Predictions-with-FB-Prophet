//  WANT TO MAKE A CHANGE TO GET ALL DATA FOR THIS PAGE FOR 2019 AT ONCE
// THEN CAN CHART IT QUICKLY WITHOUT HAVING TO MAKE API CALLS ON EACH INPUT
// SLIDER MAKES INPUT FOR EVERY VLAUE DRAGGED ACROSS



const format = d3.timeFormat('%Y-%m-%d')

const getDateArray = function(start, end) {
    var arr = {};
    
    var dt = new Date(start);
    var counter = 0;
    while (dt <= end) {
        arr[counter] = format(new Date(dt));
        dt.setDate(dt.getDate() + 1);
        counter++;
    }
    return arr;
}


var predUrl = '/api/predictions/date/range/'
var trueUrl = '/api/renewable_production/date/range/'

var sliderMin = document.getElementById('myRangeMin');
var sliderMax = document.getElementById('myRangeMax');

var dates = getDateArray(new Date('2019-01-01'), new Date('2019-12-31'))
// console.log(dates);
var minIndex = 0
var maxIndex = Object.keys(dates).length - 1
var midIndex = Math.ceil(maxIndex / 2)

// make it so the sliders can't overlap eachother - not the best for the user - but a working method
d3.select('#myRangeMin').attr('min', minIndex).attr('max', maxIndex - 1).attr('value', midIndex - 1);
d3.select('#myRangeMax').attr('min', minIndex + 1).attr('max', maxIndex).attr('value', midIndex + 1);

d3.select('#startDate').text(dates[midIndex - 1]);
d3.select('#endDate').text(dates[midIndex + 1]);



// function called on page load to get all of the production and predictions for 2019
 function getData (startDate, endDate) {

    let preds = fetch(predUrl + startDate + '/' + endDate).then( response => {
        return response.json();
    });

    let actuals = fetch(trueUrl + startDate + '/' + endDate).then( response => {
        return response.json();
    });

    return {'preds':preds, 'actuals':actuals}
}


// get the data for 2019
var data = getData(dates[0], dates[Object.keys(dates).length - 1])



function createCompareTotal(startDate, endDate) {


    function filterDates (date) {
        d = format(new Date(date))
        return (d >= startDate && d <= endDate)
    }
    
    // var test = [];
    // data['preds'].then(data => Object.keys(data).forEach( d => test.push(d)))
    // console.log(test);
    // let result = mykeys.reduce((r,k) => r.concat(predictions[]))

    var chartOptions = {
        chart: {
            type: 'spline',
            zoomType: 'x'
        },
        title: {
            text: 'Predictions Vs True - Renewable Production'
        },
        subtitle: {
            text: 'Facebook Prophet vs. TensorFlow LSTM'
        },
        credits: {
            enabled: false
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                year: '%Y'
            },
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'Number <br> of cases',
                rotation: 0
            },
            min: 0
        },
        tooltip: {
            pointFormat: '{series.name}: {point.y:.2f}'
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: false
                },
                label:{
                    enabled: false
                }
            }
        },
        colors: [ '#06C', '#FF7E00', '#910000'],
        // #2f7ed8, #0d233a, #8bbc21, #1aadce, #492970, #f28f43, #77a1e5, #c42525, #a6c96a, #ffffff
        series: [
        {
            name: "Renewable Predictions",
            data: []
        },
        {
            name: "True Renewable Production",
            data: []
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 1200
                }
            }]
        }
    }

    // console.log('actuals');
    // console.log(actuals);
    // console.log('preds');
    // console.log(preds);


    let filteredPred = data['preds']
        .then(data => {
            return Object.keys(data)
            .filter(filterDates).reduce((obj, key) => {
                obj[key] = data[key];
                return obj;
              }, {})
            }
            ).then(data => {
                Object.entries(data).forEach(item => {
                    chartOptions.series[0].data.push([Date.parse(item[0]), Math.ceil(item[1].predTotal)]);
                })
                Highcharts.chart('container', chartOptions);
            });

        let filteredActual = data['actuals']
        .then(data => {
            return Object.keys(data)
            .filter(filterDates).reduce((obj, key) => {
                obj[key] = data[key];
                return obj;
                }, {})
            }
            ).then(data => {
                Object.entries(data).forEach(item => {
                    chartOptions.series[1].data.push([Date.parse(item[0]), Math.ceil(item[1].total)]);
                })
                Highcharts.chart('container', chartOptions);
            });

}


sliderMin.oninput = function () {
    minSlider(this.value);
}
sliderMax.oninput = function () {
    maxSlider(this.value);
}

sliderMin.onchange = function() {
    let indexMin = parseInt(this.value);
    let indexMax = parseInt(d3.select('#myRangeMax').attr('value'));
    createCompareTotal(dates[indexMin], dates[indexMax])
}

sliderMax.onchange = function() {
    let indexMax = parseInt(this.value);
    let indexMin = parseInt(d3.select('#myRangeMin').attr('value'));
    createCompareTotal(dates[indexMin], dates[indexMax])
}




function minSlider(value) {
    
    let indexMin = parseInt(value);
    d3.select('#myRangeMin').attr('value',indexMin);
    let indexMax = parseInt(d3.select('#myRangeMax').attr('value'));
    // make it so the sliders can't overlap eachother - not the best for the user - but a working method
    if (indexMin > indexMax) {
        indexMax = indexMin + 1;
        d3.select('#myRangeMax').property('value', indexMax).attr('value',indexMax);
    }
    d3.select('#startDate').text(dates[indexMin]);
    d3.select('#endDate').text(dates[indexMax]);
    
}
function maxSlider(value) {
    
    let indexMax = parseInt(value);
    d3.select('#myRangeMax').attr('value',indexMax);
    let indexMin = parseInt(d3.select('#myRangeMin').attr('value')); // if I don't use D3 and just use sliderMax.value - it has strange behavior 
    // make it so the sliders can't overlap eachother - not the best for the user - but a working method
    if (indexMax < indexMin) {
        indexMin = indexMax - 1;
        d3.select('#myRangeMin').property('value', indexMin).attr('value',indexMin);
    };
    d3.select('#startDate').text(dates[indexMin]);
    d3.select('#endDate').text(dates[indexMax]);
}

createCompareTotal(dates[midIndex - 1], dates[midIndex + 1])





var sliderMinS = document.getElementById('myRangeMinSolar');
var sliderMaxS = document.getElementById('myRangeMaxSolar');

// make it so the sliders can't overlap eachother - not the best for the user - but a working method
d3.select('#myRangeMinSolar').attr('min', minIndex).attr('max', maxIndex - 1).attr('value', midIndex - 1);
d3.select('#myRangeMaxSolar').attr('min', minIndex + 1).attr('max', maxIndex).attr('value', midIndex + 1);

d3.select('#startDateSolar').text(dates[midIndex - 1]);
d3.select('#endDateSolar').text(dates[midIndex + 1]);



function createCompareSolar(startDate, endDate) {


    function filterDates (date) {
        d = format(new Date(date))
        return (d >= startDate && d <= endDate)
    }
    
    // var test = [];
    // data['preds'].then(data => Object.keys(data).forEach( d => test.push(d)))
    // console.log(test);
    // let result = mykeys.reduce((r,k) => r.concat(predictions[]))

    var chartOptionsSolar = {
        chart: {
            type: 'spline',
            zoomType: 'x'
        },
        title: {
            text: 'Predictions Vs True - Solar Energy Production'
        },
        subtitle: {
            text: ''
        },
        credits: {
            enabled: false
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                year: '%Y'
            },
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'MWh',
                rotation: 0
            },
            min: 0
        },
        tooltip: {
            pointFormat: '{series.name}: {point.y:.2f}'
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: false
                },
                label:{
                    enabled: false
                }
            }
        },
        colors: [ '#06C', '#FF7E00', '#910000'],
        // #2f7ed8, #0d233a, #8bbc21, #1aadce, #492970, #f28f43, #77a1e5, #c42525, #a6c96a, #ffffff
        series: [
        {
            name: "Renewable Predictions",
            data: []
        },
        {
            name: "True Renewable Production",
            data: []
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 1200
                }
            }]
        }
    }

    // console.log('actuals');
    // console.log(actuals);
    // console.log('preds');
    // console.log(preds);


    let filteredPred = data['preds']
        .then(data => {
            return Object.keys(data)
            .filter(filterDates).reduce((obj, key) => { // this reduces down the dates to dates between start and end Date - defined above
                obj[key] = data[key];                   // then have to reduce the object down to the keys that have be maked to true
                return obj;
              }, {})
            }
            ).then(data => {
                Object.entries(data).forEach(item => {
                    chartOptionsSolar.series[0].data.push([Date.parse(item[0]), Math.ceil(item[1].predSolar)]);
                })
                Highcharts.chart('container-solar', chartOptionsSolar);
            });

        let filteredActual = data['actuals']
        .then(data => {
            return Object.keys(data)
            .filter(filterDates).reduce((obj, key) => {
                obj[key] = data[key];
                return obj;
                }, {})
            }
            ).then(data => {
                Object.entries(data).forEach(item => {
                    chartOptionsSolar.series[1].data.push([Date.parse(item[0]), Math.ceil(item[1].solar)]);
                })
                Highcharts.chart('container-solar', chartOptionsSolar);
            });


    
}


sliderMinS.oninput = function () {
    minSliderS(this.value);
}
sliderMaxS.oninput = function () {
    maxSliderS(this.value);
}

sliderMinS.onchange = function() {
    let indexMin = parseInt(this.value);
    let indexMax = parseInt(d3.select('#myRangeMaxSolar').attr('value'));
    createCompareSolar(dates[indexMin], dates[indexMax])
}

sliderMaxS.onchange = function() {
    let indexMax = parseInt(this.value);
    let indexMin = parseInt(d3.select('#myRangeMinSolar').attr('value'));
    createCompareSolar(dates[indexMin], dates[indexMax])
}




function minSliderS(value) {
    
    let indexMin = parseInt(value);
    d3.select('#myRangeMinSolar').attr('value',indexMin);
    let indexMax = parseInt(d3.select('#myRangeMaxSolar').attr('value'));
    // make it so the sliders can't overlap eachother - not the best for the user - but a working method
    if (indexMin > indexMax) {
        indexMax = indexMin + 1;
        d3.select('#myRangeMaxSolar').property('value', indexMax).attr('value',indexMax);
    }
    d3.select('#startDateSolar').text(dates[indexMin]);
    d3.select('#endDateSolar').text(dates[indexMax]);
    
}
function maxSliderS(value) {
    
    let indexMax = parseInt(value);
    d3.select('#myRangeMaxSolar').attr('value',indexMax);
    let indexMin = parseInt(d3.select('#myRangeMinSolar').attr('value')); // if I don't use D3 and just use sliderMax.value - it has strange behavior 
    // make it so the sliders can't overlap eachother - not the best for the user - but a working method
    if (indexMax < indexMin) {
        indexMin = indexMax - 1;
        d3.select('#myRangeMinSolar').property('value', indexMin).attr('value',indexMin);
    };
    d3.select('#startDateSolar').text(dates[indexMin]);
    d3.select('#endDateSolar').text(dates[indexMax]);
}

createCompareSolar(dates[midIndex - 1], dates[midIndex + 1])




