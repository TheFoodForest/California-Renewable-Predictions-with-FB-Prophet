var url = '/api/renewable_prod/date/'

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

var dates = getDateArray(new Date('2018-01-01'), new Date('2019-09-15'))

// get the values to fill in the slider with
var minIndex = d3.min(Object.keys(dates))
var maxIndex = d3.max(Object.keys(dates))

// get the slider
var slider = document.getElementById('myRange');



d3.select('#myrange').attr('min', minIndex).attr('max', maxIndex).attr('value', Math.ceil(maxIndex / 2));


function optionChanged(value) {
    fetch(url + value).then( response => {
        return response.json();
    }).then(data => {
        // console.log(data);
        // console.log(data.Hour);
        // console.log(data['Hour'].length);

        var hour = data.Hour.reverse();
   
        var renew = data['Renewable Production'].reverse();
        var total = data['Total Production'].reverse()
        var percent = data['Percent Production Renew'].reverse().map( value => Math.round(value * 100))
        var charOptions =  {
            chart: {
                type: 'area'
            },
            title: {
                text: 'Renewable and Total Production'
            },
            subtitle: {
                text: `${value}`
            },
            xAxis: {
                categories: [],
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'MWh'
                },
                labels: {
                    formatter: function () {
                        return this.value;
                    }
                }
            },
            
            plotOptions: {
                area: {
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#666666'
                    }
                }
            },
            series: [{
                name: 'Total Production',
                data: []
            }, {
                name: 'Renewable Production',
                data: []
            }],

            tooltip: {
                // shared: true, //makes all data for that time point visible
                useHTML: true, //allows for more custom and complicated tooltip design
                // headerFormat: '{point.key}<table>',
                // pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                //     '<td style="text-align: right"><b>{point.y} EUR</b></td></tr>',
                // footerFormat: '</table>',
                // valueDecimals: 2,
                formatter: function () {
                    return `<b>${value} ` + this.x + ":00:00" + "</b>" + "<br> " +this.series.name + ": <b>" + this.y
                    +"MWh</b><br> "  + "Percent Renewable Production: <b>" + this.point.myData + "%</b>" 
                + "<br>";
                }
                },
        };



        for (var i = 0; i < data['Hour'].length; i++) {

            charOptions['xAxis']['categories'].push(hour[i]);
            
            charOptions['series'][1]['data'].push({y:renew[i],
                                                    myData:percent[i]});
        
            
            charOptions['series'][0]['data'].push({y:total[i],
            myData:percent[i]});
            
           

        }
        // console.log(charOptions);// chart built from responce 
    Highcharts.chart('container', charOptions);

    });



    
}


// just set the chart to show the middle date when loading the page 
optionChanged(dates[Math.ceil(maxIndex / 2)])

slider.onchange = function () {
    index = this.value;
    optionChanged(dates[index]);
}