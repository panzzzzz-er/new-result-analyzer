from flask import Flask, render_template, request, url_for, send_file
import reform as rf
import analyzer as ana
import statistics as stats
import seaborn as sns
import pandas as pd
import io
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = os.path.join('static', 'upload')

# app = Flask(__name__)'


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route("/")
    def index():
        return render_template('home.html')

    @app.route('/download')
    def download():
        filename = request.args.get('filename')
        return send_file(f'processed_csv\\{filename}', as_attachment=True)

    @app.route("/report", methods=['POST', 'GET'])
    def report():
        semester = int(request.form.get('semester'))
        br = request.form.get('branch')
        year = request.form.get('year')
        try:
            file = request.files['file']
            if file and allowed_file(file.filename):
                data_filename = secure_filename(file.filename)
                file.save(os.path.join('upload', data_filename))
                newname = f'upload/{data_filename}'

        except Exception as e:
            print(e)

        branch = ''
        if br=='a': branch = 'Artificial Intelligence and Data Science'
        elif br=='c': branch = 'Computer Science Engineering'
        elif br=='e': branch = 'Electronics and Computer Science'
        elif br=='m': branch = 'Mechanical Engineering'

        result = pd.read_csv(newname)
        cleared_result = rf.clear_result_data(result, semester, br)
        # print(cleared_result)

        strenght = len(cleared_result)

        # to allow user to download the cleaned csv file
        filename = 'cleaned_mu_result.csv'
        path = os.path.join('processed_csv', filename)
        cleared_result.to_csv(path, index=False)
        download_link = f'/download?filename={filename}'

        avg_cgpa, CGPA = ana.get_avg_cgpa(cleared_result)
        avg_perc, percentages = ana.get_avg_percentage(CGPA)
        # print(avg_cgpa, avg_perc)
        # print(CGPA)
        # print(percentages)

        toppers = ana.find_toppers(cleared_result)
        # print(toppers)

        ten_cgpaers = CGPA.count(10)
        subject_maxmarks = ana.find_sub_max(cleared_result, semester)
        # print(ten_cgpaers)
        # print(subject_maxmarks)

        plot1 = sns.displot(CGPA, kde=True, bins=15)
        plot1.savefig('static/graphs/cgpa.png')

        plot2 = sns.displot(percentages, kde=True, bins=15)
        plot2.savefig('static/graphs/perc.png')

        student_ranges = ana.count_students(percentages)
        # print(student_ranges)

        kts = ana.find_kts(cleared_result)
        # print(kts)

        sub_ranges = ana.find_sub_mark_ranges(cleared_result, semester)
        # print(sub_ranges)

        return render_template('report.html',
                               semester=semester,
                               branch=branch,
                               year=year,
                               filename=filename,
                               download_link=download_link,
                               avg_cgpa=round(avg_cgpa, 3),
                               avg_perc=round(avg_perc, 3),
                               toppers=toppers,
                               ten_cgpaers=ten_cgpaers,
                               subject_maxmarks=subject_maxmarks,
                               student_ranges=student_ranges,
                               kts=kts,
                               strenght = strenght,
                               sub_ranges = sub_ranges
                               )

    if __name__ == '__main__':
        app.run(debug=True, port='5000')

    return app
