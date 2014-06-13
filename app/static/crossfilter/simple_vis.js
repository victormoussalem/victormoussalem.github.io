/********************************************************
*                                                       *
*   dj.js example using Yelp Kaggle Test Dataset        *
*   Eamonn O'Loughlin 9th May 2013                      *
*                                                       *
********************************************************/
 
/********************************************************
*                                                       *
*   Step0: Load data from json file                     *
*                                                       *
********************************************************/
d3.json("dropbox_test_set_business.json", function (yelp_data) {
     
/********************************************************
*                                                       *
*   Step1: Create the dc.js chart objects & ling to div *
*                                                       *
********************************************************/
var bubbleChart = dc.bubbleChart("#dc-bubble-graph");
var pieChart = dc.pieChart("#dc-pie-graph");
var volumeChart = dc.barChart("#dc-volume-chart");
var lineChart = dc.lineChart("#dc-line-chart");
var dataTable = dc.dataTable("#dc-table-graph");
var rowChart = dc.rowChart("#dc-row-graph");
var other_rowChart = dc.rowChart("#other-dc-row-graph");
 
/********************************************************
*                                                       *
*   Step2:  Run data through crossfilter                *
*                                                       *
********************************************************/
var ndx = crossfilter(yelp_data);
     
/********************************************************
*                                                       *
*   Step3:  Create Dimension that we'll need            *
*                                                       *
********************************************************/
 
    // for volumechart
    var cityDimension = ndx.dimension(function (d) { return d.city; });
    var educationDimension = ndx.dimension(function (d) { return d.founder_education; });
    var cityGroup = cityDimension.group();
    var educationGroup = educationDimension.group();
    var cityDimensionGroup = cityDimension.group().reduce(
        //add
        function(p,v){
            ++p.count;
            p.review_sum += v.review_count;
            p.star_sum += v.stars;
            p.review_avg = p.review_sum / p.count;
            p.star_avg = p.star_sum / p.count;
            return p;
        },
        //remove
        function(p,v){
            --p.count;
            p.review_sum -= v.review_count;
            p.star_sum -= v.stars;
            p.review_avg = p.review_sum / p.count;
            p.star_avg = p.star_sum / p.count;
            return p;
        },
        //init
        function(p,v){
            return {count:0, review_sum: 0, star_sum: 0, review_avg: 0, star_avg: 0};
        }
    );
 
    // for pieChart
    var startValue = ndx.dimension(function (d) {
        return 3*1.0;
    });
    var startValueGroup = startValue.group();
 
    // For datatable
    var businessDimension = ndx.dimension(function (d) { return d.business_id; });
/********************************************************
*                                                       *
*   Step4: Create the Visualisations                    *
*                                                       *
********************************************************/
     
 bubbleChart.width(650)
            .height(300)
            .dimension(cityDimension)
            .group(cityDimensionGroup)
            .transitionDuration(1500)
            .colors(["#a60000","#ff0000", "#ff4040","#ff7373","#67e667","#39e639","#00cc00"])
            .colorDomain([-12000, 12000])
         
            .x(d3.scale.linear().domain([0, 5.5]))
            .y(d3.scale.linear().domain([0, 5.5]))
            .r(d3.scale.linear().domain([0, 2500]))
            .keyAccessor(function (p) {
                return p.value.star_avg;
            })
            .valueAccessor(function (p) {
                return p.value.review_avg;
            })
            .radiusValueAccessor(function (p) {
                return p.value.count;
            })
            .transitionDuration(1500)
            .elasticY(true)
            .yAxisPadding(1)
            .xAxisPadding(1)
            .label(function (p) {
                return p.key;
                })
            .renderLabel(true)
            .renderlet(function (chart) {
                rowChart.filter(chart.filter());
		other_rowChart.filter(chart.filter());
            })
            .on("postRedraw", function (chart) {
                dc.events.trigger(function () {
                    rowChart.filter(chart.filter());
		    other_rowChart.filter(chart.filter());
                });
	                });
            ;
 
 
pieChart.width(200)
        .height(200)
        .transitionDuration(1500)
        .dimension(startValue)
        .group(startValueGroup)
        .radius(90)
        .minAngleForLabel(0)
        .label(function(d) { return d.data.key; })
        .on("filtered", function (chart) {
            dc.events.trigger(function () {
                if(chart.filter()) {
                    console.log(chart.filter());
                    volumeChart.filter([chart.filter()-.25,chart.filter()-(-0.25)]);
                    }
                else volumeChart.filterAll();
            });
        });
 
volumeChart.width(230)
            .height(200)
            .dimension(startValue)
            .group(startValueGroup)
            .transitionDuration(1500)
            .centerBar(true)    
            .gap(17)
            .x(d3.scale.linear().domain([0.5, 5.5]))
            .elasticY(true)
            .on("filtered", function (chart) {
                dc.events.trigger(function () {
                    if(chart.filter()) {
                        console.log(chart.filter());
                        lineChart.filter(chart.filter());
                        }
                    else
                    {lineChart.filterAll()}
                });
            })
            .xAxis().tickFormat(function(v) {return v;});   
 
console.log(startValueGroup.top(1)[0].value);
 
lineChart.width(230)
        .height(200)
        .dimension(startValue)
        .group(startValueGroup)
        .x(d3.scale.linear().domain([0.5, 5.5]))
        .valueAccessor(function(d) {
            return d.value;
            })
            .renderHorizontalGridLines(true)
            .elasticY(true)
            .xAxis().tickFormat(function(v) {return v;});   ;
 
rowChart.width(340)
            .height(850)
            .dimension(cityDimension)
            .group(cityGroup)
            .renderLabel(true)
            .colors(["#a60000","#ff0000", "#ff4040","#ff7373","#67e667","#39e639","#00cc00"])
            .colorDomain([0, 0])
            .renderlet(function (chart) {
                bubbleChart.filter(chart.filter());
            })
            .on("filtered", function (chart) {
                dc.events.trigger(function () {
                    bubbleChart.filter(chart.filter());
                });
                        });
 
other_rowChart.width(340)
            .height(850)
            .dimension(educationDimension)
            .group(educationGroup)
            .renderLabel(true)
            .colors(["#a60000","#ff0000", "#ff4040","#ff7373","#67e667","#39e639","#00cc00"])
            .colorDomain([0, 0])
            .renderlet(function (chart) {
                bubbleChart.filter(chart.filter());
            })
            .on("filtered", function (chart) {
                dc.events.trigger(function () {
                    bubbleChart.filter(chart.filter());
                });
                        });

 
dataTable.width(800).height(800)
    .dimension(businessDimension)
    .group(function(d) { return "List of all Selected Acquisitions"
     })
    .size(100)
    .columns([
        function(d) { return d.name; },
        function(d) { return d.city; },
        function(d) { return d.date; },
        function(d) { return d.Categories; },
        function(d) { return d.founder_education}
    ])
    .sortBy(function(d){ return d.date; })
    // (optional) sort order, :default ascending
    .order(d3.descending);
/********************************************************
*                                                       *
*   Step6:  Render the Charts                           *
*                                                       *
********************************************************/
             
    dc.renderAll();
});
