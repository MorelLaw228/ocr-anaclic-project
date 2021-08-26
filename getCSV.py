#!/usr/bin/python3

from flask import Flask,Response , send_file

app = Flask(__name__)

@app.route("/")
def hello():
    return '''
            <html><body>
            Hello . <a href ="/getPlotCSV"> Cliquez ICI </a>
            </body></html>
        '''

@app.route("/getPlotCSV")
def getPlotCVS():
    csv = '1,2,3\n4,5,6\n'

    return Response(
        csv,
        mimeType = "text/csv",
        headers = {"Content-disposition":"attachement;"
                                         "filename = myplot.csv"}
    )

@app.route('/getPlotCSV_2')
def plot_csv():
    return send_file('/output/Adjacency.csv',
                     mimetype = 'text/csv',
                     attachement_filename = 'Adjacency.csv',
                     as_attachement = True)


if __name__ == '_main__':
    app.run(debug = True)
