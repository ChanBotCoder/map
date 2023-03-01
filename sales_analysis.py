from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os

app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Define the route for the analysis page
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        # Save the file to disk
        file.save(os.path.join('uploads', file.filename))
        # Load the data into a Pandas DataFrame
        data = pd.read_csv(os.path.join('uploads', file.filename))
        
        
        data_org = data
        
        remove_col=['Reg. Number','Stud. Name','RA','CGPA']
        for i in range(0,len(remove_col)):
            data_org= data_org.drop(remove_col[i],axis='columns')
        
        subject =[i for i in data_org.columns]
        
        for i in range(0,len(subject)):
            sales_data = data.groupby(['Reg. Number', 'Stud. Name'])[subject[i]].sum().reset_index()
            # Create plot
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Sales by Region", "Sales by Product"))
            fig.add_trace(go.Bar(x=sales_data['Reg. Number'], y=sales_data[subject[i]], name=subject[i]), row=1, col=1)
            #fig.add_trace(go.Bar(x=sales_data['Product'], y=sales_data['Sales'], name='Sales'), row=1, col=2)
            fig.update_layout(showlegend=False)
            # Convert plot to HTML format
            plot_html = fig.to_html(full_html=False)
            return render_template('analysis.html', table=data.to_html(classes='table table-striped'), plot=plot_html)
        # Render the analysis page with the plot and data table
    else:
        return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)
