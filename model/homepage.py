from flask import Flask,render_template,request
import bikeshare

app = Flask(__name__)
"""" This path is loaded in browser when the server is started   """
@app.route("/")
def welcome():
    details=bikeshare.dropdown_values()
    return render_template('index.html',city=details[0], month=details[1], day=details[2] )

"""" On click of submit this method is called for detailed statistics generation  """	
@app.route('/stat_details', methods=['POST'])
def stat_details():
    sel_city = request.form['city']
    sel_month = request.form['month']
    sel_day = request.form['day']
    somedata =bikeshare.statsgen(sel_city,sel_month,sel_day)
    return '<p style="font-weight:bold">Hello {}</p>  <a style="text-decoration:none;" href="/">Back Home</a>'.format(somedata)


""""  Begining  of execution  """
if __name__ == "__main__":
    app.run()