queue()
    .defer(d3.json, '/create_graph_data')
    .await(makeGraphs);
    
function makeGraphs(error, graphData){
    
    var ndx = crossfilter(graphData);
    
    cuisineChart(ndx);
    cuisineChartMobile(ndx)
    allergenChart(ndx);
    allergenChartMobile(ndx)
    cuisineTimeCorrelation(ndx);
    cuisineTimeCorrelationMobile(ndx)
    
    dc.renderAll();
}

function cuisineChart(ndx){
    
    var dim = ndx.dimension(dc.pluck('cuisine'));
    var group = dim.group();
    
    dc.pieChart('#cuisine-chart')
        .width(500)
        .height(350)
        .dimension(dim)
        .group(group)
        .transitionDuration(500)
        .legend(dc.legend().x(400).y(50).itemHeight(10).gap(5))
        .externalRadiusPadding(50)
        .minAngleForLabel(361);
}

function cuisineChartMobile(ndx){
    
    var dim = ndx.dimension(dc.pluck('cuisine'));
    var group = dim.group();
    
    dc.pieChart('#cuisine-chart-mobile')
        .width(300)
        .height(200)
        .dimension(dim)
        .group(group)
        .transitionDuration(500)
        .legend(dc.legend().x(255).y(0).itemHeight(10).gap(5))
        .minAngleForLabel(361);
}

function allergenChart(ndx){
    
    var dim = ndx.dimension(dc.pluck('allergen'));
    var group = dim.group();
    
    dc.pieChart('#allergens-chart')
        .width(500)
        .height(350)
        .dimension(dim)
        .group(group)
        .transitionDuration(500)
        .legend(dc.legend().x(400).y(50).itemHeight(10).gap(5))
        .externalRadiusPadding(50)
        .minAngleForLabel(361);
}

function allergenChartMobile(ndx){
    
    var dim = ndx.dimension(dc.pluck('allergen'));
    var group = dim.group();
    
    dc.pieChart('#allergens-chart-mobile')
        .width(300)
        .height(200)
        .dimension(dim)
        .group(group)
        .transitionDuration(500)
        .legend(dc.legend().x(255).y(0).itemHeight(10).gap(5))
        .minAngleForLabel(361);
}

function cuisineTimeCorrelation(ndx){
    
    var dim = ndx.dimension(dc.pluck("cuisine"));
    
    function add_item(p, v){
        p.count++;
        p.total += v.time;
        p.average = p.total / p.count;
        return p;
    }
    
    function remove_item(p, v){
        p.count--;
        
        if(p.count === 0){
            p.total = 0;
            p.average = 0;
        } else {
            p.total -= v.time;
            p.average = p.total / p.count;
        }
        return p;
    }
    
    function initialise(){
        return {count: 0, total: 0, average: 0}
    }
    
    var averageTimeByCuisine = dim.group().reduce(add_item, remove_item, initialise);
    
    dc.barChart("#cuisine-time-correlation")
        .width($('#cuisine-time-correlation').parent().width())
        .height(500)
        .margins({top: 10, right: 50, bottom: 100, left: 50})
        .dimension(dim)
        .group(averageTimeByCuisine)
        .valueAccessor(function(d){
            return d.value.average.toFixed(2);
        })
        .transitionDuration(500)
        .elasticY(false)
        .x(d3.scale.ordinal())
        .y(d3.scale.linear().domain([0, 180]))
        .xUnits(dc.units.ordinal)
        .yAxisLabel("Time (mins)")
        .yAxis().ticks(10);
}

function cuisineTimeCorrelationMobile(ndx){
    
    var dim = ndx.dimension(dc.pluck("cuisine"));
    
    function add_item(p, v){
        p.count++;
        p.total += v.time;
        p.average = p.total / p.count;
        return p;
    }
    
    function remove_item(p, v){
        p.count--;
        
        if(p.count === 0){
            p.total = 0;
            p.average = 0;
        } else {
            p.total -= v.time;
            p.average = p.total / p.count;
        }
        return p;
    }
    
    function initialise(){
        return {count: 0, total: 0, average: 0}
    }
    
    var averageTimeByCuisine = dim.group().reduce(add_item, remove_item, initialise);
    
    dc.barChart("#cuisine-time-correlation-mobile")
        .width($('#cuisine-time-correlation-mobile').parent().width())
        .height(350)
        .margins({top: 10, right: 10, bottom: 70, left: 25})
        .dimension(dim)
        .group(averageTimeByCuisine)
        .valueAccessor(function(d){
            return d.value.average.toFixed(2);
        })
        .transitionDuration(500)
        .elasticY(false)
        .x(d3.scale.ordinal())
        .y(d3.scale.linear().domain([0, 180]))
        .xUnits(dc.units.ordinal)
        .yAxis().ticks(10);
}