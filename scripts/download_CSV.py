#!/usr/bin/python3


from flask import Flask,make_response,Response,send_file

app = Flask(__name__)


# Fonction pour télécharger un fichier CSV lorsque l'on appuie sur un bouton

@app.route("/")
def hello():
    return '''
            <html>
                <body>
                
                <center>Salut Tout le monde : <a href ="/download_csv">CLIQUEZ ICI.</a></center>
                
                </body>
            </html>
    '''

@app.route("/download_csv")
def telecharger_csv():
    csv = '1,2,3\n4,5,6\n7,8,9\n10,11,12\n13,14,15\n'

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-Disposition":"attachement;" \
                                       "filename=monCSV.csv"}
    )


@app.route('/csv')
def download_csv():
    csv = 'foo,bar,baz\nhai,bai,crai\n'
    response = make_response(csv)

    cd = 'attachement; filename = mon_resultat.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response

@app.route("/getPlotCSV")
def getPlotCVS():
    csv = '1,2,3\n4,5,6\n'

    return Response(
        csv,
        mimetype = "text/csv",
        headers = {"Content-disposition":"attachement;"
                                         "filename = myplot.csv"}
    )


# To send a static file

#@app.route("/send_csv")
#def send_csv():
#    return send_file('outputs/Adjacency.csv',
#                     mimetype='text/csv',
#                     attachment_filename='Adjacency.csv',
#                     as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
