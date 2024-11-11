from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.secret_key = '23bcc70022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Colleges(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    location=db.Column(db.String(100))
    link=db.Column(db.String(200),nullable=False)
    
class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    info=db.Column(db.Text)

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    course=db.Column(db.String(200))
    fees=db.Column(db.String(200))
    eligibility=db.Column(db.String(200))
    app_date=db.Column(db.String(200))

class Cutoffs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    course_name=db.Column(db.String(200))
    cutoff=db.Column(db.String(200))

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    department=db.Column(db.String(200))
    location=db.Column(db.String(200))

class Distance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    distance_edu_info=db.Column(db.Text)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    faculty_name=db.Column(db.String(200))
    title=db.Column(db.String(200))
    department=db.Column(db.String(00))
    phone_no=db.Column(db.String(200))
    email=db.Column(db.String(200))

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    source=db.Column(db.String(200))

class Hostels(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    hostel_info=db.Column(db.Text)
    
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    info_data=db.Column(db.Text)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    title=db.Column(db.String(200))
    link=db.Column(db.String(200))

class Placements(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    company=db.Column(db.String(200))
    package=db.Column(db.String(200))
    job_roles=db.Column(db.String(200))
    headings=db.Column(db.String(200))

class Qa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    question=db.Column(db.Text)
    answer=db.Column(db.Text)

class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    ranking_agency=db.Column(db.String(200))
    year=db.Column(db.String(200))
    rank=db.Column(db.String(200))

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    rating=db.Column(db.String(100))
    pros=db.Column(db.Text)
    cons=db.Column(db.Text)

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.Integer)
    college_name = db.Column(db.String(200), nullable=False)
    info=db.Column(db.Text)

# Load college data
college_data = pd.read_csv('DATA\\next_500_colleges.csv')
info_data = pd.read_csv('DATA\\info_data_1000.csv')
admission_data = pd.read_csv('DATA\\adm2024_1000.csv')
course_fees_data = pd.read_csv('DATA\\coursefees1000.csv')
cutoff_data = pd.read_csv('DATA\\cutoff_marks_1000.csv')
departments_data = pd.read_csv('DATA\\departments_1000.csv')
distance_data = pd.read_csv('DATA\\distance_education_1000.csv')
faculty_data = pd.read_csv('DATA\\faculty_data_1000.csv')
gallery_data = pd.read_csv('DATA\\gallery_data_1000.csv')
hostel_data = pd.read_csv('DATA\\hostel_data_1000.csv')
news_data = pd.read_csv('DATA\\news_articles_data_1000.csv')
placement_data = pd.read_csv('DATA\\placement_data_1000.csv')
ranking_data = pd.read_csv('DATA\\ranking_data_1000.csv')
reviews_data = pd.read_csv('DATA\\reviews_1000.csv')
scholarship_data = pd.read_csv('DATA\\scholarship_data_1000.csv')
qa_data = pd.read_csv('DATA\\qa_data_1000.csv')

def load_data():
    # Check if tables are empty before loading
    if Colleges.query.first() is None:
        for _, row in college_data.iterrows():
            college = Colleges(serial_no=row['Serial No.'],name=row['College Name'], location=row['Location'],link=row['URL'])
            db.session.add(college)
        db.session.commit()
    
    if Admission.query.first() is None:
        for _, row in admission_data.iterrows():
            college = Admission(serial_no=row['Serial No.'],college_name=row['College Name'], info=row['Info'])
            db.session.add(college)
        db.session.commit()
    
    if Courses.query.first() is None:
        for _, row in course_fees_data.iterrows():
            college = Courses(serial_no=row['Serial No.'],college_name=row['College Name'], course=row['Course'],fees=row['Fees'],eligibility=row['Eligibility'],app_date=row['Application Date'])
            db.session.add(college)
        db.session.commit()
    
    if Cutoffs.query.first() is None:
        for _, row in cutoff_data.iterrows():
            college = Cutoffs(serial_no=row['Serial No.'],college_name=row['College Name'], course_name=row['Course Name'],cutoff=row['Cutoff Mark'])
            db.session.add(college)
        db.session.commit()
    
    if Departments.query.first() is None:
        for _, row in departments_data.iterrows():
            college = Departments(serial_no=row['Serial No.'],college_name=row['College Name'], department=row['Department'],location=row['Location'])
            db.session.add(college)
        db.session.commit()
    
    if Distance.query.first() is None:
        for _, row in distance_data.iterrows():
            college = Distance(serial_no=row['Serial No.'],college_name=row['College Name'], distance_edu_info=row['Distance Education Info'])
            db.session.add(college)
        db.session.commit()
    
    if Gallery.query.first() is None:
        for _, row in gallery_data.iterrows():
            college = Gallery(serial_no=row['Serial No.'],college_name=row['College Name'], source=row['Image Source'])
            db.session.add(college)
        db.session.commit()
    
    if Hostels.query.first() is None:
        for _, row in hostel_data.iterrows():
            college = Hostels(serial_no=row['Serial No.'],college_name=row['College Name'], hostel_info=row['Info'])
            db.session.add(college)
        db.session.commit()
    
    if Faculty.query.first() is None:
        for _, row in faculty_data.iterrows():
            college = Faculty(serial_no=row['Serial No.'],college_name=row['College Name'], faculty_name=row['Faculty Name'],title=row['Title'],department=row['Department'],phone_no=row['Phone No'],email=row['Email'])
            db.session.add(college)
        db.session.commit()
    
    if Info.query.first() is None:
        for _, row in info_data.iterrows():
            college = Info(serial_no=row['Serial No.'],college_name=row['College Name'], info_data=row['Info Data'])
            db.session.add(college)
        db.session.commit()
    
    if News.query.first() is None:
        for _, row in news_data.iterrows():
            college = News(serial_no=row['Serial No.'],college_name=row['College Name'],title=row['Title'],link=row['Link'])
            db.session.add(college)
        db.session.commit()
    
    if Placements.query.first() is None:
        for _, row in placement_data.iterrows():
            college = Placements(serial_no=row['Serial No.'],college_name=row['College Name'], company=row['Company'],package=row['Package'],job_roles=row['Job Roles'],headings=row['Headings'])
            db.session.add(college)
        db.session.commit()
    
    if Qa.query.first() is None:
        for _, row in qa_data.iterrows():
            college = Qa(serial_no=row['Serial No.'],college_name=row['College Name'],question=row['Question'], answer=row['Answer'])
            db.session.add(college)
        db.session.commit()
    
    if Ranking.query.first() is None:
        for _, row in ranking_data.iterrows():
            college = Ranking(serial_no=row['Serial No.'],college_name=row['College Name'], ranking_agency=row['Ranking Agency'], year=row['Year'], rank=row['Rank'])
            db.session.add(college)
        db.session.commit()
    
    if Reviews.query.first() is None:
        for _, row in reviews_data.iterrows():
            college = Reviews(serial_no=row['Serial No.'],college_name=row['College Name'],rating=row['Rating'],pros=row['Pros'], cons=row['Cons'])
            db.session.add(college)
        db.session.commit()
    
    if Scholarship.query.first() is None:
        for _, row in scholarship_data.iterrows():
            college = Scholarship(serial_no=row['Serial No.'],college_name=row['College Name'], info=row['Scholarship Info'])
            db.session.add(college)
        db.session.commit()
    
   

# Initialize database
@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()
    load_data()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            return redirect(url_for('landing_page'))
        error_message = 'Invalid credentials. Please try again.'
        return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account has been created successfully!', 'success')
        #return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/landing')
def landing_page():
    if 'user' in session:
        return render_template('landing.html',username=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/engineering_colleges', methods=['GET', 'POST'])
def engineering_colleges():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    search_query = request.form.get('search_query')
    if search_query:
        filtered_colleges = Colleges.query.filter(Colleges.name.ilike(f'%{search_query}%')).all()
    else:
        filtered_colleges = Colleges.query.all()
    return render_template('engineering_colleges.html', colleges=filtered_colleges)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/info/<int:college_id>')
def info(college_id): 
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    college_info = Info.query.filter_by(serial_no=college_id).first()
    gallery_info = Gallery.query.filter_by(serial_no=college_id).all()
    return render_template('info.html', college_info=college_info, gallery_info=gallery_info, college_id=college_id, college_name=college_name)

@app.route('/adms/<int:college_id>')
def adms(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    admission_info = Admission.query.filter_by(serial_no=college_id).first()
    gallery_info = Gallery.query.filter_by(serial_no=college_id).all()
    return render_template('adms.html', admission_info=admission_info, gallery_info=gallery_info, college_id=college_id, college_name=college_name)

@app.route('/course/<int:college_id>')
def course(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    course_info = Courses.query.filter_by(serial_no=college_id).all()
    return render_template('course.html', course_info=course_info, college_id=college_id, college_name=college_name)

@app.route('/cutoff/<int:college_id>')
def cutoff(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    cutoff_info = Cutoffs.query.filter_by(serial_no=college_id).all()
    return render_template('cutoff.html', cutoff_info=cutoff_info, college_id=college_id, college_name=college_name)

@app.route('/departments/<int:college_id>')
def departments(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    departments_info = Departments.query.filter_by(serial_no=college_id).all()
    return render_template('departments.html', departments_info=departments_info, college_id=college_id, college_name=college_name)

@app.route('/distance/<int:college_id>')
def distance(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    distance_info = Distance.query.filter_by(serial_no=college_id).first()
    gallery_info = Gallery.query.filter_by(serial_no=college_id).all()
    return render_template('distance.html', distance_info=distance_info, gallery_info=gallery_info, college_id=college_id, college_name=college_name)

@app.route('/faculty/<int:college_id>')
def faculty(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    faculty_info = Faculty.query.filter_by(serial_no=college_id).all()
    return render_template('faculty.html', faculty_info=faculty_info, college_id=college_id, college_name=college_name)

@app.route('/gallery/<int:college_id>')
def gallery(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    gallery_info = Gallery.query.filter_by(serial_no=college_id).all()
    return render_template('gallery.html', gallery_info=gallery_info, college_id=college_id, college_name=college_name)

@app.route('/hostel/<int:college_id>')
def hostel(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    hostel_info = Hostels.query.filter_by(serial_no=college_id).first()
    gallery_info = Gallery.query.filter_by(serial_no=college_id).all()
    return render_template('hostel.html', hostel_info=hostel_info, gallery_info=gallery_info, college_id=college_id, college_name=college_name)

@app.route('/news/<int:college_id>')
def news(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    news_info = News.query.filter_by(serial_no=college_id).all()
    gallery_info = Gallery.query.filter_by(serial_no=college_id).all()
    return render_template('news.html', news_info=news_info, gallery_info=gallery_info, college_id=college_id, college_name=college_name)

@app.route('/placement/<int:college_id>')
def placement(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    print(f"College Name Received: {college_name}")
    placement_info = Placements.query.filter_by(serial_no=college_id).all()
    if placement_info:
        headings = placement_info[0].headings.split(', ')
    else:
        headings = ["No headings found"] * 3
    return render_template('placement.html', placement_info=placement_info, college_id=college_id, college_name=college_name, headings=headings,size=len(headings))

@app.route('/ranking/<int:college_id>')
def ranking(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    ranking_info = Ranking.query.filter_by(serial_no=college_id).all()
    return render_template('ranking.html', ranking_info=ranking_info, college_id=college_id, college_name=college_name)

@app.route('/reviews/<int:college_id>')
def reviews(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    reviews_info = Reviews.query.filter_by(serial_no=college_id).all()
    return render_template('reviews.html', reviews_info=reviews_info, college_id=college_id, college_name=college_name)

@app.route('/scholarship/<int:college_id>')
def scholarship(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    scholarship_info = Scholarship.query.filter_by(serial_no=college_id).first()
    gallery_info = Gallery.query.filter_by(serial_no=college_id).all()
    return render_template('scholarship.html', scholarship_info=scholarship_info, gallery_info=gallery_info, college_id=college_id, college_name=college_name)

@app.route('/qa/<int:college_id>')
def qa(college_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    college=Colleges.query.filter_by(serial_no=college_id).first()
    college_name = college.name
    qa_info = Qa.query.filter_by(serial_no=college_id).all()
    return render_template('qa.html', qa_info=qa_info, college_id=college_id, college_name=college_name)

if __name__ == '__main__':
    app.run(debug=True)
