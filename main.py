## Importing required functions --------------------------------
import random
from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.palettes import Accent4
from bokeh.models import ColumnDataSource, FactorRange

## Flask constructor -------------------------------------------
app = Flask(__name__)

## Root endpoint -----------------------------------------------
@app.route('/')
def homepage():
    ############################################################
    # Basic Bar Chart
    ############################################################
    language   = [
        'Python', 'Java', 'JavaScript', 'C#', 'PHP', 'C/C++', 
        'R', 'Objective-C', 'Swift', 'TypeScript', 'Matlab', 
        'Kotlin', 'Go', 'Ruby', 'VBA'
    ]

    popularity = [
        31.56, 16.4, 8.38, 6.5, 5.85, 5.8, 4.08, 2.79, 2.35, 
        1.92, 1.65, 1.61, 1.44, 1.22, 1.16
    ]

    p1 = figure(
        x_range = language,
        height  = 400,
        title   = "Popularity of Programming Languages",
        sizing_mode = "stretch_width"
    )

    p1.vbar(x = language, top = popularity, width = 0.5)
    p1.xgrid.grid_line_color = None
    p1.y_range.start = 0

    ############################################################
    # Stacking Bar Chart
    ############################################################
    months   = ['January', 'February', 'March', 'April', 'May', 'June']
    category = ['Travel', 'Food', 'Rent', 'Other']

    data = {
        'Months' : months,
        'Travel' : [2121, 1980, 2090, 1553, 2391, 2780],
        'Food'   : [5681, 4300, 6955, 5100, 4911, 6245],
        'Rent'   : [9000, 9000, 9000, 9000, 9000, 9000],
        'Other'  : [13490, 4245, 6810, 22390, 2900, 7649],
    }

    p2 = figure(
        x_range  = months,
        height   = 350,
        title    = 'Expenses by Month',
        tools    = 'hover',
        tooltips ='$name @months: @$name',
    )

    p2.vbar_stack(
        stackers     = category,
        x            = 'Months',
        width        = 0.9,
        color        = Accent4,
        source       = data,
        legend_label = category,
    )

    p2.y_range.start              = 0
    p2.x_range.range_padding      = 0.1
    p2.xgrid.grid_line_color      = None
    p2.axis.minor_tick_line_color = None
    p2.outline_line_color         = None
    p2.legend.location            = 'top_left'
    p2.legend.orientation         = 'horizontal'
    
    ############################################################
    # Grouped Bar Chart
    ############################################################
    country = ['USA', 'China', 'Japan', 'UK', 'India']
    years   = ['2010', '2015', '2020']
    
    data = {
        'Country': country,
        '2010': ['14964', '5812', '5793', '2246', '1729'],
        '2015': ['18036', '11226', '4382', '2863', '2088'],
        '2020': ['20936', '14772', '5064', '2707', '2622']
    }

    x = [(cntry, year) for cntry in country for year in years]

    counts = sum(zip(data['2010'], data['2015'], data['2020']), ())
    source = ColumnDataSource(data = dict(x = x, counts = counts))

    p3 = figure(
        x_range = FactorRange(*x),
        height  = 350,
        title   = "Country GDP by Year",
        tools   = ""
    )

    p3.vbar(x='x', top='counts', width=0.7, source=source)
    p3.y_range.start = 0
    p3.x_range.range_padding = 0.1
    p3.xaxis.major_label_orientation = 1
    p3.xgrid.grid_line_color = None

    ##### Return all the charts to the HTML template #####
    script1, div1 = components(p1)
    script2, div2 = components(p2)
    script3, div3 = components(p3)

    return render_template(
        template_name_or_list = 'bar-charts.html',
        script  = [script1, script2, script3],
        div     = [div1, div2, div3],
    )

## Main Driver Function ----------------------------------------
if __name__ == '__main__':
    ## Run the application on the local development server ##
    app.run(debug=True)