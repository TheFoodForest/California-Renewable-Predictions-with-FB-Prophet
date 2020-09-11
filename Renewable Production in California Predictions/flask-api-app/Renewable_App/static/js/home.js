var url = '/api/renewable_prod/date/'
var total_url = '/api/total_production/'
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



    fetch(total_url + value).then( response => {
        return response.json();
    }).then(data => {

        var nuclear = 0
        var hydro = 0
        var renew = 0
        var thermal = 0

        for (var i = 0; i < Object.keys(data).length; i++){
            nuclear += data[Object.keys(data)[i]].nuclear;
            hydro += data[Object.keys(data)[i]].hydro;
            renew += data[Object.keys(data)[i]].renew;
            thermal += data[Object.keys(data)[i]].thermal;
        }
        var barOptions = {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Production By Source'
            },
            xAxis: {
                categories: ['']
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'MWh'
                },
                stackLabels: {
                    enabled: true,
                    style: {
                        fontWeight: 'bold',
                        color: ( // theme
                            Highcharts.defaultOptions.title.style &&
                            Highcharts.defaultOptions.title.style.color
                        ) || 'gray'
                    }
                }
            },
            legend: {
                align: 'right',
                x: -30,
                verticalAlign: 'top',
                y: 25,
                floating: true,
                backgroundColor:
                    Highcharts.defaultOptions.legend.backgroundColor || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false
            },
            tooltip: {
                headerFormat: '<b>{point.x}</b><br/>',
                pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: false
                    }
                }
            },
            series: [{
                name: 'Renewables',
                data: [renew]
            }, {
                name: 'Nuclear',
                data: [nuclear]
            }, {
                name: 'Thermal',
                data: [thermal]
            },
        {
            name: 'Hydro',
            data: [hydro]
        }]
        };

        

        Highcharts.chart('container-bar', barOptions)
    });



    
}


// just set the chart to show the middle date when loading the page 
optionChanged(dates[Math.ceil(maxIndex / 2)])

slider.onchange = function () {
    index = this.value;
    optionChanged(dates[index]);
}



