//  WANT TO MAKE A CHANGE TO GET ALL DATA FOR THIS PAGE FOR 2019 AT ONCE
// THEN CAN CHART IT QUICKLY WITHOUT HAVING TO MAKE API CALLS ON EACH INPUT
// SLIDER MAKES INPUT FOR EVERY VLAUE DRAGGED ACROSS





const getDateArray = function(start, end) {
    var arr = {};
    var format = d3.timeFormat('%Y-%m-%d')
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
var trueUrl = '/api/renewable_prod/date/range/'

var sliderMin = document.getElementById('myRangeMin');
var sliderMax = document.getElementById('myRangeMax');

var dates = getDateArray(new Date('2019-01-01'), new Date('2019-09-15'))
// console.log(dates);
var minIndex = 0
var maxIndex = Object.keys(dates).length - 1
var midIndex = Math.ceil(maxIndex / 2)

// make it so the sliders can't overlap eachother - not the best for the user - but a working method
d3.select('#myRangeMin').attr('min', minIndex).attr('max', maxIndex - 1).attr('value', midIndex - 1);
d3.select('#myRangeMax').attr('min', minIndex + 1).attr('max', maxIndex).attr('value', midIndex + 1);

d3.select('#startDate').text(dates[midIndex - 1]);
d3.select('#endDate').text(dates[midIndex + 1]);




function getData (startDate, endDate) {


    var preds = fetch(predUrl + startDate + '/' + endDate).then( response => {
        return response.json();
    });

    var actual = fetch(trueUrl + startDate + '/' + endDate).then( response => {
        return response.json();
    });

    return {"preds":preds, "actuals":actual}
}


function createCompare(starDate, endDate) {

    var data = getData(starDate, endDate);
    var actuals = data['actuals'];
    var preds = data['preds'];

    console.log('preds');
    console.log(preds);

    console.log('actuals');
    console.log(actuals);

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
            pointFormat: 'Cases: {point.y:.2f}'
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
        colors: ['#000', '#FF0000', '#06C', '#FF7E00', '#910000'],
        // #2f7ed8, #0d233a, #8bbc21, #1aadce, #492970, #f28f43, #77a1e5, #c42525, #a6c96a, #ffffff
        series: [
        {
            name: "Renewable Preictions",
            data: []
        },
        {
            name: "Solar Predictions",
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


    Highcharts.chart('container', chartOptions)
}

// when min slider changes - aducst the graphs
sliderMin.oninput = function () {
    minSlider(this.value);
}
sliderMax.oninput = function () {
    maxSlider(this.value);
}




function minSlider(value) {
    console.log('MINSLIDER FUNCTION');
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
    console.log('MAXSLIDER FUNCTION');
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

